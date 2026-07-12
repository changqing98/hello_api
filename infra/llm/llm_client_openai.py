import os
from typing import Iterator, Optional

from dotenv import load_dotenv
from openai import OpenAI

from .llm_client import LLMClient, Messages

# 加载 .env 文件中的环境变量
load_dotenv()


class OpenAILLMClient(LLMClient):
    """
    OpenAI 兼容协议的公共实现。
    OpenAI、GLM 都通过该能力复用。
    """

    def __init__(self, model: str, apiKey: str, baseUrl: str, timeout: int = 60, providerName: str = "LLM"):
        if not all([model, apiKey, baseUrl]):
            raise ValueError(f"{providerName} 的模型ID、API密钥和服务地址必须被提供或在.env文件中定义。")

        self.model = model
        self.providerName = providerName
        self.client = OpenAI(api_key=apiKey, base_url=baseUrl, timeout=timeout)

    def complete(self, messages: Messages, temperature: float = 0) -> Optional[str]:
        """
        同步返回完整文本。
        """
        print(f"🧠 正在调用 {self.providerName} 模型: {self.model}")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=False,
            )
            print("✅ 大语言模型响应成功")
            return response.choices[0].message.content or ""
        except Exception as e:
            print(f"❌ 调用 {self.providerName} API 时发生错误: {e}")
            return None

    def complete_stream(self, messages: Messages, temperature: float = 0) -> Iterator[str]:
        """
        流式返回增量文本。
        """
        print(f"🧠 正在流式调用 {self.providerName} 模型: {self.model}")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,
            )

            for chunk in response:
                choices = getattr(chunk, "choices", [])
                if not choices:
                    continue
                content = getattr(choices[0].delta, "content", None) or ""
                if content:
                    yield content

        except Exception as e:
            print(f"❌ 流式调用 {self.providerName} API 时发生错误: {e}")
            return
