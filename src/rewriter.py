import ollama
from config_getter import get_config

class Rewriter:

    def __init__(self, model_string) -> None:
        self.config = get_config()
        self.client = ollama.Client()
        self.client.create(
            model='Rewriter',
            from_=model_string,
            system=self.config["rewrite_system_prompt"]
        )

    def rewrite(self, sentence) -> str:
        return ollama.chat(
            model="Rewriter",
            options={"temperature":self.config["temperature"]},
            messages=[
                {
                    "role": self.config["role"], 
                    "content": self.config["rewrite_prompt"].format(sentence=sentence)}]
        )["message"]["content"]
