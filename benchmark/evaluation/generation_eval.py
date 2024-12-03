import pandas as pd
import ast

from RIG import RuleInstanceGenerator

# Initialize the rule instance generator
rig = RuleInstanceGenerator()

# Path to the CSV file containing eval_data_generation
csv_path = "data/generation_data.csv"

# Load the CSV file
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
df_eval["excepted_response"] = df_eval["excepted_response"].apply(ast.literal_eval)  # Convert strings to dictionaries
df_eval["free_text"] = df_eval["free_text"].apply(parse_free_text)  # Handle plain strings and lists

# Create eval_data_generation from the DataFrame
eval_data_generation = [
    (row["id"], row["type_names"], row["excepted_response"], row["free_text"])
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


def predict(free_text):
    """Predict rule instance using the rig."""
    model_response = rig.get_rule_instance(free_text)
    if model_response["error"] == True:
        return False, False
    rule_instance = model_response["rule_instance"]
    print(f"rule instance: {rule_instance}")
    response = rule_instance["params"]
    response["ruleInstanceName"] = rule_instance["ruleInstanceName"]
    response["severity"] = rule_instance["severity"]
    return response, model_response


def normalize_empty_value(value):
    """Normalize empty values to a common representation."""
    if value in [None, "", "null", "None", "none", "empty"] or (isinstance(value, float) and pd.isna(value)):
        return "EMPTY"  # Choose a common representation for empty values
    return value


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
        verbal_keys = [k for k, v in expected.items() if not is_numerical(v) and k != "ruleInstanceName"]

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
def collect_error_data(param_name, expected, response, free_text):
    """Helper function to create error data entry."""
    return {
        "param_name": param_name,
        "expected": expected,
        "response": response,
        "free_text": free_text
    }


# Initialize DataFrames for errors for each scoring metric
error_df_param_numerical_binary_score = []
error_df_param_verbal_binary_score = []
error_df_rule_name_score = []


# Evaluation Function
def evaluate():
    rows = []
    # Loop through the eval_data_generation
    for row_id, type_name, expected, free_text_list in eval_data_generation:
        for free_text in free_text_list:
            # print(free_text)
            if not free_text.strip():
                print("Skipping empty free_text")
                continue

            try:
                # Predict the response
                response, rig_response = predict(free_text)
                if not rig_response:
                    error
                # Normalize values
                expected, response = correct_prediction(expected, response)

                # Numerical and segmentation scores
                binary_score = int(response == expected)
                param_numerical_binary_score = score_param_type(expected, response, numerical=True)
                param_verbal_binary_score = score_param_type(expected, response, numerical=False)
                param_numerical_avg_score = score_param_type_avg(expected, response, numerical=True)
                param_verbal_avg_score = score_param_type_avg(expected, response, numerical=False)
                rule_name_score = score_rule_instance_name(expected, response)

                # If there is a score mismatch, add the error data to the respective lists
                if param_numerical_binary_score == 0:
                    error_df_param_numerical_binary_score.append(
                        collect_error_data('param_numerical_binary_score', expected, response, free_text))
                if param_verbal_binary_score == 0:
                    error_df_param_verbal_binary_score.append(
                        collect_error_data('param_verbal_binary_score', expected, response, free_text))
                if rule_name_score == 0:
                    error_df_rule_name_score.append(
                        collect_error_data('score_rule_instance_name', expected, response, free_text))

                # New row with evaluation metrics
                new_row = {
                    "binary_score": binary_score,
                    "param_numerical_binary_score": param_numerical_binary_score,
                    "param_verbal_binary_score": param_verbal_binary_score,
                    "param_numerical_avg_score": param_numerical_avg_score,
                    "param_verbal_avg_score": param_verbal_avg_score,
                    "score_rule_instance_name": rule_name_score,
                    "response": response,
                    "expected": expected,
                    "free_text": free_text,
                    "correct_type_name": int(rig_response["type_name"] == type_name)
                }
                rows.append(new_row)
            except Exception as e:
                new_row = {
                    "binary_score": 0,
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

# Save the full results
df_results.to_csv("output/test_results.csv", index=False)

# Save the error DataFrames
df_error_param_numerical_binary_score.to_csv("output/error_param_numerical_binary_score.csv", index=False)
df_error_param_verbal_binary_score.to_csv("output/error_param_verbal_binary_score.csv", index=False)
df_error_rule_name_score.to_csv("output/error_rule_name_score.csv", index=False)


# Optional: Print out the error dataframes to verify


def calculate_accuracy(df):
    """
    Calculate the average accuracy for each scoring parameter.
    """
    accuracy_metrics = {
        "binary_score": df["binary_score"].mean(),
        "param_numerical_binary_score": df["param_numerical_binary_score"].mean(),
        "param_numerical_avg_score": df["param_numerical_avg_score"].mean(),
        "param_verbal_binary_score": df["param_verbal_binary_score"].mean(),
        "param_verbal_avg_score": df["param_verbal_avg_score"].mean(),
        "score_rule_instance_name": df["score_rule_instance_name"].mean(),
    }

    # Print the results
    print("\nAverage Accuracy Metrics:")
    for metric, value in accuracy_metrics.items():
        print(f"{metric}: {value:.2%}")

    return accuracy_metrics


# Calculate and print the accuracy metrics
accuracy_results = calculate_accuracy(df_results[df_results["correct_type_name"] == 1])
"""Average Accuracy Metrics:
binary_score: 8.60%
param_numerical_binary_score: 67.87%
param_verbal_binary_score: 8.60%
param_numerical_avg_score: 87.78%
param_verbal_avg_score: 69.66%
score_rule_instance_name: 81.90%"""
accuracy_results_2 = calculate_accuracy(df_results)
