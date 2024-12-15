import openai
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class ChatGptApi:

    def __init__(self):
        pass


    def predict(self, prompt) -> str:
        response = openai.Completion.create(
            model="gpt-4o",
            prompt=prompt,
            max_tokens=200,
            temperature=0.02,
            top_p=1.0,
            n=1,
            stop='}'
        )
        print(response)
        return response.choices[0].text.strip() + '}'
