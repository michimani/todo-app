#!/bin/bash

CHANGESET_OPTION="--no-execute-changeset"
TARGET_API_ID=$(cat ./.chalice/deployed/prod.json | jq '.resources[].rest_api_id' | grep -E "^\".+\"" | sed -e "s/\"//g")

if [ $# = 1 ] && [ $1 = "deploy" ]; then
  echo "deploy mode"
  CHANGESET_OPTION=""
fi

CFN_TEMPLATE="$(dirname $0)/api-custom-domain.yml"
CFN_STACK_NAME=TodoApiCustomDomain

aws cloudformation deploy --stack-name $CFN_STACK_NAME --template-file $CFN_TEMPLATE \
--parameter-overrides AcmArn=$TD_ACM_ARN \
CustomDomainName=$TD_CUSTOM_DOMAIN_NAME \
ChaliceDeployedApi=$TARGET_API_ID \
DomainHostZoneId=$TD_DOMAIN_HOST_ZONE_ID
