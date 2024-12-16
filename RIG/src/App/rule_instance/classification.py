from typing import Tuple, List, Any
from RIG.src.Utils.utils import get_dict
from RIG.globals import GLOBALS, MODELS
from RIG.src.Utils.prompts import rag_query_prompt

class Classification:

    def __init__(self):
        pass

    def predict(self, query) -> tuple[Any, int, bool]:

        # # using regex
        # type_names, succeed = self.find_rule_name_in_query(query)
        # if succeed:
        #     return type_names[0], -1, False

        # using rag:
        type_names_list, succeed = self.using_rag(query)
        if succeed:
            return type_names_list[0][0], type_names_list[0][1], False

        # using llm
        type_name, succeed = self.ask_model(query, type_names_list)
        if succeed:
            return type_name, -2, False

        # failed
        return type_name, -3, True

    def find_rule_name_in_query(self, query) -> tuple[list[Any], bool]:
        """
        (regex search) - searching in the string matchhing between any rulu_type_nameto the query
        :param query:
        :return:
        """
        def clean_text(text):
            """Remove all non-alphanumeric characters and convert to lowercase."""
            return ''.join(char.lower() for char in text if char.isalnum())

        rule_names_list = GLOBALS.db_manager.get_all_types_names()
        results = []
        for type_name in rule_names_list:
            if clean_text(type_name) in clean_text(query):
                results.append(type_name.lower())

        if len(results) == 1:
            return [results[0]], True
        else:
            return results, False

    def using_rag(self, query):
        succeed = False
        type_names_list = MODELS.rag_api.get_closest_type_name(rag_query_prompt + query) #
        closest_distance = type_names_list[0][1]
        difference = type_names_list[0][1] - type_names_list[1][1]
        if difference > GLOBALS.rag_difference and difference != float('inf'):  # the case of empty list
            if closest_distance > GLOBALS.rag_threshold:
                succeed = True
        if type_names_list[0][0] != 'None' and type_names_list[1][0] == 'None':  # in case of one type name
            succeed = True
        return type_names_list, succeed

    def ask_model(self, query, type_names):
        schema_a = GLOBALS.db_manager.get_dict_features(type_name=type_names[0][0], feature="schema")
        description_a = GLOBALS.db_manager.get_dict_features(type_name=type_names[0][0], feature="description")

        schema_b = GLOBALS.db_manager.get_dict_features(type_name=type_names[1][0], feature="schema")
        description_b = GLOBALS.db_manager.get_dict_features(type_name=type_names[1][0], feature="description")

        prompt = f"""
        Analyze the following query:  
{query} <END>

Based on the query, choose which type is a better match from the two options provided. Use the schema and description as context for your decision.  

Option 1:  
- Name: {type_names[0][0]}  
- Schema: {schema_a}  
- Description: {description_a}  

Option 2:  
- Name: {type_names[1][0]}  
- Schema: {schema_b}  
- Description: {description_b}  

You must return ONLY ONE: either {{"type_name": {type_names[0][0]}}} or {{"type_name": {type_names[1][0]}}}.  

Note: it must be in json form!
Example of expected output:  
{{"type_name": "Hay_field"}}  

Actual output:
        """
        type_name = get_dict(MODELS.gemma_api.predict(prompt) + '}')[0]
        try:
            if type_name["type_name"] in GLOBALS.db_manager.get_all_types_names():
                return type_name["type_name"], True
        except:
            return f'model didnt generate well: {str(type_name)}', False
