#!/bin/bash

# Default file names
dotenv=".env"
output="gradient-deployment.yaml"

# Parse command line arguments
while getopts ":e:o:" opt; do
    case $opt in
    e)
        dotenv="$OPTARG"
        ;;
    o)
        output="$OPTARG"
        ;;
    \?)
        echo "Invalid option -$OPTARG" >&2
        exit 1
        ;;
    :)
        echo "Option -$OPTARG requires an argument." >&2
        exit 1
        ;;
    esac
done

echo "Using dotenv file: '$dotenv' and output file: '$output'"

# Set the environment variables from the .env file
source $dotenv

# Clear the output file if it exists, or create it if it doesn't
>"$output"

# Write the beginning of the yaml to the output file
cat >"$output" <<EOL
enabled: $PAPER_SPACE_DEPLOY_ENABLED
image: $PAPER_SPACE_DEPLOY_IMAGE
resources:
  replicas: $PAPER_SPACE_DEPLOY_REPLICAS
  instanceType: $PAPER_SPACE_DEPLOY_INSTANCE_TYPE
env:
EOL

# Read the input file line by line
while IFS= read -r line; do
    # Skip if line is empty or only contains whitespace
    [[ -z "${line// /}" ]] && continue

    # Check if the line contains the assignment (=)
    if [[ $line == *=* ]] && [[ ! $line == \#* ]] && [[ ! $line == *PAPERSPACE_* ]]; then
        key="${line%=*}"
        value="${line#*=}"

        # Append the key-value pair to the spec file in the desired format
        echo "  - name: $key" >>"$output"
        echo "    value: $value" >>"$output"
    fi

done <"$dotenv"

echo "Done! Spec file written to '$output'"
