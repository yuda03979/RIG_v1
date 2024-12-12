from RIG.globals import GLOBALS
import pandas as pd

def clean_text(text):
    """Remove all non-alphanumeric characters and convert to lowercase."""
    return ''.join(char.lower() for char in text if char.isalnum())

def prompt_json_gemma_v1(free_text, type_name, schema, description):
    prompt = f"""
    You are a helpful assistant trained to extract information from free text and format it to match a JSON schema. Your task is to fill out the given JSON schema with the corresponding values from the provided free text. If a field in the schema is not mentioned in the text, use "null". Follow this format strictly.

    Example:
    Free text:

    "Please generate a Weather Alert - other for area code 2001. Alert type is Thunderstorm. Intensity: severe. Urgency: high. Ignore the forecast source for now. Add short desc: Heavy winds and lightning expected. Duration in hours: 6."
    Schema:
    {{
    "alertType": "string",
    "areaCode": "int",
    "intensity": "string",
    "urgency": "string",
    "forecastSource": "string",
    "description": "string",
    "duration": "int"
    "ruleInstanceName": "str"
    "severity": "int"
    }}

    Output:
    {{
    "alertType": "Thunderstorm",
    "areaCode": 2001,
    "intensity": "severe",
    "urgency": "high",
    "forecastSource": "null",
    "description": "Heavy winds and lightning expected. ",
    "duration": 6,
    "ruleInstanceName": "Weather Alert - other"
    "severity": "null"
    }}
    Now, perform the task for the following:

    Free text:
    {free_text}

    Schema:
    {schema}

    you also got context for the fields to help you - dont fill that: {description}
    Output:
    """
    return prompt


def prompt_json_gemma_v1_b(free_text, type_name, schema, description):
    prompt = f"""
    You are a helpful assistant trained to extract information from free text and format it to match a JSON schema. Your task is to fill out the given JSON schema with the corresponding values from the provided free text. If a field in the schema is not mentioned in the text, use "null". Follow this format strictly.

    Example 1:
    - Free text: 
    "Please generate a Weather Alert - other for area code 2001. Alert type is Thunderstorm. Intensity: severe. Urgency: high. Ignore the forecast source for now. Add short desc: Heavy winds and lightning expected. The duration of this case, I'd say, is around two."
    - Schema:
    {{
        "alertType": "string",
        "areaCode": "int",
        "intensity": "string",
        "urgency": "string",
        "forecastSource": "string",
        "description": "string",
        "duration": "int",
        "ruleInstanceName": "string",
        "severity": "int"
    }}
    - Output:
    {{
        "alertType": "Thunderstorm",
        "areaCode": 2001,
        "intensity": "severe",
        "urgency": "high",
        "forecastSource": "null",
        "description": "Heavy winds and lightning expected.",
        "duration": 2,
        "ruleInstanceName": "Weather Alert - other",
        "severity": "null"
    }}
    Example 2: 
    - Free text: 
     "Add a report for 'Shell Delay'. Equipment Malfunction case. Type: shell. Site is not important. Malfunction at level five, urgency four. Description: Detonation delayed. Severity am i think 3.",
    - Schema:
    {{
        "type": "string",
        "site": "string",
        "malfunctionLevel": "int",
        "urgency": "int",
        "description": " string",
        "ruleInstanceName": "string",
        "severity": "int",
    }}

    - Output:
    {{
        "type": "shell",
        "site": "empty",
        "malfunctionLevel": 5,
        "urgency": 4,
        "description": "Detonation delayed",
        "ruleInstanceName": "Equipment Malfunction - Shell Delay",
        "severity": 3,
    }}
    Now, perform the task for the following:

    Free text:
    {free_text}

    Schema:
    {schema}

    you also got context for the fields to help you - dont fill that: {description}
    Output:
    """
    return prompt


def prompt_yaml_gemma(free_text, type_name, schema, description):
    prompt = f"""
    You are a helpful assistant trained to extract information from free text and format it to match a JSON schema. Your task is to fill out the given JSON schema with the corresponding values from the provided free text. If a field in the schema is not mentioned in the text, use "null". return it as YAML. Follow this format strictly.

    Example:
    Free text:

    "Please generate a Weather Alert - other for area code 2001. Alert type is Thunderstorm. Intensity: severe. Urgency: high. Ignore the forecast source for now. Add short desc: Heavy winds and lightning expected. Duration in hours: 6."
    Schema:
    {{
    "alertType": "string",
    "areaCode": "int",
    "intensity": "string",
    "urgency": "string",
    "forecastSource": "string",
    "description": "string",
    "duration": "int"
    "ruleInstanceName": "str"
    }}

    Output:
    ---
alertType: Thunderstorm
areaCode: 2001
intensity: severe
urgency: high
forecastSource: 'null'
description: 'Heavy winds and lightning expected. '
duration: 6
ruleInstanceName: Weather Alert - other

    Now, perform the task for the following:

    Free text:
    {free_text}

    Schema:
    {schema}

    you also got context for the fields to help you - dont fill that: {description}
    Output:
    """
    return prompt


def prompt_json_gemma_v2(free_text, type_name, schema, description):
    prompt = f"""
    You are a helpful assistant trained to extract information from free text and format it to match a JSON schema. Your task is to fill out the given JSON schema with the corresponding values from the provided free text. If a field in the schema is not mentioned in the text, use "null". Follow this format strictly.

    Example:
    - Free text:

    "Please generate a Weather Alert - other for area code 2001. Alert type is Thunderstorm. Intensity: severe. Urgency: high. Ignore the forecast source for now. Add short desc: Heavy winds and lightning expected. The duration of this case, I'd say, is around a of two"
    - Schema:
    {{
    "alertType": "string",
    "areaCode": "int",
    "intensity": "string",
    "urgency": "string",
    "forecastSource": "string",
    "description": "string",
    "duration": "int"
    "ruleInstanceName": "str"
    "severity": "int"
    }}

    - Output:
    {{
    "alertType": "Thunderstorm",
    "areaCode": 2001,
    "intensity": "severe",
    "urgency": "high",
    "forecastSource": "null",
    "description": "Heavy winds and lightning expected. ",
    "duration": 6,
    "ruleInstanceName": "Weather Alert - other"
    "severity": "null"
    }}
    Now, perform the task for the following:

    - Free text:
    {free_text}

    - Schema:
    {schema}

    you also got context for the fields to help you - dont fill that: {description}
    - Output:
    """
    return prompt


def prompt_json_gemma_v3(free_text, type_name, schema, description):
    """
    from cloude
    """
    prompt = f"""
    Task: Extract structured information from free text and format it precisely to match the given JSON schema.

    Instructions:
    1. Carefully read the entire free text
    2. Map values exactly to the corresponding schema fields
    3. If a field is not present in the text, use "null"
    4. Ensure type consistency (convert to correct type as specified in schema)
    5. Be precise and concise in value extraction

    Schema Details:
    {schema}

    Additional Context (DO NOT include in output):
    {description}

    Example Conversion:
    - Input Text: "Please generate a Weather Alert - other for area code 2001. Alert type is Thunderstorm. Intensity: severe. Urgency: high. Ignore the forecast source for now. Add short desc: Heavy winds and lightning expected. The duration of this case, I'd say, is around a of two"
    - Schema: 
    {{
        "alertType": "string",
        "areaCode": "int",
        "intensity": "string",
        "urgency": "string",
        "forecastSource": "string",
        "description": "string",
        "duration": "int",
        "ruleInstanceName": "str",
        "severity": "int"
    }}
    - Output:
    {{
        "alertType": "Thunderstorm",
        "areaCode": 2001,
        "intensity": "severe",
        "urgency": "high",
        "forecastSource": null,
        "description": "Heavy winds and lightning expected.",
        "duration": 2,
        "ruleInstanceName": "Weather Alert - other",
        "severity": null
    }}

    Current Input Text:
    {free_text}

    Provide the JSON output following the schema precisely:
    """
    return prompt


def prompt_json_gemma_v4(free_text, type_name, schema, description):
    """
    from chat gpt
    """
    prompt = f"""
    Extract information from the provided text and format it according to the given JSON schema. If a field is not mentioned in the text, set its value to "null". Follow the schema exactly.

    Example:
    - Free text: 
    "Please generate a Weather Alert - other for area code 2001. Alert type is Thunderstorm. Intensity: severe. Urgency: high. Ignore the forecast source for now. Add short desc: Heavy winds and lightning expected. The duration of this case, I'd say, is around two."
    - Schema:
    {{
        "alertType": "string",
        "areaCode": "int",
        "intensity": "string",
        "urgency": "string",
        "forecastSource": "string",
        "description": "string",
        "duration": "int",
        "ruleInstanceName": "string",
        "severity": "int"
    }}
    - Output:
    {{
        "alertType": "Thunderstorm",
        "areaCode": 2001,
        "intensity": "severe",
        "urgency": "high",
        "forecastSource": "null",
        "description": "Heavy winds and lightning expected.",
        "duration": 2,
        "ruleInstanceName": "Weather Alert - other",
        "severity": "null"
    }}

    Now process this input:
    - Free text: {free_text}
    - Schema: {schema}
    - Context for fields (do not fill): {description}
    - Output:
    """
    return prompt


def prompt_json_gemma_v5(free_text, type_name, schema, description ,examples = None):
    """
    from chat gpt
    """
    if  not examples: 
        examples ="""
        xample 1:
        - Free text: 
        "Please generate a Weather Alert - other for area code 2001. Alert type is Thunderstorm. Intensity: severe. Urgency: high. Ignore the forecast source for now. The duration of this case, I'd say, is around two. severity is empty or unclear"
        - Schema:
        {{
            "alertType": "string",
            "areaCode": "int",
            "intensity": "string",
            "urgency": "string",
            "forecastSource": "string",
            "duration": "int",
            "ruleInstanceName": "string",
            "severity": "int"
        }}
            "ruleInstanceName" field should be: "Weather Alert - ?". ? length should be about 1-3 words.
        
        - Output:
        {{"alertType": "Thunderstorm","areaCode": 2001,"intensity": "severe","urgency": "high","forecastSource": "null","duration": 2,"ruleInstanceName": "Weather Alert - other","severity": "null"}}
        
        Example 2:
        
        - Free text: 
         "Add a report for 'Shell Delay'. Equipment Malfunction case. Type: shell. Site is not important. Malfunction at level five, urgency four. Desc: Detonation delayed in poland Severity i think 3.",
        - Schema:
        {{
            "type": "string",
            "site": "string",
            "malfunctionLevel": "int",
            "urgency": "int",
            "description": " string",
            "ruleInstanceName": "string",
            "severity": "int"
        }}
        "ruleInstanceName" field should be: "Equipment Malfunction - ?". ? length should be about 1-3 words.
    
        - Output:
        {{"type": "shell","site": "empty","malfunctionLevel": 5,"urgency": 4,"description": "Detonation delayed in poland","ruleInstanceName": "Equipment Malfunction - Shell Delay","severity": 3}}
      """
        # closest_question_2
        # ":closest_question_2,
        # "closest_answer_2": closest_answer_2,
        # "closest_distance_2": closest_distance_2,
        # "response_id_2": response_id_2,
        # "type_name_2": type_name_2}
    else:
        example_free_text_1 = examples["example_1"]["free_text"]
        df = GLOBALS.db_manager.get_df()

        example_schema_1 = df.loc[
            df["type_name"].apply(clean_text) == clean_text(examples["example_1"]["type_name"]), "schema"
        ].values[0]
        print(example_schema_1)

        example_output_1 = str(examples["example_1"]["response"])

        example_free_text_2 = examples["example_2"]["free_text"]
        example_schema_2 = df.loc[
            df["type_name"].apply(clean_text) == clean_text(examples["example_2"]["type_name"]), "schema"
        ].values[0]
        example_output_2 = str(examples["example_2"]["response"])

        examples = f"""
         Example 1:
        - Free text:
         {example_free_text_1}
        - Schema:
        {example_schema_1}
        - Output:
        {example_output_1}
        Example 2:
        - Free text:
        {example_free_text_2}
        - Schema:
        {example_schema_2}
        - Output:
        {example_output_2}
            
        """

        
    prompt = f"""
    Extract information from the provided text and format it according to the given JSON schema. If a field is not mentioned in the text, set its value to "null" (with quotes). Follow the schema exactly.
    
    {examples}

    
    (The severity parameter means the severity level of the alert)
    
    
    Now process this input:
    - Free text: {free_text}
    - Schema: {schema}
    "ruleInstanceName" field should be: "{type_name} - ?". ? length should be about 1-3 words.
    - Context for fields (do not fill): {description}
    - Output:
    """
    print('prompt = '+ prompt)
    return prompt
