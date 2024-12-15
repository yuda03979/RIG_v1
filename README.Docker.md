
# Project Setup and Deployment Guide

## Prerequisites

### Installation Requirements
- Git (for large file handling)
- Docker
- Docker Compose

## Setup Steps

### 1. Git LFS Configuration
Initialize Git Large File Storage (LFS):
```bash
git lfs install
```
or:
```angular2html
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt install git-lfs
```


### 2. Model Downloads (Optional)

#### Gemma Model
Download the Gemma model:
```bash
curl -L -O https://huggingface.co/lmstudio-community/gemma-2-2b-it-GGUF/resolve/main/gemma-2-2b-it-Q8_0.gguf
```

#### RAG Model
Clone the BGE-M3 model:
```bash
git clone https://huggingface.co/BAAI/bge-m3
```

### 3. Configuration

#### Environment Configuration
1. Locate the `.env` file
2. Update paths and settings as required
3. Ensure all necessary environment variables are set correctly


## Running the Application

install docker
```
sudo snap install docker  
```

### Local Development
Navigate to the project directory and run:
```bash
docker compose build
```

### to run it:
docker compose up

The application will be accessible at: http://localhost:8000/docs
also you can run it with the examples below (curl) or with the how_to_docker.ipynb

- --
## to use it with python, check out the how_to_docker.ipyb notebook.
- --
# how to use:

- --
- functions:
1. init_gemma_model
```bash
  curl -X 'POST' \
  'http://0.0.0.0:8000/init_gemma_model?max_context_length=1536&max_new_tokens=512&n_threads=8' \
  -H 'accept: application/json' \
  -d ''
```
output:
true
2. get_rule_instance
```
  curl -X 'POST' \
  'http://0.0.0.0:8000/get_rule_instance?free_text=system%20failure%20severity%205' \
  -H 'accept: application/json' \
  -d ''
```
output:
{"rule_instance":{"_id":"00000000-0000-0000-0000-000000000000","description":"string","isActive":true,"lastUpdateTime":"00/00/0000 00:00:00","params":{"speed":"null","type":"null","weight":"null","fuel":"null","altitute":"null","wheels":"null","engine":"null"},"ruleInstanceName":"system failure - system failure","severity":5,"ruleType":"structured","ruleOwner":"","ruleTypeId":"fb8e8ef1-e382-43b5-b896-70d254878751","eventDetails":[{"objectName":"Airplan","objectDescription":null,"timeWindowInMilliseconds":0,"useLatest":false}],"additionalInformation":{},"presetId":"00000000-0000-0000-0000-000000000000"},"is_error":false,"error_message":"","free_text":"system failure severity 5","type_name":"system failure","rag_score":0.6298588514328003,"model_response":"```json\n    {\"speed\": null, \"type\": \"null\", \"weight\": null, \"fuel\": null, \"altitute\": null, \"wheels\": null, \"engine\": null, \"ruleInstanceName\": \"system failure - system failure\", \"severity\": 5}","schema":{"speed":"Int","type":"String","weight":"Int","fuel":"Int","altitute":"Int","wheels":"Int","engine":"Int","ruleInstanceName":"string","severity":"int"},"time":"2024-12-08|11:12:02","inference_time":15.802719354629517}%

3. get_rule_types_names
```angular2html
  curl -X 'GET' \
  'http://0.0.0.0:8000/get_rule_types_names' \
  -H 'accept: application/json'
```
output:
["missile malfunction","missile failure","launch failure","platoon report","encryption flaw","corruption scandal","betrayal risk","leadership breakdown","satellite disruption","bomb failure","defection threat","attack overview","fire control","disloyal soldier","command incompetence","supply shortage","system failure","covert agent","suspected person","radar error monitoring","api throttling","temperature overload","disk space warning","memory usage alert","equipment malfunction","password expiry","temperature threshold exceeded"]%

4. tweak_rag_parameters
```angular2html
curl -X 'POST' \
  'http://0.0.0.0:8000/tweak_rag_parameters?rag_difference=0.002&rag_threshold=0.5' \
  -H 'accept: application/json' \
  -d ''
```
output:
true

5. feedback
```
curl -X 'POST' \
  'http://0.0.0.0:8000/feedback?fb=True' \
  -H 'accept: application/json' \
  -d ''
```
output:
thank you :)


# example .env:
# leave "" if you don't want to use the variable.

PROJECT_DIRECTORY="/home/ubuntu/RIG_v1/project_directory/"               # required
GPT_MODEL_PATH="/home/ubuntu/gemma-2-2b-it-Q8_0.gguf"             # required
RAG_MODEL_PATH="/home/ubuntu/bge-m3"                              # required
RULE_TYPES_DIRECTORY="/home/ubuntu/RIG_v1/evaluation/data/rule_types/"    # optional - you don't need to change that
RAG_DIFFERENCE="0.001"                                                          # optional - you don't need to change that
RAG_THRESHOLD="0.5"                                                             # optional - you don't need to change that
MAX_CONTEXT_LENGTH="1536"                                                       # optional - you don't need to change that
MAX_NEW_TOKENS="512"                                                            # optional - you don't need to change that
N_THREADS="8"                                                                   # optional - you don't need to change that
