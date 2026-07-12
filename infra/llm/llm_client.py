from abc import ABC, abstractmethod
from typing import Dict, Iterator, List, Optional

Message = Dict[str, str]
Messages = List[Message]


class CompleteCommand:
    def __init__(self, messages: Messages, temperature: float = 1, stream: bool = False):
        self.messages = messages
        self.temperature = temperature
        self.stream = stream


class LLMClient(ABC):
    """
    LLMClient 接口，约束统一的调用方式。
    """

    @abstractmethod
    def complete(self, cmd: CompleteCommand) -> Optional[str]:
        """
        同步返回完整的大模型响应。
        """
        raise NotImplementedError
