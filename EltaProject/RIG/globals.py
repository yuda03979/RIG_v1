import os


project_directory = "/Users/yuda/PycharmProjects/EltaBenchmark/benchmark/data_directory/"  # change that


class Globals:

    def __init__(self):
        self.models_directory = project_directory

        self.rag_model_name = "BAAI/bge-m3"
        self.rag_model_path = ""
        self.gpt_model_path = ""

        self.db_path = project_directory + "db_data.csv"
        self.db_manager = None  # temporarily

        self.rag_difference = 0.001
        self.rag_threshold = 0.5
        self.max_context_length = 1512
        self.n_threads = os.cpu_count() - 2 if os.cpu_count() - 2 > 1 else 1
        self.max_new_tokens = 512


GLOBALS = Globals()
