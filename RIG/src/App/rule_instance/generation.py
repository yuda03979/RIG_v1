from RIG.src.Utils.prompts import prompt_json_gemma_v6
from RIG.src.Utils.utils import get_dict
from RIG.globals import GLOBALS, MODELS


class Generation:

    def __init__(self):
        self.db_manager = GLOBALS.db_manager

    def predict(self, type_name, free_text):
        schema = self.db_manager.get_dict_features(type_name=type_name, feature="schema")
        description = self.db_manager.get_dict_features(type_name=type_name, feature="description")
        response = MODELS.gemma_api.predict(prompt=prompt_json_gemma_v6(free_text, type_name, schema, description))
        return response, schema

