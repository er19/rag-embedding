from core.claude import Claude
from mcp_client import MCPClient
from core.tools import ToolManager


class Chat:
    def __init__(self, claude_service: Claude, clients: dict[str, MCPClient]):
        self.claude_service: Claude = claude_service
        self.clients: dict[str, MCPClient] = clients
        self.messages: list[dict] = []

    async def _process_query(self, query: str):
        self.messages.append({"role": "user", "content": query})

    async def run(
        self,
        query: str,
    ) -> str:
        final_text_response = ""

        await self._process_query(query)

        while True:
            response = self.claude_service.chat(
                messages=self.messages,
                tools=await ToolManager.get_all_tools(self.clients),
            )

            self.claude_service.add_assistant_message(self.messages, response)

            finish_reason = response.choices[0].finish_reason
            tool_calls = response.choices[0].message.tool_calls

            if finish_reason == "tool_calls" or tool_calls:
                text = self.claude_service.text_from_message(response)
                if text:
                    print(text)
                tool_results = await ToolManager.execute_tool_requests(
                    self.clients, response
                )

                self.claude_service.add_user_message(
                    self.messages, tool_results
                )
            else:
                final_text_response = self.claude_service.text_from_message(
                    response
                )
                break

        return final_text_response
