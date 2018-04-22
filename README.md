# Getting Started
## Installing dependencies
1. Install [python](https://www.python.org/downloads/) v3.6 or greater
1. Open a commandline and navigate to this directory
1. Install the required python dependencies listed in `requirements.txt` by running `pip install -r requirements.txt` in the commandline

## Running the project locally
1. Open the commandline and navigate to this directory
1. Run `python ./main.py` to run the server

## Generating the API Client for Aurelia and TypeScript
1. Install [nswag](https://github.com/RSuter/NSwag) using npm by running `npm install -g nswag` from the commandline
1. Install the [.NET Core Runtime v2.0.7](https://www.microsoft.com/net/download/all)
1. Run the api server locally
1. Run the following command in the commandline `nswag swagger2tsclient /input:http://localhost:9001/swagger.json /output:client.ts /template:aurelia /runtime:NetCore20`
