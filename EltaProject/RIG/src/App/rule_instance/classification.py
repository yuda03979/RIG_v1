from typing import Tuple, List, Any

from RIG.globals import GLOBALS


class Classification:

    def __init__(self, rag_api, gemma_api):
        self.rag_api = rag_api
        self.gemma_api = gemma_api

    def predict(self, query) -> tuple[Any, int, bool]:

        # using regex
        type_names, succeed = self.find_rule_name_in_query(query)
        if succeed:
            return type_names[0], -1, False

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
        type_name = None
        type_names_list = self.rag_api.get_closest_type_name(query)
        closest_distance = type_names_list[0][1]
        difference = type_names_list[0][1] - type_names_list[1][1]
        if difference > GLOBALS.rag_difference and difference != float('inf'):  # the case of empty list
            if closest_distance > GLOBALS.rag_threshold:
                print(difference)
                succeed = True
        return type_names_list, succeed

    def ask_model(self, query, type_names):
        print("type name given to gemma")
        schema_a = GLOBALS.db_manager.get_dict_features(type_name=type_names[0][0], feature="schema")
        description_a = GLOBALS.db_manager.get_dict_features(type_name=type_names[0][0], feature="description")

        schema_b = GLOBALS.db_manager.get_dict_features(type_name=type_names[1][0], feature="schema")
        description_b = GLOBALS.db_manager.get_dict_features(type_name=type_names[1][0], feature="description")

        prompt = f"""
        this is the query: 
        {query} <END>
        
        your task is to return ONLY!!! {type_names[0][0]} or {type_names[1][0]}.
        according to which is more simialr to the query.
        
        you also have schema and description for each of them:
        for {type_names[0][0]}:
        - schema: {schema_a}
        - description: {description_a}
        
        for {type_names[1][0]}:
        - schema: {schema_b}
        - description: {description_b}
        
        choose only one!! or {type_names[0][0]} or {type_names[1][0]}:
        Output:
        """
        type_name = self.gemma_api.predict(prompt)
        if type_name in GLOBALS.db_manager.get_all_types_names():
            return type_name, True
        else:
            return f'model didnt generate well: {type_name}', False
