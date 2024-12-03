from RIG.src.Utils.gemma_api import GemmaApi
from RIG.src.Utils.prompts import prompt_json_gemma_v3
from RIG.src.Utils.utils import get_dict
from RIG.globals import GLOBALS


class Generation:

    def __init__(self):
        self.gemma_api = GemmaApi()
        self.db_manager = GLOBALS.db_manager

    def predict(self, type_name, free_text):

        schema = self.db_manager.get_dict_features(type_name=type_name, feature="schema")
        description = self.db_manager.get_dict_features(type_name=type_name, feature="description")
        response = self.gemma_api.predict(prompt_json_gemma_v3(free_text, type_name, schema, description))
        return response + '}', schema

