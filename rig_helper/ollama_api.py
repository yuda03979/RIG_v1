from typing import Union, Sequence
import ollama
from tqdm import tqdm

class OllamaApi:

    def __init__(self, model_name):
        self.model_name = model_name
        self.pull()
    
    def pull(self):

        current_digest, bars = '', {}
        for progress in ollama.pull(self.model_name, stream=True):
            digest = progress.get('digest', '')
            if digest != current_digest and current_digest in bars:
                bars[current_digest].close()

            if not digest:
                print(progress.get('status'))
                continue

            if digest not in bars and (total := progress.get('total')):
                bars[digest] = tqdm(total=total, desc=f'pulling {digest[7:19]}', unit='B', unit_scale=True)

            if completed := progress.get('completed'):
                bars[digest].update(completed - bars[digest].n)

        current_digest = digest


    def chat_stream(self, messages: list):
        response = ''
        for part in ollama.chat(self.model_name, messages=messages, stream=True):
            response += part['message']['content']
            print(part['message']['content'], end='', flush=True)
        return response


    def embed(self, input: Union[str, Sequence[str]]):
        return ollama.embed(model=self.model_name, input=input)['embeddings']


    def generate_schema(self):
        pass

    def get_tasks(self):
        return {
            "chat_stream": self.chat_stream,
            "embed": self.embed
        }
    
    def close(self):
        ollama.generate(model=self.model_name, keep_alive=0)
        return f"<closed model {self.model_name}>"