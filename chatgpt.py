from prompt import Prompt  # 修正引用方式
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatGPT:
    def __init__(self):
        self.prompt = Prompt()
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")  # 更新模型
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", 0))
        self.frequency_penalty = float(os.getenv("OPENAI_FREQUENCY_PENALTY", 0))
        self.presence_penalty = float(os.getenv("OPENAI_PRESENCE_PENALTY", 0.6))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", 240))

    def get_response(self):
        response = openai.ChatCompletion.create(  # 修正 API 版本
            model=self.model,
            messages=[{"role": "user", "content": self.prompt.generate_prompt()}],
            temperature=self.temperature,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            max_tokens=self.max_tokens
        )
        return response['choices'][0]['message']['content'].strip()

    def add_msg(self, text):
        self.prompt.add_msg(text)
