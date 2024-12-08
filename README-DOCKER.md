
# Installation

* git - big files
```angular2html
git lfs install
```
* install docker


## - downlads (if using internet):
* gemma:
```
curl -L -O https://huggingface.co/lmstudio-community/gemma-2-2b-it-GGUF/resolve/main/gemma-2-2b-it-Q8_0.gguf
```
* rag:
```
git clone https://huggingface.co/BAAI/bge-m3
```
## - run docker
- (before that, read the how to use section).
1. open the docker app.
2. in your terminal, go to the project directory.
3. run:
```
docker-compose up --build 
```
4. you ready to go. check out: 
```angular2html
http://0.0.0.0:8000/docs
```

## how to use:
- place the correct pathes in the .env file



- make sure to `init_gemma_model` before using.