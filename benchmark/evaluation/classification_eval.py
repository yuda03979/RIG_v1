import polars as pl
from RIG import RuleInstanceGenerator
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


csv_path = "data/classification_data_yosef.csv"
df = pl.read_csv(csv_path)

rig = RuleInstanceGenerator()

def clean_text(text):
    """Remove all non-alphanumeric characters and convert to lowercase."""
    return ''.join(char.lower() for char in text if char.isalnum())

def evaluate_accuracy():
    rag_api = rig.get_instance.classifier.rag_api
    rows = []
    correct_predictions = 0

    # Iterate through the DataFrame rows
    for row in df.iter_rows(named=True):
        # Extract the free_text, actual type_name, and expected classification
        free_text = row['free_text']
        actual_type_name = row['type_names']
        id_free_text = row['id']

        # Predict the type name using the RAG API
        predicted_type_name = str(rag_api.get_closest_type_name(free_text)[0])

        # Clean strings for comparison
        actual_type_name_cleaned = clean_text(actual_type_name)
        predicted_type_name_cleaned = clean_text(predicted_type_name)

        # Debugging: Print the cleaned strings
        # print(f"Actual (cleaned): {actual_type_name_cleaned}")
        # print(f"Predicted (cleaned): {predicted_type_name_cleaned}")

        # Calculate the score (1 for correct, 0 for incorrect)
        score = 1 if predicted_type_name_cleaned == actual_type_name_cleaned else 0
        correct_predictions += score

        # Append the results to the rows
        rows.append({
            "id": id_free_text,
            "score": score,
            "predicted": predicted_type_name_cleaned,
            "actual": actual_type_name_cleaned,
            "free_text": free_text,
        })

    # Convert rows to a DataFrame
    results_df = pl.DataFrame(rows)

    # Calculate the final score
    accuracy = correct_predictions / len(df)

    return results_df, accuracy

# Run the evaluation
results_df, final_score = evaluate_accuracy()

# Print the final accuracy score
print(f"Accuracy Score: {final_score:.2%}")

# Print rows where the prediction was incorrect
errors = results_df.filter(pl.col("score") == 0).to_dicts()
# print("Errors:", errors)

# Optional: Save errors to a CSV
results_df.filter(pl.col("score") == 0).write_csv("output/classification_errors.csv")

print("results_df['actual'].unique():\n")
for i, _ in enumerate(results_df['actual'].unique()):
    print(i, _)

print("results_df['predicted'].unique():\n")
for i, _ in enumerate(results_df['predicted'].unique()):
    print(i, _)

new_row = pl.DataFrame({
    "id": ["9999999"],
    "score": [-1],
    "predicted": ["None"],
    "actual": ["None"],
    "free_text": ['this is fake']
})

results_df = pl.concat([results_df, new_row]).to_pandas()

confusion_matrix = pd.crosstab(
    results_df["actual"],
    results_df["predicted"],
    # normalize='index'
)


plt.figure(figsize=(20, 20))
sns.heatmap(
    confusion_matrix,
    annot=True,  # Show numbers in each cell
    cmap='Blues',  # Color scheme
    fmt='g',  # Format for the annotations
    xticklabels=confusion_matrix.columns
)
plt.title('Confusion Matrix')
plt.xlabel('Predicted Label')
plt.xticks(rig.get_rule_types())
plt.ylabel('Actual Label')
plt.yticks(rig.get_rule_types())
plt.tight_layout()
plt.show()