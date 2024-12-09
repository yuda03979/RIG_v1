
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

install docker compose
```
sudo apt-get install docker-compose-plugin
```
or:
```angular2html
sudo curl -L "https://github.com/docker/compose/releases/download/v2.29.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```
output: ```Docker Compose version v2.29.1```
### Local Development
Navigate to the project directory and run:
```bash
docker compose up --build
```

The application will be accessible at: http://localhost:8000/docs

## Deployment to Cloud

### Building Docker Image

#### Standard Build
```bash
docker build -t myapp .
```

#### Cross-Platform Build (e.g., Mac M1 to AMD64)


```bash
docker build --platform=linux/amd64 -t myapp .
```

### Pushing to Registry
```bash
docker push myregistry.com/myapp
```

## Additional Resources
- [Docker's Python Guide](https://docs.docker.com/language/python/)
- [Docker Getting Started - Sharing](https://docs.docker.com/go/get-started-sharing/)

## Troubleshooting
- Verify Docker and Docker Compose are correctly installed
- Check environment variable configurations - they all must be correct, even if you don't use them.
- Ensure model files are downloaded and placed correctly

## Notes
- Recommended to use the latest stable versions of Docker and Docker Compose
- Platform-specific build may be necessary for cloud deployment


# how to use:
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