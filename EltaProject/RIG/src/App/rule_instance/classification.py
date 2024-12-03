from RIG.src.Utils.rag_api import RagApi


class Classification:

    def __init__(self):
        self.rag_api = RagApi()

    def predict(self, query) -> list:
        type_name, closest_distance = self.rag_api.get_closest_type_name(query)
        is_error = False
        if type_name is None:
            is_error = True
        return [type_name, closest_distance, is_error]
