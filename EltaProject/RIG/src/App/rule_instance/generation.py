from RIG.src.Utils.prompts import prompt_json_gemma_v1_b, prompt_json_gemma_v5
from RIG.src.Utils.utils import get_dict
from RIG.globals import GLOBALS


class Generation:

    def __init__(self, gemma_api):
        self.gemma_api = gemma_api
        self.db_manager = GLOBALS.db_manager

    def predict(self, type_name, free_text):
        schema = self.db_manager.get_dict_features(type_name=type_name, feature="schema")
        description = self.db_manager.get_dict_features(type_name=type_name, feature="description")
        response = self.gemma_api.predict(prompt_json_gemma_v5(free_text, type_name, schema, description))
        return response + '}', schema

