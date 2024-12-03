import random

import numpy as np
from llama_cpp import Llama
import torch
from RIG.globals import GLOBALS

torch.set_num_threads(4)
random.seed(42)
np.random.seed(42)
torch.manual_seed(42)


class GemmaApi:

    def __init__(self):

        self.model = Llama(
            model_path=f"{GLOBALS.models_directory}gemma-2-2b-it-Q8_0.gguf",
            cache_dir=GLOBALS.models_directory,
            n_ctx=GLOBALS.max_context_length,
            n_threads=GLOBALS.n_threads,
            temperature=0.0,
            decoding_method="greedy",
            flash_attention=True,
            verbose=False
        )


    def predict(self, prompt) -> str:
        response = self.model.create_completion(
            prompt=str(prompt),
            max_tokens=GLOBALS.max_new_tokens,
            stop=['}']
            # seed=0,
        )["choices"][0]["text"]
        return response
