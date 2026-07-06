from abc import ABC, abstractmethod
from typing import Dict, Iterator, List, Optional

Message = Dict[str, str]
Messages = List[Message]


class LLMClient(ABC):
    """
    LLMClient 接口，约束统一的调用方式。
    """

    @abstractmethod
    def complete(self, messages: Messages, temperature: float = 0) -> Optional[str]:
        """
        同步返回完整的大模型响应。
        """
        raise NotImplementedError

    @abstractmethod
    def complete_stream(self, messages: Messages, temperature: float = 0) -> Iterator[str]:
        """
        流式返回大模型响应增量。
        """
        raise NotImplementedError
