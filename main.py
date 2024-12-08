from RIG import rule_instance_generator
from fastapi import FastAPI
from dotenv import find_dotenv, load_dotenv
import os
import ast
load_dotenv(find_dotenv())


app = FastAPI()

project_directory = os.getenv("PROJECT_DIRECTORY") if os.getenv("PROJECT_DIRECTORY") != "" else None
gpt_model_path = os.getenv("GPT_MODEL_PATH") if os.getenv("GPT_MODEL_PATH") != "" else None
rag_model_path = os.getenv("RAG_MODEL_PATH") if os.getenv("RAG_MODEL_PATH") != "" else None
llama_server_path = os.getenv("LLAMA_SERVER_PATH") if os.getenv("LLAMA_SERVER_PATH") != "" else None
rule_types_directory = os.getenv("RULE_TYPES_DIRECTORY") if os.getenv("RULE_TYPES_DIRECTORY") != "" else None
rag_difference = float(os.getenv("RAG_DIFFERENCE")) if os.getenv("RAG_DIFFERENCE") != "" else None
rag_threshold = float(os.getenv("RAG_THRESHOLD")) if os.getenv("RAG_THRESHOLD") != "" else None
max_context_length = int(os.getenv("MAX_CONTEXT_LENGTH")) if os.getenv("MAX_CONTEXT_LENGTH") != "" else None
max_new_tokens = int(os.getenv("MAX_NEW_TOKENS")) if os.getenv("MAX_NEW_TOKENS") != "" else None
n_threads = int(os.getenv("N_THREADS")) if os.getenv("N_THREADS") != "" else None



rig = rule_instance_generator.RuleInstanceGenerator(

    project_directory=project_directory,
    gpt_model_path=gpt_model_path,
    rag_model_path=rag_model_path,
    llama_server_path=llama_server_path,
    rule_types_directory=rule_types_directory,
    rag_difference=rag_difference,
    rag_threshold=rag_threshold,
    max_context_length=max_context_length,
    max_new_tokens=max_new_tokens,
    n_threads=n_threads,
)

@app.post("/init_gemma_model")
def init_gemma_model(
    max_context_length=max_context_length,
    max_new_tokens=max_new_tokens,
    n_threads=n_threads
):
    return rig.init_gemma_model(int(max_context_length), int(max_new_tokens), int(n_threads))


@app.post("/get_rule_instance")
def get_rule_instance(free_text):
    return rig.get_rule_instance(free_text)


@app.get("/get_rule_types_names")
def get_rule_types_names():
    return rig.get_rule_types_names()


# @app.post("/new_rule_type")
# def new_rule_type(rule_type):
#     return rig.new_rule_type(rule_type)


@app.post("/tweak_rag_parameters")
def tweak_rag_parameters(
        rag_difference=os.getenv("RAG_DIFFERENCE"),
        rag_threshold=os.getenv("RAG_THRESHOLD")
):
    return rig.tweak_rag_parameters(float(rag_threshold), float(rag_difference))

@app.post("/feedback")
def feedback(fb):
    return rig.feedback(fb)


