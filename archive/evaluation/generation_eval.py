import os
import tqdm
import pandas as pd
import ast
import time
import json
from RIG import RuleInstanceGenerator

# Initialize the rule instance generator
rig = RuleInstanceGenerator()

folder_path = "data/rule_types/"
for file_name in os.listdir(folder_path):
    if file_name.endswith(".json"):
        print(rig.new_rule_type(folder_path + file_name))

csv_path = "data/data_yuda.csv"
df_eval = pd.read_csv(csv_path)


# Helper function to parse `free_text`
def parse_free_text(text):
    """Parse `free_text` as a list or wrap it in a list if it's plain text."""
    try:
        # Try to parse the value as a Python literal
        parsed_value = ast.literal_eval(text)
        # Ensure the parsed value is a list
        if isinstance(parsed_value, list):
            return parsed_value
        else:
            return [parsed_value]
    except (SyntaxError, ValueError):
        # If parsing fails, wrap the text in a list
        return [text.strip()]


# Parse `excepted_response` and `free_text`
df_eval["expected_response"] = df_eval["expected_response"].apply(ast.literal_eval)  # Convert strings to dictionaries
df_eval["free_text"] = df_eval["free_text"].apply(parse_free_text)  # Handle plain strings and lists

# Create eval_data_generation from the DataFrame
eval_data_generation = [
    (row["id"], row["rule_types_names"], row["expected_response"], row["free_text"])
    for _, row in df_eval.iterrows()
]


# Helper Functions
def lower_values(expected, response):
    """Normalize values to lowercase for comparison."""
    for k in expected.keys():
        expected[k] = str(expected[k]).lower()
    for k in response.keys():
        response[k] = str(response[k]).lower()
    return expected, response


def correct_prediction(expected, response):
    """Prepare expected and response for comparison."""
    return lower_values(expected, response)


def clean_text(text):
    """Remove all non-alphanumeric characters and convert to lowercase."""
    return ''.join(char.lower() for char in text if char.isalnum())


def predict(free_text):
    """Predict rule instance using the rig."""
    model_response = rig.get_rule_instance(free_text)
    if model_response["is_error"] == True:
        print("error: ", model_response)
        return False, False
    rule_instance = model_response["rule_instance"]
    response = rule_instance["params"]
    response["ruleInstanceName"] = rule_instance["ruleInstanceName"]
    response["severity"] = rule_instance["severity"]
    return response, model_response


# def normalize_empty_value(value):
#     """Normalize empty values to a common representation."""
#     if value in [None, "", "null", "None", "none", "empty"] or (isinstance(value, float) and pd.isna(value)):
#         return "EMPTY"
#     return value
#
def normalize_empty_value(value):
    """Normalize empty values to a common representation."""
    if value in [None, '', ' ', " ", "", "null", "None", "none", "empty"] + ["int", "Int", "String", "string"]:
        return "null"  # Choose a common representation for empty values
    return value

def normalize_values(dictionary):
    """Normalize all values in the dictionary."""
    return {k: normalize_empty_value(v) for k, v in dictionary.items()}


def score_param_type(expected, response, numerical=True):
    """Generic binary score for numerical or verbal parameters."""
    if numerical:
        # Filter numerical values
        bin_expected = {k: v for k, v in expected.items() if is_numerical(v)}
        bin_response = {k: v for k, v in response.items() if is_numerical(v)}
    else:
        # Filter verbal (non-numerical) values
        bin_expected = {k: v for k, v in expected.items() if not is_numerical(v) and k != "ruleInstanceName"}
        bin_response = {k: v for k, v in response.items() if not is_numerical(v) and k != "ruleInstanceName"}
    return int(bin_response == bin_expected)


def is_numerical(value):
    """Check if a value is numerical."""
    try:
        float(value)
        return True
    except ValueError:
        return False


def score_param_type_avg(expected, response, numerical=True):
    """Evaluate average score for verbal (non-numerical) parameters."""
    # Extract verbal (non-numerical) values from expected and response
    if numerical:
        # Filter numerical values
        verbal_keys = [k for k, v in expected.items() if is_numerical(v)]
    else:
        verbal_keys = [k for k, v in expected.items() if
                       not is_numerical(v) and k.lower() != "ruleInstanceName".lower()]

    score = 0

    for k in verbal_keys:
        normalized_expected = normalize_empty_value(expected[k])
        normalized_response = normalize_empty_value(response.get(k, None))
        if normalized_expected == normalized_response:
            score += 1

    return score / len(verbal_keys) if verbal_keys else 0


def score_rule_instance_name(expected, response):
    """Evaluate the correctness of 'ruleInstanceName'."""
    return int(expected["ruleInstanceName"] == response["ruleInstanceName"])


# Helper function to collect errors for each scoring type
def collect_error_data(param_name, id, expected, response, free_text, difference):
    """Helper function to create error data entry."""
    return {
        "param_name": param_name,
        "id":id,
        "expected": expected,
        "response": response,
        "free_text": free_text,
        "errors":difference
    }

def score_binary(expected, response):
    for k, expected_v in expected.items():
        try:
            if normalize_empty_value(response[k]) != normalize_empty_value(expected_v):
                return 0
        except:
            return 0
    return 1


def find_differences(expected, response):
    """
    Find differences between the expected and response dictionaries.
    """
    differences = {
        "mismatched_keys": {},
        "missing_keys": [],
        "extra_keys": []
    }
    expected = normalize_values(expected)
    response = normalize_values(response)

    for key in expected:
        if key in response and expected[key] != response[key]:
            differences["mismatched_keys"][key] = {"expected": expected[key], "response": response[key]}
    differences["missing_keys"] = [key for key in expected if key not in response]
    differences["extra_keys"] = [key for key in response if key not in expected]

    return differences



error_df_param_numerical_binary_score = []
error_df_param_verbal_binary_score = []
error_df_rule_name_score = []


# Evaluation Function
def evaluate():
    rows = []
    for i, (row_id, type_name, expected, free_text_list) in tqdm.tqdm(enumerate(eval_data_generation[::3]), total=len(eval_data_generation[::3])):
        if not i % 10:
            time.sleep(20)
        for free_text in free_text_list:
            # print(free_text)
            if not free_text.strip():
                print("Skipping empty free_text")
                continue

            try:
                response, rig_response = predict(free_text)
                print(i, rig_response)
                if not rig_response:
                    error
                expected, response = correct_prediction(expected, response)

                # Numerical and segmentation scores
                binary_score_no_rule_instance = score_binary(expected, response)
                param_numerical_binary_score = score_param_type(expected, response, numerical=True)
                param_verbal_binary_score = score_param_type(expected, response, numerical=False)
                param_numerical_avg_score = score_param_type_avg(expected, response, numerical=True)
                param_verbal_avg_score = score_param_type_avg(expected, response, numerical=False)
                rule_name_score = score_rule_instance_name(expected, response)
                binary_score = 1 if rule_name_score and binary_score_no_rule_instance else 0

                # If there is a score mismatch, add the error data to the respective lists
                differences = None
                if binary_score == 0:
                    differences = find_differences(expected, response)
                if param_numerical_binary_score == 0:
                    error_df_param_numerical_binary_score.append(
                        collect_error_data('param_numerical_binary_score', row_id, expected, response, free_text, differences))
                if param_verbal_binary_score == 0:
                    error_df_param_verbal_binary_score.append(
                        collect_error_data('param_verbal_binary_score', row_id, expected, response, free_text, differences))
                if rule_name_score == 0:
                    error_df_rule_name_score.append(
                        collect_error_data('score_rule_instance_name', row_id, expected, response, free_text, differences))

                # New row with evaluation metrics
                new_row = {
                    "binary_score": binary_score,
                    "binary_score_no_rule_instance": binary_score_no_rule_instance,  # name
                    "param_numerical_binary_score": param_numerical_binary_score,
                    "param_verbal_binary_score": param_verbal_binary_score,
                    "param_numerical_avg_score": param_numerical_avg_score,
                    "param_verbal_avg_score": param_verbal_avg_score,
                    "score_rule_instance_name": rule_name_score,
                    "response": response,
                    "expected": expected,
                    "free_text": free_text,
                    "correct_type_name": int(clean_text(rig_response["type_name"]) == clean_text(type_name))
                }
                rows.append(new_row)
            except Exception as e:
                new_row = {
                    "binary_score": 0,
                    "binary_score_no_rule_instance": 0,
                    "param_numerical_binary_score": 0,
                    "param_verbal_binary_score": 0,
                    "param_numerical_avg_score": 0,
                    "param_verbal_avg_score": 0,
                    "score_rule_instance_name": 0,
                    "response": 'error',
                    "expected": expected,
                    "free_text": free_text,
                    "correct_type_name": 0
                }
                rows.append(new_row)

    # Convert the results into a DataFrame
    df_results = pd.DataFrame(rows)

    # Create DataFrames for the errors
    df_error_param_numerical_binary_score = pd.DataFrame(error_df_param_numerical_binary_score)
    df_error_param_verbal_binary_score = pd.DataFrame(error_df_param_verbal_binary_score)
    df_error_rule_name_score = pd.DataFrame(error_df_rule_name_score)

    # Return the results and the error DataFrames
    return df_results, df_error_param_numerical_binary_score, df_error_param_verbal_binary_score, df_error_rule_name_score


# Run the evaluation and collect the results
df_results, df_error_param_numerical_binary_score, df_error_param_verbal_binary_score, df_error_rule_name_score = evaluate()
def generate_unique_filename(directory, base_name, extension="csv"):
    """
    Generate a unique filename by appending a sequential number.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)  # Create the directory if it doesn't exist
    # Start with no number
    i = 1
    while True:
        filename = f"{base_name}_{i}.{extension}"
        full_path = os.path.join(directory, filename)
        if not os.path.exists(full_path):
            return full_path  # Return the first available filename
        i += 1


file_path = generate_unique_filename("output", "test_results")
df_results.to_csv(file_path, index=False)

file_path = generate_unique_filename("output", "error_param_numerical_binary_score")
df_error_param_numerical_binary_score.to_csv(file_path, index=False)

file_path = generate_unique_filename("output", "error_param_verbal_binary_score")
df_error_param_verbal_binary_score.to_csv(file_path, index=False)

file_path = generate_unique_filename("output", "error_rule_name_score")
df_error_rule_name_score.to_csv(file_path, index=False)


def calculate_accuracy(df):
    """
    Calculate the average accuracy for each scoring parameter.
    """
    accuracy_metrics = {
        "binary_score": df["binary_score"].mean(),
        "binary_score_no_instance_name": df["binary_score_no_rule_instance"].mean(),
        "param_numerical_binary_score": df["param_numerical_binary_score"].mean(),
        "param_numerical_avg_score": df["param_numerical_avg_score"].mean(),
        "param_verbal_binary_score": df["param_verbal_binary_score"].mean(),
        "param_verbal_avg_score": df["param_verbal_avg_score"].mean(),
        "score_rule_instance_name": df["score_rule_instance_name"].mean(),
        "classification score": df["correct_type_name"].mean()
    }

    # Print the results
    print("\nAverage Accuracy Metrics:")
    for metric, value in accuracy_metrics.items():
        print(f"{metric}: {value:.2%}")

    return accuracy_metrics


print("without classification mistakes: ")
accuracy_results = calculate_accuracy(df_results[df_results["correct_type_name"] == 1])
print("with all the data: ")
accuracy_results_2 = calculate_accuracy(df_results)