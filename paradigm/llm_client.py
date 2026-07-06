"""
兼容层：LLM 客户端已迁移到 infra/llm。

推荐新用法：
    from infra.llm import OpenAILLMClient, GLMLLMClient, LLMStrategyContext
"""

from infra.llm import GLMLLMClient, HelloAgentsLLM, LLMClient, OpenAILLMClient

__all__ = [
    "LLMClient",
    "OpenAILLMClient",
    "GLMLLMClient",
    "HelloAgentsLLM",
]


# --- 客户端使用示例 ---
if __name__ == '__main__':
    try:
        llmClient: LLMClient = OpenAILLMClient()

        exampleMessages = [
            {"role": "system", "content": "You are a helpful assistant that writes Python code."},
            {"role": "user", "content": "写一个快速排序算法"}
        ]

        print("--- complete(同步) ---")
        responseText = llmClient.complete(exampleMessages)
        if responseText:
            print(responseText)

        print("\n--- complete_stream(流式) ---")
        streamText = []
        for delta in llmClient.complete_stream(exampleMessages):
            print(delta, end="", flush=True)
            streamText.append(delta)
        print()

    except ValueError as e:
        print(e)
