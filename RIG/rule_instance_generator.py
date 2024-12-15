import os
import time
from datetime import datetime

from RIG.src.Utils.db_manager import DBManager
from RIG.globals import GLOBALS, MODELS
from RIG.src.App.rule_instance.get import Get
from RIG.src.App.new_type import NewType
from RIG.src.Utils.utils import log_interactions

from RIG.src.Utils.rag_api import RagApi
from RIG.src.Utils.gemma_api import GemmaApi
from RIG.src.Utils.gpt_server import GPTServer

from RIG.rig_evaluate import *
def set_globals(project_directory, rag_model_path, gpt_model_path, llama_server_path, db_file_name, rag_difference, rag_threshold, max_context_length, max_new_tokens,
                n_threads):
    GLOBALS.db_manager = DBManager(project_directory + GLOBALS.db_file_name)
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
                 rule_types_directory=None,
                 db_file_name=GLOBALS.db_file_name,
                 rag_difference=GLOBALS.rag_difference,
                 rag_threshold=GLOBALS.rag_threshold,
                 max_context_length=GLOBALS.max_context_length,
                 max_new_tokens=GLOBALS.max_new_tokens,
                 n_threads=GLOBALS.n_threads,
                 ):
        if project_directory and not project_directory.endswith('/'):
            project_directory += '/'
        set_globals(project_directory, rag_model_path, gpt_model_path, llama_server_path, db_file_name, rag_difference, rag_threshold, max_context_length, max_new_tokens,
                    n_threads)
        self.globals = GLOBALS
        MODELS.rag_api = RagApi()
        self.get_instance = Get()
        self.new_type = NewType()
        if rule_types_directory != "":
            self.add_rule_types_from_folder(rule_types_directory)

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

    def init_gemma_model(
            self,
            max_context_length=GLOBALS.max_context_length,
            max_new_tokens=GLOBALS.max_new_tokens,
            n_threads=GLOBALS.n_threads
    ):
        try:
            GLOBALS.max_context_length = int(max_context_length)
            GLOBALS.max_new_tokens = int(max_new_tokens)
            GLOBALS.n_threads = int(n_threads)
            MODELS.gemma_api = GemmaApi()  # GPTServer()  #
            return True
        except:
            return False


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
        try:
            response["rag_score"] = response["rag_score"].item()
        except:
            pass
        log_interactions(response)
        return response

    def add_rule_types_from_folder(self, rule_types_directory=None):
        try:
            if isinstance(rule_types_directory, str):
                if not rule_types_directory.endswith("/"):
                    rule_types_directory += "/"
                rule_types_loaded = []
                for file_name in os.listdir(rule_types_directory):
                    if file_name.endswith(".json"):
                        rule_types_loaded.append(file_name)
                        if not self.new_rule_type(rule_types_directory + file_name):
                            return f"in  add_rule_types_from_folder, loading don't complete. error with: {file_name}"
                print(f"rule_types_loaded: {rule_types_loaded}")
                return f"rule_types_loaded: {rule_types_loaded}"
        except Exception as e:
            return f"in add_rule_types_from_folder, error occur: {e}"
        return "in add_rule_types_from_folder, no folder provided"

    def tweak_rag_parameters(self, rag_threshold=GLOBALS.rag_threshold, rag_difference=GLOBALS.rag_difference):
        GLOBALS.rag_threshold = rag_threshold
        GLOBALS.rag_difference = rag_difference
        return True

    def get_rule_types_names(self):
        return GLOBALS.db_manager.get_all_types_names()

    def feedback(self, fb: str):
        log_interactions({"feedback": fb, "time": datetime.now()})
        return "thank you :)"

    def evaluate(
        self,
        data_dile_path,
        output_directory,
        start_point=0,
        end_point=2,  # None - all the data
        sleep_time_each_10_iter=30
    ):
        evaluate_func(
            self,
            data_dile_path=data_dile_path,
            output_directory=output_directory,
            start_point=start_point,
            end_point=end_point,  # None - all the data
            sleep_time_each_10=sleep_time_each_10_iter
        )
