from RIG import rule_instance_generator
from fastapi import FastAPI
from dotenv import find_dotenv, load_dotenv
import os
load_dotenv(find_dotenv())


app = FastAPI()


rig = rule_instance_generator.RuleInstanceGenerator(
    project_directory=os.getenv("PROJECT_DIRECTORY"),
    gpt_model_path=os.getenv("GPT_MODEL_PATH"),
    rag_model_path=os.getenv("RAG_MODEL_PATH"),
    llama_server_path=os.getenv("LLAMA_SERVER_PATH"),
    rule_types_directory=os.getenv("RULE_TYPES_DIRECTORY"),
    rag_difference=float(os.getenv("RAG_DIFFERENCE")),
    rag_threshold=float(os.getenv("RAG_THRESHOLD")),
    max_context_length=int(os.getenv("MAX_CONTEXT_LENGTH")),
    max_new_tokens=int(os.getenv("MAX_NEW_TOKENS")),
    n_threads=int(os.getenv("N_THREADS")),
)

@app.post("/init_gemma_model")
def init_gemma_model(
    max_context_length=os.getenv("MAX_CONTEXT_LENGTH"),
    max_new_tokens=os.getenv("MAX_NEW_TOKENS"),
    n_threads=os.getenv("N_THREADS")
):
    return rig.init_gemma_model(int(max_context_length), int(max_new_tokens), int(n_threads))


@app.post("/get_rule_instance")
def get_rule_instance(free_text):
    return str(rig.get_rule_instance(free_text))


@app.get("/get_rule_types_names")
def get_rule_types_names():
    return rig.get_rule_types_names()


@app.post("/new_rule_type")
def new_rule_type(rule_type):
    return rig.new_rule_type(rule_type)


@app.post("/tweak_rag_parameters")
def tweak_rag_parameters(
        rag_difference=os.getenv("RAG_DIFFERENCE"),
        rag_threshold=os.getenv("RAG_THRESHOLD")
):
    return rig.tweak_rag_parameters(float(rag_threshold), float(rag_differences))

@app.post("/feedback")
def feedback(fb):
    return rig.feedback(fb)


