from openai import OpenAI
from openai.types.chat import ChatCompletion


class Claude:
    def __init__(self, model: str, base_url: str, api_key: str):
        # Ensure base_url ends with /v1 as required by the OpenAI SDK
        if not base_url.rstrip("/").endswith("/v1"):
            base_url = base_url.rstrip("/") + "/v1"
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model

    def add_user_message(self, messages: list, message):
        if isinstance(message, ChatCompletion):
            # Extract text from a ChatCompletion response
            content = self.text_from_message(message)
        elif isinstance(message, list):
            # Tool results: list of {"role": "tool", ...} dicts
            messages.extend(message)
            return
        else:
            content = message

        messages.append({"role": "user", "content": content})

    def add_assistant_message(self, messages: list, message):
        if isinstance(message, ChatCompletion):
            # Append the raw assistant message from the response
            msg = message.choices[0].message
            assistant_msg = {"role": "assistant", "content": msg.content or ""}
            if msg.tool_calls:
                assistant_msg["tool_calls"] = [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in msg.tool_calls
                ]
            messages.append(assistant_msg)
        else:
            messages.append({"role": "assistant", "content": message})

    def text_from_message(self, message: ChatCompletion) -> str:
        content = message.choices[0].message.content
        return content if content else ""

    def chat(
        self,
        messages,
        system=None,
        temperature=1.0,
        stop_sequences=None,
        tools=None,
    ) -> ChatCompletion:
        full_messages = []

        if system:
            full_messages.append({"role": "system", "content": system})

        full_messages.extend(messages)

        params = {
            "model": self.model,
            "messages": full_messages,
            "temperature": temperature,
        }

        if stop_sequences:
            params["stop"] = stop_sequences

        if tools:
            params["tools"] = tools

        response = self.client.chat.completions.create(**params)
        return response
