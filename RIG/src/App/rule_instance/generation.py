from RIG.src.Utils.prompts import prompt_json_gemma_v1_b, prompt_json_gemma_v5
from RIG.src.Utils.utils import get_dict
from RIG.src.Utils.caeate_examples_eval import CreateExamples
from RIG.globals import GLOBALS, MODELS


class Generation:

    def __init__(self):
        self.db_manager = GLOBALS.db_manager
        self.create_examples = CreateExamples()

    def predict(self, type_name, free_text,row_id = 'id'):
        schema = self.db_manager.get_dict_features(type_name=type_name, feature="schema")
        print(type_name)
        description = self.db_manager.get_dict_features(type_name=type_name, feature="description")
        examples = self.create_examples.get_closest_question(question = free_text, type_name=type_name,row_id = row_id)
        # print("is axameles " +axameles)
        response = MODELS.gemma_api.predict(prompt=prompt_json_gemma_v5(free_text, type_name, schema, description, examples))
        return response, schema,examples

