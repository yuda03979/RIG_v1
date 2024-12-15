from RIG import rule_instance_generator
from fastapi import FastAPI
from dotenv import find_dotenv, load_dotenv
import os
import ast
load_dotenv(find_dotenv())


app = FastAPI()


def validate_path(env_var, var_name):
    """Validate and return the path or None if invalid."""
    if not env_var or not os.path.exists(env_var):
        print(f"Warning: {var_name} is invalid or does not exist: {env_var}")
    return env_var


def validate_numeric(env_var, var_name, cast_func, default=None):
    try:
        return cast_func(env_var) if env_var else default
    except ValueError:
        print(f"Warning: {var_name} is invalid: {env_var}")
        return default


project_directory = validate_path(os.getenv("PROJECT_DIRECTORY"), "PROJECT_DIRECTORY")
gpt_model_path = validate_path(os.getenv("GPT_MODEL_PATH"), "GPT_MODEL_PATH")
rag_model_path = validate_path(os.getenv("RAG_MODEL_PATH"), "RAG_MODEL_PATH")
rule_types_directory = validate_path(os.getenv("RULE_TYPES_DIRECTORY"), "RULE_TYPES_DIRECTORY")
rag_difference = validate_numeric(os.getenv("RAG_DIFFERENCE"), "RAG_DIFFERENCE", float)
rag_threshold = validate_numeric(os.getenv("RAG_THRESHOLD"), "RAG_THRESHOLD", float)
max_context_length = validate_numeric(os.getenv("MAX_CONTEXT_LENGTH"), "MAX_CONTEXT_LENGTH", int)
max_new_tokens = validate_numeric(os.getenv("MAX_NEW_TOKENS"), "MAX_NEW_TOKENS", int)
n_threads = validate_numeric(os.getenv("N_THREADS"), "N_THREADS", int)




rig = rule_instance_generator.RuleInstanceGenerator(

    project_directory=project_directory,
    gpt_model_path=gpt_model_path,
    rag_model_path=rag_model_path,
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


