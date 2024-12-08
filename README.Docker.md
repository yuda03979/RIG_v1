
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
### Building and running

- (before that, read the how to use section).

in your terminal, go to the project directory.

When you're ready, start your application by running:
`docker compose up --build`.

Your application will be available at http://localhost:8000.

### Deploying your application to the cloud

First, build your image, e.g.: `docker build -t myapp .`.
If your cloud uses a different CPU architecture than your development
machine (e.g., you are on a Mac M1 and your cloud provider is amd64),
you'll want to build the image for that platform, e.g.:
`docker build --platform=linux/amd64 -t myapp .`.

Then, push it to your registry, e.g. `docker push myregistry.com/myapp`.

Consult Docker's [getting started](https://docs.docker.com/go/get-started-sharing/)
docs for more detail on building and pushing.

### References
* [Docker's Python guide](https://docs.docker.com/language/python/)



## how to use:
- place the correct pathes in the .env file - check out what is required changes.

- make sure to `init_gemma_model` before using.

