import os
import csv
import re
import ast
import json
import yaml
import numpy as np
from yaml import SafeLoader
from datetime import datetime
from RIG.globals import GLOBALS,MODELS
from datetime import datetime
import pandas as pd



class CreateExamples:
    def __init__(self):
        """
        Initialize the CreateExamples with the RAG API and log file.
        :param log_file: The path to the CSV log file.
        """
        self.rag_api = MODELS.rag_api
        self.log_dir = os.path.join(GLOBALS.project_directory, 'logs')
        self.log_file = os.path.join(self.log_dir,"logs_examples5.csv")


    def clean_text(self,text):
        """Remove all non-alphanumeric characters and convert to lowercase."""
        return ''.join(char.lower() for char in text if char.isalnum())


    def get_closest_question(self, question, type_name, row_id = None):
        """
        Find the closest two questions in the log file to the given question.
        :return: A dictionary containing the two closest questions, answers, and distances.
        """
        print("id =",row_id)
        if not os.path.exists(self.log_file) or os.stat(self.log_file).st_size == 0:
            print("Log file is empty or does not exist.")
            return {"example_1": {"free_text":None}, "example_2": {"free_text":None}}

        # Generate embedding for the input question
        _, query_embedding = self.rag_api.get_embedding(question)

        # Initialize placeholders for the top two closest matches
        closest = {"distance": -float("inf"), "free_text": None, "response": None, "response_id": None, "type_name": None}
        second_closest = {"distance": -float("inf"), "free_text": None, "response": None, "response_id": None,
                          "type_name": None}

        # Read the log file and calculate similarity
        with open(self.log_file, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                logged_embedding = np.array(json.loads(row["Embedding"]))
                distance = query_embedding @ logged_embedding.T
                if row_id:
                    match = re.search(r'D(\d+)Q', row_id)
                    id_dict_qust = match.group(1) if match else None

                    match = re.search(r'D(\d+)Q', row["id"])
                    id_dict_resp = match.group(1) if match else None
                
                # Check if this row is closer than the current closest match
                if distance > closest["distance"] and self.clean_text(type_name)  != self.clean_text(row["Type_Name"]):
                    if distance > second_closest["distance"]:
                        if row_id:
                            match = re.search(r'D(\d+)Q', row_id)
                            id_dict_qust = match.group(1) if match else None

                            match = re.search(r'D(\d+)Q', row["id"])
                            id_dict_resp = match.group(1) if match else None
                            if id_dict_qust != id_dict_resp:
                                second_closest = closest.copy()
                        else:
                            second_closest = closest.copy()

                    # Update closest with the new closest match
                    closest = {
                        "distance": distance,
                        "free_text": row["Question"],
                        "response": row["Answer"],
                        "response_id": row["id"],
                        "type_name": row["Type_Name"],
                    }
                # Check if this row is closer than the current second_closest
                elif distance > second_closest["distance"] and row["id"] != closest["response_id"] and id_dict_qust != id_dict_resp if row_id else True:

                    second_closest = {
                        "distance": distance,
                        "free_text": row["Question"],
                        "response": row["Answer"],
                        "response_id": row["id"],
                        "type_name": row["Type_Name"],
                    }
        # Prepare the output examples
        examples = {
            "example_1": closest,
            "example_2": second_closest,
        }
        print(examples)
        return examples

