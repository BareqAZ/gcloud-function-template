# Google Cloud Function Template
A Python-based template designed for rapidly and efficiently building APIs using Google Cloud Functions.


# Key Features
- Support for multiple API endpoints within a single cloud function
- Logging utility that logs to Google Cloud Operations Suite (formerly known as Stackdriver)
- Built-in API authentication mechanism, featuring both public and private route options
- Integrated testing and linting


# Getting Started
## Run
To get started you will need to setup your python environment:
- Create a python virtual environment `python3 -m venv .venv`
- Activate the virtual environment `source .venv/bin/activate`
- Install the required dependencies `pip3 install -r requirements.txt`
- Install the development dependencies `pip3 install -r requirements_dev.txt`
- Run the application `run.sh`

## Develop
- First you may want to edit the `.env` file to add your own credentials
- Then modify the contents of the `app` directory to build your own API functionality
- Write relevant tests in the `tests` directory
- Run the linters `run.sh --lint` they will automatically fix any linting issues
- Run tests `pytest tests`
- Run application `run.sh`

## Deploy
To deploy the application you must have gcloud CLI installed and configured, more information can be found here: https://cloud.google.com/sdk/docs/install-sdk
Once you've got gcloud CLI configured simply run the following `run.sh --deploy` it will use the configured gcloud project and it will deploy a cloud function with the same name as configured in the `.env` file.
