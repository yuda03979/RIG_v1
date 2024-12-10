import json


class ConfidenceValidator:
    def __init__(self, model):
        """
        Initialize with external model
        model: instance of external class that handles model operations
        """
        self.model = model
        
    def create_prompt(self, text, extracted_data, schema) -> str:
        """Create the validation prompt"""
        

        prompt = f"""You are an expert data validator. Your task is to evaluate:
1. How well the extracted data matches the given text
2. How well the data types conform to the provided schema

Context Text (Answer Key):
{text}

Schema Definition:
{json.dumps(schema, indent=2)}

Extracted Data:
{json.dumps(extracted_data, indent=2)}

Please analyze carefully:

1. Text Matching:
   - Find corresponding information in the text
   - Compare values exactly
   - Note discrepancies
   - Mark fields not in text as "unverifiable"

2. Schema Validation:
   - Check if each field matches its defined type
   - Verify required fields exist
   - Check data type correctness

Scoring Guidelines:
- 70% weight for text matching accuracy
- 30% weight for schema conformance
- Deduct points for missing required fields
- Deduct points for incorrect types
- Deduct points for unverifiable or incorrect values

Return only the final combined numerical score between 0-100.
Score:"""
        return prompt

    def extract_score(self, response: str) -> float:
        """Extract numerical score from model response"""
        try:
            score = float(''.join(filter(str.isdigit, response.split("Score:")[-1])))
            return min(max(score, 0), 100)
        except Exception:
            return 50

    def check_match(self, text: str, extracted_data: dict, temperature=0.1) -> float:
        """Main validation method"""
        prompt = self.create_prompt(text, extracted_data)
        response = self.model.generate_response(prompt, temperature)
        return self.extract_score(response)


# דוגמאות לקלטים רצויים
# text = """Please create a Rule instance Suspected Person - other that relates to Suspected Person. 
#     The person is old 26. Gender F. HistoryRecord 0. Organization RedCross."""

# data = {
#         "ruleInstanceName": "Suspected Person - other",
#         "age": 26,
#         "gender": "F",
#         "historyRecord": 0,
#         "organization": "RedCross"
#     }
# schema = [
#             "ruleInstanceName: {'type': 'string'}", 
#             "age: {'type': 'Int'}", 
#             "gender: {'type': 'String'}", 
#             "historyRecord: {'type': 'Int'}", 
#             "organization: {'type': 'String'}", 
#             "address: {'type': 'String'}"
#         ]