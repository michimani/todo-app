todo-app
===

# Preparing

## DynamoDB local

1. download from [DynamoDB (ダウンロード可能バージョン) - Amazon DynamoDB](https://docs.aws.amazon.com/ja_jp/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html)
2. run following command
  
    ```zsh
    $ export DYNAMODB_LOCAL_DIR=your_dynamo_db_local_path
    $ java -Djava.library.path=$DYNAMODB_LOCAL_DIR/DynamoDBLocal_lib \
    -jar $DYNAMODB_LOCAL_DIR/DynamoDBLocal.jar \
    -sharedDb -port 8001
    ```

3. create table
  
    ```zsh
    $ aws dynamodb create-table \
    --cli-input-json file://dynamodb_local_schema.json \
    --endpoint-url http://localhost:8001
    ```

# Run at local

1. start DynamoDB local
2. run following command

    ```zsh
    $ chalice local
    Found credentials in shared credentials file: ~/.aws/credentials
    Serving on http://127.0.0.1:8000
    ```

# Deploy to AWS

1. create table

    ```zsh
    $ sh ./cfn/00-dynamodb.sh deploy
    ```

2. deploy app

    ```zsh
    $ chalice deploy
    ```