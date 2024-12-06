import gradio as gr
import threading
import time

from RIG.rule_instance_generator import RuleInstanceGenerator


elta_project = RuleInstanceGenerator()

def submit_input(query, json_file):
    response = {}

    ###################

    if json_file:
        if elta_project.new_rule_type(json_file):
            response["message"] = "New type added successfully!\n"
        else:
            response["message"] = "Your file didn't upload! Something went wrong.\n"
        return response, "", None, show_rule_types()


    ####################

    if any(char.isalpha() for char in query):
        response = elta_project.get_rule_instance(query)
    return response, "", None, show_rule_types()


def show_rule_types():
    return "\n".join(elta_project.globals.db_manager.get_all_types_names())


############################

def run_gui():
    with gr.Blocks() as demo:
        gr.Markdown("# Rules Manager")

        with gr.Row():
            input_text = gr.Textbox(label="User Input", value=" ")
            file_input = gr.File(label="Upload a new RuleType File")

        output = gr.JSON(label="Output")  # Use gr.JSON for JSON formatted output
        rule_types_output = gr.Textbox(label="Rule Types", lines=0)

        submit_btn = gr.Button("Process")
        submit_btn.click(
            fn=submit_input,
            inputs=[input_text, file_input],
            outputs=[output, input_text, file_input, rule_types_output]
        )

        rule_types_output.value = show_rule_types()

    demo.launch(server_name="0.0.0.0", server_port=8000)