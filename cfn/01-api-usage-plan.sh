#!/bin/bash

CHANGESET_OPTION="--no-execute-changeset"
TARGET_API_ID=$(cat ./.chalice/deployed/prod.json | jq '.resources[].rest_api_id' | grep -E "^\".+\"" | sed -e "s/\"//g")

if [ $# = 1 ] && [ $1 = "deploy" ]; then
  echo "deploy mode"
  CHANGESET_OPTION=""
fi

CFN_TEMPLATE="$(dirname $0)/api-usage-plan.yml"
CFN_STACK_NAME=TodoApiUsagePlan

aws cloudformation deploy --stack-name ${CFN_STACK_NAME} --template-file ${CFN_TEMPLATE} --parameter-overrides ChaliceDeployedApi=$TARGET_API_ID ${CHANGESET_OPTION}

if [ $# = 1 ] && [ $1 = "deploy" ]; then
  echo "\n----------------------------------------------\n"
  echo "Following string is ID of created usage plan. Use it for creating api key belongs to an usage plan.\n"
  aws cloudformation describe-stacks --stack-name ${CFN_STACK_NAME} | jq ".Stacks[0].Outputs[0].OutputValue" | sed -E "s/\"//g"
fi
