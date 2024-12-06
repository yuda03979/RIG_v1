from RIG.src.Utils.utils import get_dict

from .classification import Classification
from .generation import Generation
from .post_processing import post_processing
from RIG.globals import GLOBALS



class Get:

    def __init__(self):
        self.classifier = Classification()
        self.generator = Generation()

    def predict(self, free_text):

        response = {
            "rule_instance": None,
            "is_error": True,
            "error_message": "",
            "free_text": free_text,
            "type_name": None,
            "rag_score": None,
            "model_response": None,
            "schema": None
        }

        response["type_name"], response["rag_score"], is_error = self.classifier.predict(free_text)
        if is_error:
            response["error_message"] = "error! can't identify ruleType. no ruleType exist or didnt pass the threshold."
            return response

        response["model_response"], response["schema"] = self.generator.predict(response["type_name"], free_text)
        model_response, succeed = get_dict(response["model_response"])
        if not succeed:
            response["error_message"] = "error! can't extract json from model response"
            return response

        response["rule_instance"] = post_processing(response["type_name"], model_response)
        response["is_error"] = False
        return response

