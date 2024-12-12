import os
import csv
import re
import ast
import json
import yaml
import numpy as np
from langchain.chains.constitutional_ai.prompts import examples
from yaml import SafeLoader
from datetime import datetime
from RIG.globals import GLOBALS,MODELS
from datetime import datetime
import pandas as pd



class CreateExamples:
    def __init__(self):
        """
        Initialize the RagHandler with the RAG API and log file.
        :param log_file: The path to the CSV log file.
        """
        self.rag_api = MODELS.rag_api
        self.log_dir = os.path.join(GLOBALS.project_directory, 'logs')
        self.log_file = os.path.join(self.log_dir, "logs_examples.csv")


        # Create the log file if it doesn't exist
        if not os.path.exists(self.log_file):
            with open(self.log_file, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["id","Timestamp", "Question", "Answer", "Embedding","Type_Name"])  # Headers

    def clean_text(self,text):
        """Remove all non-alphanumeric characters and convert to lowercase."""
        return ''.join(char.lower() for char in text if char.isalnum())
    def get_closest_question(self, question, type_name,row_id):
        """
        Find the closest two questions in the log file to the given question.
        :param question: The input question.
        :param type_name: The type name to filter by.
        :return: A dictionary containing the two closest questions, answers, and distances.
        """
        print("id =" +row_id)
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
                
                match = re.search(r'D(\d+)Q', row_id)
                id_dict_qust = match.group(1) if match else None
                
                match = re.search(r'D(\d+)Q', row["id"])
                id_dict_resp = match.group(1) if match else None
                
                # Check if this row is closer than the current closest match
                if distance > closest["distance"] and self.clean_text(type_name)  != self.clean_text(row["Type_Name"]):
                    # Push the current closest to second_closest
                    if distance > second_closest["distance"] and  id_dict_qust != id_dict_resp:
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
                elif distance > second_closest["distance"] and row["id"] != closest["response_id"] and  id_dict_qust != id_dict_resp:
                    
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
        print("examples_1= " + str(examples["example_1"]))
        print("examples_2= " + str(examples["example_2"]))

        return examples

#     def log_question_and_answer(self,row_id, question, answer,type_name):
#         """
#         Log a question, answer, and its embedding to the log file.
#         :param question: The input question.
#         :param answer: The corresponding answer.
#         """
#         embedding_json, embedding = rag_api.get_embedding(question)
# 
#         with open(self.log_file, mode="a", newline="", encoding="utf-8") as file:
#             writer = csv.writer(file)
#             writer.writerow([
#                 row_id,
#                 datetime.now().isoformat(),
#                 question,
#                 answer,
#                 embedding_json,
#                 type_name
# 
#             ])
#         print(f"Logged question and answer: {question}")
# # # Example usage:
# if __name__ == "__main__":
#     # Initialize the RAG API and RagHandler
#     log_file = "questions_data.csv"
#     rag_handler = RagHandler(log_file)
#
#     # Log a new question and answer
#     question = "What is the weather today?"
#     answer = "The weather is sunny with a temperature of 25°C."
#     rag_handler.log_question_and_answer(question, answer)
#
#     # Find the closest question to a new query
#     new_question = "Tell me about the current weather."
#     closest_q, closest_a, score = rag_handler.get_closest_question(new_question)
#     print(f"Closest question: {closest_q}\nAnswer: {closest_a}\nSimilarity: {score}")
# df = pd.read_csv("/home/mefathim/PycharmProjects/llm-app/data_yuda.csv")
# log_file = "questions_data.csv"
# rag_handler = RagHandler(log_file)
#
# def parse_free_text(text):
#     """Parse `free_text` as a list or wrap it in a list if it's plain text."""
#     try:
#         # Try to parse the value as a Python literal
#         parsed_value = ast.literal_eval(text)
#         # Ensure the parsed value is a list
#         if isinstance(parsed_value, list):
#             return parsed_value
#         else:
#             return [parsed_value]
#     except (SyntaxError, ValueError):
#         # If parsing fails, wrap the text in a list
#         return [text.strip()]
#
# # free_text_list = df["free_text","expected_response"].tolist()
# df["expected_response"] = df["expected_response"].apply(ast.literal_eval)  # Convert strings to dictionaries
# df["free_text"] = df["free_text"].apply(parse_free_text)  # Handle plain strings and lists
#
# # Create eval_data_generation from the DataFrame
# free_text_list = [
#     ( row["free_text"],row["expected_response"])
#     for _, row in df.iterrows()
# ]
# for free_text,expected in free_text_list:
#      rag_handler.log_question_and_answer(free_text, expected)
#      print(free_text)
