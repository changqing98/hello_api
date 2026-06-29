from unittest import TestCase

from infra.llm import glm


class Test(TestCase):
    def test_get_completion(self):
        completion = glm.get_completion("hello, 你好")
        print(completion)


    def test_get_embedding(self):
        completion = glm.get_embedding("hello, 你好")
        print(completion)
