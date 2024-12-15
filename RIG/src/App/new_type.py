import json
import os

from RIG.globals import GLOBALS, MODELS


class NewType:

    def __init__(self):
        self.db_manager = GLOBALS.db_manager

    def add(self, json_input) -> None:
        """
        :param json_input: file.json or dict.
        :return: None
        """
        if isinstance(json_input, dict):
            rule_type = json_input
        else:
            try:
                # Check if the input is a file path
                if json_input.endswith('.json') and os.path.isfile(json_input):
                    with open(json_input, 'r') as file:
                        rule_type_json = file.read()
                    rule_type = json.loads(rule_type_json)
            except (IOError, json.JSONDecodeError) as e:
                raise ValueError(
                    f"Please load file.json or dict, and make sure it's in correct rule type format. Error: {str(e)}")

        type_name = rule_type['name'].lower()
        schema = self.create_schema(rule_type)
        description = self.create_description(rule_type)
        default_values = self.create_default_values(rule_type)
        default_rule_instance = self.create_default_rule_instance(rule_type, default_values)
        embedding = self.create_embedding(type_name, schema)

        self.db_manager.write_new_type(str(type_name),
                                       str(schema),
                                       str(description),
                                       str(default_values),
                                       str(default_rule_instance),
                                       str(rule_type),
                                       str(embedding))

    def create_schema(self, rule_type) -> dict:
        schema = {}
        for param in rule_type["parameters"]:
            schema[param["name"]] = str(param["type"])
        schema['ruleInstanceName'] = "string"
        schema['severity'] = "int"
        return schema

    def create_description(self, rule_type) -> dict:
        description = {}
        for param in rule_type["parameters"]:
            description[param["name"] + "_description"] = str(param["description"])
        description['ruleInstanceName_description'] = "about what the message and to what it related in the db."
        description['severity_description'] = "level of importance, criticality, or risk."
        description["event details"] = {}
        description["event details"]["global description"] = str(rule_type["description"])
        description["event details"]["object name"] = rule_type["eventDetails"][0]["objectName"]
        return description

    def create_default_values(self, rule_type) -> dict:
        """ assuming severity and ruleInstanceName default values"""
        default_values = {}
        for param in rule_type["parameters"]:
            default_values[param["name"]] = str(param["defaultValue"])
        return default_values

    # rule_type["description"]
    def create_default_rule_instance(self, rule_type, default_values) -> dict:
        rule_instance = {
            "_id": "00000000-0000-0000-0000-000000000000",  # Sample ID
            "description": "string",
            "isActive": True,
            "lastUpdateTime": "00/00/0000 00:00:00",
            "params": default_values,
            "ruleInstanceName": '',
            "severity": '',
            "ruleType": rule_type['logicType'],
            "ruleOwner": "",
            "ruleTypeId": rule_type["_id"],
            "eventDetails": rule_type["eventDetails"],
            "additionalInformation": rule_type['additionalInformation'],
            "presetId": "00000000-0000-0000-0000-000000000000"
        }
        return rule_instance

    def create_embedding(self, type_name, schema) -> str:
        embedding_words = str(schema) + str(type_name)
        embedding_json, embedding = MODELS.rag_api.get_embedding(str(embedding_words))
        MODELS.rag_api.add_rule_type_embedding(type_name, embedding)
        return str(embedding_json)
