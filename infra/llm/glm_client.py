import os
from typing import Iterator, Optional

from dotenv import load_dotenv
from zhipuai import ZhipuAI

from .llm_client import LLMClient, Messages

# 加载 .env 文件中的环境变量
load_dotenv()


class GLMLLMClient(LLMClient):
    """
    GLM（智谱）实现，基于 zhipuai SDK。
    """

    def __init__(self, model: str = None, apiKey: str = None, baseUrl: str = None, timeout: int = None):
        self.model = model or os.getenv("GLM_MODEL_ID") or "glm-4-plus"
        apiKey = apiKey or os.getenv("GLM_API_KEY")

        if not apiKey:
            raise ValueError("GLM 的 API 密钥必须被提供或在 .env 文件中定义。")

        # 当前 zhipuai SDK 主要通过 api_key 初始化，baseUrl/timeout 参数保留以兼容构造签名。
        _ = baseUrl, timeout
        self.client = ZhipuAI(api_key=apiKey)

    def complete(self, messages: Messages, temperature: float = 0) -> Optional[str]:
        """
        同步返回完整文本。
        """
        print(f"🧠 正在调用 GLM 模型: {self.model}")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
            )
            print("✅ 大语言模型响应成功")

            choices = getattr(response, "choices", [])
            if not choices:
                return ""

            message = getattr(choices[0], "message", None)
            return (getattr(message, "content", None) or "") if message else ""
        except Exception as e:
            print(f"❌ 调用 GLM API 时发生错误: {e}")
            return None

    def complete_stream(self, messages: Messages, temperature: float = 0) -> Iterator[str]:
        """
        流式返回增量文本。
        """
        print(f"🧠 正在流式调用 GLM 模型: {self.model}")
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

                delta = getattr(choices[0], "delta", None)
                content = (getattr(delta, "content", None) or "") if delta else ""
                if content:
                    yield content

        except Exception as e:
            print(f"❌ 流式调用 GLM API 时发生错误: {e}")
            return
