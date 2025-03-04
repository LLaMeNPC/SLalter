import ollama

class Rewriter:

    def __init__(self, model_string) -> None:
        self.client = ollama.Client()
        self.client.create(
            model='Rewriter',
            from_=model_string,
            system="""
                You are a rewriter, who specializes in rewriting sentences with the same meaning and emotion. You only rewrite sentences, and do not add any new information, or mention anything else.
            """
        )

    def rewrite(self, sentence) -> str:
        return ollama.chat(
            model="Rewriter",
            messages=[{"role": "user", "content": f"""
            Please rewrite the following sentence, keeping the meaning, emotion and tone intact:
            {sentence}
            """}]
        )["message"]["content"]
