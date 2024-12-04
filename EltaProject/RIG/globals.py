import os


data_directory = "/Users/yuda/PycharmProjects/EltaBenchmark/benchmark/data_directory/"  # change that
db_file_name = "db_data.csv"  # you also can change that


class Globals:

    def __init__(self):
        self.models_directory = data_directory

        self.db_file_name = db_file_name
        self.db_path = data_directory + db_file_name
        self.db_manager = None  # temporarily

        self.rag_difference = 0.001
        self.rag_threshold = 0.5
        self.max_context_length = 1512
        self.n_threads = os.cpu_count() - 2 if os.cpu_count() - 2 > 1 else 1
        self.max_new_tokens = 512


GLOBALS = Globals()
