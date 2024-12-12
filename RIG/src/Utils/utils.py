import re
import ast
import json
import yaml
from yaml import SafeLoader
import os
import csv
from datetime import datetime
from RIG.globals import GLOBALS,MODELS




def get_dict(input_string):
    # Use regex to find content between { and } that looks like a valid JSON
    input_string = re.sub(r"[\t\n]", "", input_string)
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
            json_str = re.sub(r"(None|null|'None'|\"None\"|'null'|\"null\")", '"null"', json_str)
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

def log_question_and_answer(response):

    """
    Log a question, answer, and its embedding to the log file.
    :param question: The input question.
    :param answer: The corresponding answer.
    """
    rag_api = MODELS.rag_api

    log_dir = os.path.join(GLOBALS.project_directory, 'logs')
    log_file = os.path.join(log_dir, "logs_examples2.csv")

    if not os.path.exists(log_file):
        with open(log_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Question", "Answer", "Embedding","Type_Name"])  # Headers
    question = response["free_text"]
    answer = response["model_response"]
    type_name = response["type_name"]
    embedding_json, embedding = rag_api.get_embedding(question)

    with open(log_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            'id',
            datetime.now().isoformat(),
            question,
            answer,
            embedding_json,
            type_name

        ])
    print(f"Logged question and answer: {question}")
