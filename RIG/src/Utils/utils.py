import re
import ast
import json
import yaml
from yaml import SafeLoader
import os
import csv
from datetime import datetime
from RIG.globals import GLOBALS




def get_dict(input_string):
    # Use regex to find content between { and } that looks like a valid JSON
    match = re.search(r'\{[^}]*\}', input_string)

    if not match:
        return input_string, False

    json_str = match.group(0)

    try:
        # First, try standard JSON parsing
        parsed_dict = json.loads(json_str)
        return parsed_dict, True
    except json.JSONDecodeError:
        # If standard parsing fails, try some custom parsing
        try:
            # Replace 'null' strings with actual None
            json_str = json_str.replace("'", '"')
            json_str = json_str.replace('null', '"null"')
            json_str = json_str.replace('None', '"null"')
            json_str = json_str.replace('"None"', '"null"')
            # Use ast for more flexible parsing
            import ast
            parsed_dict = ast.literal_eval(json_str)
            return parsed_dict, True
        except (SyntaxError, ValueError):
            return input_string, False


def json_from_yaml(yaml_doc):
    dict_doc = yaml.load(yaml_doc, Loader=SafeLoader)
    return dict_doc


def yaml_from_json(json_doc):
    yaml_doc = yaml.dump(json_doc, default_flow_style=False)
    return yaml_doc


def log_interactions(response):
    # create hidde logs directory if it doesn't exist
    log_dir = os.path.join(GLOBALS.project_directory, '.logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = os.path.join(log_dir, "logs.csv")
    # check if file exists, if not create it with headers
    file_exists = os.path.isfile(log_file)
    current_time = datetime.now()
    with open(log_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # add headers for new file
        if not file_exists:
            writer.writerow(['Date', 'Time', 'Output'])

        # write new row
        writer.writerow([
            current_time.strftime('%Y-%m-%d'),
            current_time.strftime('%H:%M:%S'),
            str(response)
        ])
