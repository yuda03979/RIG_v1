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