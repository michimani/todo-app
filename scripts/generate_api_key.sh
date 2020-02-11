#!/bin/bash

if [ $# != 2 ] || [ $1 = "" ] || [ $2 = "" ]; then
  echo "Two parameters are required"
  echo ""
  echo "1st : string for API Key name (ex. user1)"
  echo "2nd : string for Usage Plan ID (ex. abcd123)"
  echo ""
  echo "example command"
  echo "\t$ sh ./generate_api_key.sh user1 abcd123"
  exit
fi

API_KEY_NAME=$1
USAGE_PLAN_ID=$2

# create api key
CREATE_RES=$(aws apigateway create-api-key --name $API_KEY_NAME --enabled)
CREATED_API_KEY_ID=$(echo $CREATE_RES | jq ".id" | sed -E "s/\"//g")
CREATED_API_KEY_VALUE=$(echo $CREATE_RES | jq ".value" | sed -E "s/\"//g")

# add api key to usage plan
ADD_RES=$(aws apigateway create-usage-plan-key --usage-plan-id $USAGE_PLAN_ID --key-id $CREATED_API_KEY_ID --key-type API_KEY)
ADDED_KEY_ID=$(echo $ADD_RES | jq ".id" | sed -E "s/\"//g")

if [ $ADDED_KEY_ID != $CREATED_API_KEY_ID ]; then
  echo "Failed to generate a API Key"
  exit
fi

echo "API Key generated successfully."
echo $CREATE_RES | jq "."
