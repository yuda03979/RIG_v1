import os
import time
from datetime import datetime

from RIG.src.Utils.db_manager import DBManager
from RIG.globals import GLOBALS
from RIG.src.App.rule_instance.get import Get
from RIG.src.App.new_type import NewType
from RIG.src.Utils.utils import log_interactions

from RIG.src.Utils.rag_api import RagApi
from RIG.src.Utils.gemma_api import GemmaApi
from RIG.src.Utils.gpt_server import GPTServer


def set_globals(project_directory, rag_model_path, gpt_model_path, llama_server_path, db_path, rag_difference, rag_threshold, max_context_length, max_new_tokens,
                n_threads):
    GLOBALS.db_manager = DBManager(db_path)
    GLOBALS.project_directory = project_directory
    GLOBALS.gpt_model_path = gpt_model_path
    GLOBALS.rag_model_path = rag_model_path
    GLOBALS.rag_difference = rag_difference
    GLOBALS.rag_threshold = rag_threshold
    GLOBALS.max_context_length = max_context_length
    GLOBALS.max_new_tokens = max_new_tokens
    GLOBALS.n_threads = n_threads
    GLOBALS.llama_server_path = llama_server_path


class RuleInstanceGenerator:

    def __init__(self,
                 project_directory=GLOBALS.project_directory,
                 rag_model_path=GLOBALS.rag_model_path,
                 gpt_model_path=GLOBALS.gpt_model_path,
                 llama_server_path=GLOBALS.llama_server_path,
                 db_path=GLOBALS.db_path,
                 rag_difference=GLOBALS.rag_difference,
                 rag_threshold=GLOBALS.rag_threshold,
                 max_context_length=GLOBALS.max_context_length,
                 max_new_tokens=GLOBALS.max_new_tokens,
                 n_threads=GLOBALS.n_threads,
                 ):

        set_globals(project_directory, rag_model_path, gpt_model_path, llama_server_path, db_path, rag_difference, rag_threshold, max_context_length, max_new_tokens,
                    n_threads)
        self.globals = GLOBALS
        self.rag_api = RagApi()
        self.gemma_api = GPTServer()  # GemmaApi()
        self.get_instance = Get(rag_api=self.rag_api, gemma_api=self.gemma_api)
        self.new_type = NewType(rag_api=self.rag_api)

    def new_rule_type(self, rule_type) -> bool:
        """
        return True if succeeded, else False
        :param rule_type:
        :return: bool
        """
        try:
            self.new_type.add(rule_type)
            succeeded = True
        except Exception as e:
            succeeded = False

        log_interactions({"succeeded": succeeded, "file upload": rule_type})

        return succeeded

    def get_rule_instance(self, free_text: str) -> dict:
        """
        Processes user input and returns a response with its validation status.

        Args:
            free_text (str): User input text to be processed.

        Returns:
            dict:
                -"rule_instance": desire response,
                -"error": True if error occurs, else False,
                -"free_text": free_text,
                -"type_name": the predicted type name,
                -"rag_score": score of how much we are sure the type name is correct, higher is better.
                -"model_response": the model response before preprocessing.
        """

        start_time = time.time()

        response = {
            "rule_instance": None,
            "is_error": True,
            "error_message": '',
            "free_text": free_text,
            "type_name": None,
            "rag_score": None,
            "model_response": None,
            "schema": None
        }

        if any(char.isalpha() for char in free_text) and len(free_text) > 10:
            try:
                response = self.get_instance.predict(free_text)

            except Exception as e:
                response["error_message"] = f"Processing failed: {type(e).__name__}, {str(e)}"

        else:
            response["error_message"] = f"please enter meaningful text"

        current_time = datetime.now()
        response["time"] = f"{current_time.strftime('%Y-%m-%d')}|{current_time.strftime('%H:%M:%S')}"
        response["inference_time"] = time.time() - start_time
        log_interactions(response)
        return response

    def add_rule_types_from_file(self, json_directory=None):
        if json_directory:
            for file_name in os.listdir(json_directory):
                if file_name.endswith(".json"):
                    if not self.new_rule_type(json_directory + file_name):
                        return f"loading don't complete. error with: {file_name}"
            return True
        return False

    def tweak_rag_parameters(self, rag_threshold=GLOBALS.rag_threshold, rag_difference=GLOBALS.rag_difference):
        GLOBALS.rag_threshold = rag_threshold
        GLOBALS.rag_difference = rag_difference
        return True

    def get_rule_types(self):
        return GLOBALS.db_manager.get_all_types_names()

    def feedback(self, fb):
        log_interactions({"feedback": fb, "time": datetime.now()})
        print("thank you :)")
