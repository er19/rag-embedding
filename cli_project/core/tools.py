import json
from typing import Optional, List
from mcp.types import CallToolResult, Tool, TextContent
from mcp_client import MCPClient
from openai.types.chat import ChatCompletion


class ToolManager:
    @classmethod
    async def get_all_tools(cls, clients: dict[str, MCPClient]) -> list:
        """Gets all tools from the provided clients in OpenAI function-calling format."""
        tools = []
        for client in clients.values():
            tool_models = await client.list_tools()
            tools += [
                {
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description,
                        "parameters": t.inputSchema,
                    },
                }
                for t in tool_models
            ]
        return tools

    @classmethod
    async def _find_client_with_tool(
        cls, clients: list[MCPClient], tool_name: str
    ) -> Optional[MCPClient]:
        """Finds the first client that has the specified tool."""
        for client in clients:
            tools = await client.list_tools()
            tool = next((t for t in tools if t.name == tool_name), None)
            if tool:
                return client
        return None

    @classmethod
    def _build_tool_result(cls, tool_call_id: str, content: str) -> dict:
        """Builds a tool result message in OpenAI format."""
        return {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": content,
        }

    @classmethod
    async def execute_tool_requests(
        cls, clients: dict[str, MCPClient], message: ChatCompletion
    ) -> List[dict]:
        """Executes tool calls from an OpenAI ChatCompletion response."""
        tool_calls = message.choices[0].message.tool_calls or []
        tool_results: list[dict] = []

        for tool_call in tool_calls:
            tool_call_id = tool_call.id
            tool_name = tool_call.function.name
            tool_input = json.loads(tool_call.function.arguments)

            client = await cls._find_client_with_tool(
                list(clients.values()), tool_name
            )

            if not client:
                tool_result = cls._build_tool_result(
                    tool_call_id, "Could not find that tool"
                )
                tool_results.append(tool_result)
                continue

            try:
                tool_output: CallToolResult | None = await client.call_tool(
                    tool_name, tool_input
                )
                items = []
                if tool_output:
                    items = tool_output.content
                content_list = [
                    item.text for item in items if isinstance(item, TextContent)
                ]
                content_json = json.dumps(content_list)
                tool_result = cls._build_tool_result(tool_call_id, content_json)
            except Exception as e:
                error_message = f"Error executing tool '{tool_name}': {e}"
                print(error_message)
                tool_result = cls._build_tool_result(
                    tool_call_id, json.dumps({"error": error_message})
                )

            tool_results.append(tool_result)
        return tool_results
