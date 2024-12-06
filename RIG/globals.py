import os


class Globals:

    def __init__(self):
        self.project_directory = "/Users/yuda/PycharmProjects/EltaProject_v1/archive/data_directory/" # ensure the / in the end

        self.llama_server_path = "/Users/yuda/PycharmProjects/EltaProject_v1/archive/data_directory/llama.cpp/llama-server"
        self.rag_model_path = "/Users/yuda/PycharmProjects/EltaProject_v1/archive/data_directory/BAAI/bge-m3"
        self.gpt_model_path = "/Users/yuda/PycharmProjects/EltaProject_v1/archive/data_directory/gemma-2-2b-it-Q8_0.gguf"

        self.db_path = "db_data.csv"
        self.db_manager = None  # temporarily

        self.rag_difference = 0.001
        self.rag_threshold = 0.5
        self.max_context_length = 1512
        self.n_threads = os.cpu_count() - 2 if os.cpu_count() - 2 > 1 else 1
        self.max_new_tokens = 512


GLOBALS = Globals()


class Models:

    def __init__(self):
        self.rag_api = None
        self.gemma_api = None

MODELS = Models()