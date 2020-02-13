#!/bin/bash

aws cloudformation delete-stack --stack-name "TodoDynamoDB"
aws cloudformation delete-stack --stack-name "TodoApiUsagePlan"
