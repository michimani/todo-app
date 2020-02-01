#!/bin/bash

CHANGESET_OPTION="--no-execute-changeset"

if [ $# = 1 ] && [ $1 = "deploy" ]; then
  echo "deploy mode"
  CHANGESET_OPTION=""
fi

CFN_TEMPLATE="$(dirname $0)/dynamodb.yml"
CFN_STACK_NAME=TodoDynamoDB

aws cloudformation deploy --stack-name ${CFN_STACK_NAME} --template-file ${CFN_TEMPLATE} ${CHANGESET_OPTION}
