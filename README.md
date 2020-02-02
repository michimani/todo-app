todo-app
===

# Preparing

## DynamoDB local

1. download from [DynamoDB (ダウンロード可能バージョン) - Amazon DynamoDB](https://docs.aws.amazon.com/ja_jp/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html)
2. run following command
  
    ```zsh
    $ export DYNAMODB_LOCAL_DIR=your_dynamo_db_local_path
    $ sh start_local_db.sh
    ```

3. create table
  
    ```zsh
    $ aws dynamodb create-table \
    --cli-input-json file://dynamodb_local_schema.json \
    --endpoint-url http://localhost:8001
    ```

# Run at local

1. start DynamoDB local

    ```zsh
    $ sh start_local_db.sh
    ```

2. run following command

    ```zsh
    $ chalice local --stage dev
    Found credentials in shared credentials file: ~/.aws/credentials
    Serving on http://127.0.0.1:8000
    ```

# Test

```zsh
$ python -m pytest
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