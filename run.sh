#!/usr/bin/env bash
# A simple bash script that handles running, deploying and deleting the cloud function.

# Find the absolute path regardless of where this script is being executed from.
SRC=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source "$SRC/.env" 2> /dev/null
FUNCTION_NAME=${FUNCTION_NAME:-"gcloud-func-dev"}
API_KEY=${API_KEY:-"gcloud-func-key"}

test -f "$SRC/.env" || {
    echo "FUNCTION_NAME=$FUNCTION_NAME" > "$SRC/.env"
    echo "API_KEY=$API_KEY" >> "$SRC/.env"
}


function run() {
    trap 'exit' SIGINT
    cd "$SRC" || exit
    while true; do
        source ".venv/bin/activate"
        functions-framework --target=main --debug
        printf "\e[31;1;5mServer crashed, restarting!\e[0m\n"
        sleep 5
    done
}


function deploy() {
    printf "Deploying the cloud function: \e[31m%s\e[0m\n" "$FUNCTION_NAME"
    gcloud functions deploy "$FUNCTION_NAME" \
        --runtime=python311 \
        --source="$SRC" \
        --trigger-http \
        --entry-point=main \
        --gen2 \
        --region=us-east1 \
        --allow-unauthenticated \
        --memory=128MiB \
        --cpu=0.333 \
        --set-env-vars API_KEY="$API_KEY"

    if [[ $? -eq 0 ]]; then
        printf "Successfully deployed the cloud function: \e[31m%s\e[0m\n" "$FUNCTION_NAME"
        exit 0
    else
        printf "Failed to deploy the cloud function: \e[31m%s\e[0m\n" "$FUNCTION_NAME"
        exit 1
    fi
}


function delete() {
    printf "Deleting the cloud function: \e[31m%s\e[0m\n" "$FUNCTION_NAME"
    gcloud functions delete "$FUNCTION_NAME" --region=us-east1

    if [[ $? -eq 0 ]]; then
        printf "Successfully deleted the cloud function: \e[31m%s\e[0m\n" "$FUNCTION_NAME"
        exit 0
    else
        printf "Failed to delete the cloud function: \e[31m%s\e[0m\n" "$FUNCTION_NAME"
        exit 1
    fi
}


function lint() {
    set -e
    linter_path="$*"
    [[ -z $linter_path ]] && linter_path="$SRC/app"
    flake8 "$linter_path" --config "$SRC/linter_config.cfg" --exit-zero
    black "$linter_path"
    isort "$linter_path" --settings-path "$SRC/linter_config.cfg"
    radon mi -s -n B "$linter_path"
}


if [[ $# -eq 0 ]]; then
    run
fi


USAGE="
Usage: \e[33m$(basename "$0")\e[0m [OPTION]

    \e[33m--remove\e[0m        Remove the cloud function from GCP
    \e[33m--update\e[0m        Update the cloud function to GCP
    \e[33m--lint\e[0m          Run linters on the local code
    \e[33m--deploy\e[0m        Deploy the cloud function to GCP
    \e[33m--run\e[0m           Run the cloud function locally
"


case "$1" in
    "--remove"|"--delete")
        delete
        ;;
    "--deploy"|"--update")
        deploy
        ;;
    "--lint")
        shift
        lint "$@"
        ;;
    "--run")
        run
        ;;
    *)
        echo -e "$USAGE"
esac
