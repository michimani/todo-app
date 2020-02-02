#!/bin/bash

java -Djava.library.path=$DYNAMODB_LOCAL_DIR/DynamoDBLocal_lib \
-jar $DYNAMODB_LOCAL_DIR/DynamoDBLocal.jar \
-sharedDb -port 8001