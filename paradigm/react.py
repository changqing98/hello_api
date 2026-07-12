# ReAct 提示词模板
import json
import os
from typing import List, Dict

from dotenv import load_dotenv
from keyring.core import load_env
from openai import OpenAI
from sympy import false

system_template = """
你运行在一个和思考、行动、观察和回答的循环,在循环结束时,你输出最终的答案。
用【思考"来描述你对被问问题的想法。
用"操作"运行您可用的操作之一。
"观察"将是运行这些操作的结果。
"答案"将是分析观察结果的结果。
"""

# 加载 .env 文件中的环境变量
load_dotenv()

message_history = []
message_history.append({"role": "system", "content": system_template})


def get_info_on_ball_game(name):
    data = [
        {
            "name": "篮球",
            "team_members": 11,
            "players_on_field": 6,
        },

        {
            "name": "排球",
            "team_members": 11,
            "players_on_field": 5,
        }
    ]
    for item in data:
        if item["name"] == name:
            return item
    return None


class ReactAgent:
    """
    为本书 "Hello Agents" 定制的LLM客户端。
    它用于调用任何兼容OpenAI接口的服务，并默认使用流式响应。
    """

    def __init__(self, model: str = None, apiKey: str = None, baseUrl: str = None, timeout: int = None):
        """
        初始化客户端。优先使用传入参数，如果未提供，则从环境变量加载。
        """
        self.model = model or os.getenv("LLM_MODEL_ID")
        apiKey = apiKey or os.getenv("LLM_API_KEY")
        baseUrl = baseUrl or os.getenv("LLM_BASE_URL")
        timeout = timeout or int(os.getenv("LLM_TIMEOUT", 60))

        if not all([self.model, apiKey, baseUrl]):
            raise ValueError("模型ID、API密钥和服务地址必须被提供或在.env文件中定义。")

        self.client = OpenAI(api_key=apiKey, base_url=baseUrl, timeout=timeout)

    def complete(self, message) -> str:
        message_history.append(message)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=message_history,
            stream=False,
            temperature=0,
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "get_info_on_ball_game",
                        "description": "获取球类运动人数",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                            }
                        },
                        "strict": True,
                    }
                }
            ]
        )
        response_dict = dict(response.choices[0].message)
        message_history.append(response_dict)
        return response_dict

    def agent(self, query):
        max_turns = 5
        current_turns = 1
        next_message = {"role": "user", "content": query}
        while current_turns < max_turns:
            message = self.complete(next_message)
            print(message['content'])
            if message['tool_calls']:
                func_call_id = message['tool_calls'][0].id
                func_kwargs = json.loads(message['tool_calls'][0].function.arguments)
                func_result = get_info_on_ball_game(**func_kwargs)
                print(f"观察：{func_result}")
                next_message = {"role": "tool", "tool_call_id": func_call_id, "content": str(func_result)}
            else:
                break


if __name__ == '__main__':
    query = "请问篮球运动在场人数乘以排球运动在场人数，结果等于多少"
    client = ReactAgent()
    client.agent(query)
