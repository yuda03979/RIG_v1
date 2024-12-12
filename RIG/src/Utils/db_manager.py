import ast
import os
import pandas as pd


class DBManager:

    def __init__(self, db_path):
        """
        ensure your db_path is good. e.g. example.csv
        :param db_path:
        """
        self.db_path = db_path
        self.df = self.get_df()

    def validate_db_path(self):
        if self.db_path[-4:] != '.csv':
            raise f"the db_path should end with '.csv'! your path: {self.db_path}"

    def get_df(self) -> pd.DataFrame:
        try:
            df = pd.read_csv(self.db_path)
        except:
            df = pd.DataFrame(
                columns=["type_name", "schema", "description", "default_values", "default_rule_instance", "rule_type",
                         "embedding"])
            self.update_db()
        return df

    def update_db(self) -> None:
        """
        Save the current DataFrame to the db.
        """
        self.df.to_csv(self.db_path, index=False)

    def get_all_types_names(self) -> list:
        """
        Get a list of all types in the DataFrame.
        :return: List of all types.
        """
        return self.df['type_name'].tolist()

    def get_dict_features(self, type_name, feature) -> dict:
        """

        :param type_name: must like in the rule_type
        :return: rule_type -> dict
        """
        return ast.literal_eval(self.df[self.df['type_name'] == type_name][feature].iloc[0])

    def get_embedding(self, type_name) -> list:
        return ast.literal_eval(self.df[self.df['type_name'] == type_name]["embedding"].tolist()[0])

    def write_new_type(self, type_name: str, schema: str, description: str, default_values: str,
                       default_rule_instance: str,
                       rule_type: str, embedding: str) -> None:
        """
        Add or update a new type_name in the DataFrame and save the changes to S3.
        :param type_name: The type name.
        :param schema:
        :param description:
        :param default_values:
        :param default_rule_instance:
        :param rule_type: The new type_name to be added or updated.
        """
        new_row = {
            'type_name': type_name,
            'schema': schema,
            'description': description,
            'default_values': default_values,
            'default_rule_instance': default_rule_instance,
            'rule_type': rule_type,
            'embedding': embedding
        }

        if type_name in self.get_all_types_names():
            self.df.loc[self.df['type_name'] == type_name, list(new_row.keys())] = list(new_row.values())
        else:
            self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
        self.update_db()
