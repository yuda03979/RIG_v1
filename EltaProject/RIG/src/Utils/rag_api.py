from RIG.globals import GLOBALS
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from RIG.globals import GLOBALS



class RagModel:
    def __init__(self):
        self.model_name = "BAAI/bge-m3"
        self.model = SentenceTransformer(self.model_name, trust_remote_code=True, cache_folder=GLOBALS.models_directory)

    def get_embedding(self, text: str):
        embedding = self.model.encode(text, padding=True, truncation=True)
        return embedding


class RagApi:
    def __init__(self):
        self.db_manager = GLOBALS.db_manager
        self.rag_model = RagModel()
        self.rule_types_embedding = self.init_rule_types_embeddings()

    def init_rule_types_embeddings(self):
        rule_types_embeddings = {}
        # Example database of rule types
        for type_name in self.db_manager.get_all_types_names():
            rule_types_embeddings[type_name] = np.array(self.db_manager.get_embedding(type_name))
        return rule_types_embeddings

    def add_rule_type_embedding(self, type_name, embedding):
        self.rule_types_embedding[type_name] = embedding

    def get_embedding(self, text):
        embedding = self.rag_model.get_embedding(text=text)
        embedding_json = json.dumps(embedding.tolist())
        return embedding_json, embedding

    def get_closest_type_name(self, query: str):
        """
        Classifies a free-form query to the closest rule_type.
        :param query: The free-text
        :return: The closest type_name
        """
        query_embedding = self.rag_model.get_embedding(text=query)

        types_names_resault = {k: -float("inf") for k in self.rule_types_embedding.keys()}

        for type_name in self.rule_types_embedding.keys():
            embedding = self.rule_types_embedding[type_name]
            distance = query_embedding @ embedding.T
            types_names_resault[type_name] = distance

        types_names_resault_list = sorted(types_names_resault.items(), key=lambda item: item[1], reverse=True)

        types_names_resault_list.append(('None', 0))
        types_names_resault_list.append(('None', -float('inf')))

        return types_names_resault_list[:2]
