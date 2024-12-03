from RIG.globals import GLOBALS
from RIG.src.Utils.utils import normalize_empty_value

def post_processing(type_name, model_response):
    model_response = {k: normalize_empty_value(v) for k, v in model_response.items()}
    default_rule_instance = GLOBALS.db_manager.get_dict_features(type_name, 'default_rule_instance')
    for param in [k for k in model_response.keys() if  # or: default_rule_instance['params'].keys()
                  k not in ["severity", "ruleInstanceName", "ruleInstanceName".lower()]]:
        default_rule_instance['params'][param] = model_response[param]
    for param in [k for k in model_response.keys() if  # or: default_rule_instance['params'].keys()
                  k in ["severity", "ruleInstanceName", "ruleInstanceName".lower()]]:
        default_rule_instance[param] = model_response[param]
    return default_rule_instance
