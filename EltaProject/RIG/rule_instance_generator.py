import time
from datetime import datetime

from RIG.src.Utils.db_manager import DBManager
from RIG.globals import GLOBALS
from RIG.src.App.rule_instance.get import Get
from RIG.src.App.new_type import NewType
from RIG.src.Utils.utils import log_interactions

from RIG.src.Utils.rag_api import RagApi
from RIG.src.Utils.gemma_api import GemmaApi


def set_globals(data_directory, db_file_name, rag_difference, rag_threshold, max_context_length, max_new_tokens, n_threads):
    GLOBALS.db_manager = DBManager(data_directory + db_file_name)
    GLOBALS.models_directory = data_directory
    GLOBALS.rag_difference = rag_difference
    GLOBALS.rag_threshold = rag_threshold
    GLOBALS.max_context_length = max_context_length
    GLOBALS.max_new_tokens = max_new_tokens
    GLOBALS.n_threads = n_threads


class RuleInstanceGenerator:

    def __init__(self,
                 data_directory=GLOBALS.models_directory,
                 db_file_name=GLOBALS.db_file_name,
                 rag_difference=GLOBALS.rag_difference,
                 rag_threshold=GLOBALS.rag_threshold,
                 max_context_length=GLOBALS.max_context_length,
                 max_new_tokens=GLOBALS.max_new_tokens,
                 n_threads=GLOBALS.n_threads,
                 ):

        set_globals(data_directory, db_file_name, rag_difference, rag_threshold, max_context_length, max_new_tokens, n_threads)
        self.globals = GLOBALS
        self.gemma_api = GemmaApi()
        self.rag_api = RagApi()
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

    def get_rule_types(self):
        return GLOBALS.db_manager.get_all_types_names()

    def feedback(self, fb):
        print("thank you :)")
