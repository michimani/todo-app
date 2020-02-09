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
    --cli-input-json file://local/dynamodb_local_schema.json \
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

## Unit test

```zsh
$ python -m pytest ./tests/0_unit_tests/
```

## API test

0. start DynamoDB local

    ```zsh
    $ sh start_local_db.sh
    ```

1. create table for test

    If *todos_test* table has already exists, delete it.
    
    ```zsh
    $ aws dynamodb delete-table --table-name todos_test \
    --endpoint-url http://localhost:8001
    ```
    
    Create *todos_test* table.

    ```zsh
    $ aws dynamodb create-table --cli-input-json file://local/dynamodb_local_for_test_schema.json \
    --endpoint-url http://localhost:8001
    ```

2. insert test data

    ```zsh
    $ aws dynamodb batch-write-item --request-items file://local/initial_data.json \
    --endpoint-url http://localhost:8001
    ```

3. run at local with stage `test`

    ```zsh
    $ chalice local --stage test
    ```
    
4. test

    ```zsh
    $ python -m pytest ./tests/1_api_tests/
    ```

# Deploy to AWS

1. create DynamoDB table

    ```zsh
    $ sh ./cfn/00-dynamodb.sh deploy
    ```

2. deploy app

    ```zsh
    $ chalice deploy --stage prod
    ```

3. create API Gateway Usage Plan

    ```zsh
    $ sh ./cfn/01-api-usage-plan.sh deploy
    ```

    If creating usage plan successfully, ID of created usage plan will be outputed. 

    ```
    ...
    ----------------------------------------------

    Following string is ID of created usage plan. Use it for creating api key belongs to an usage plan. Use it in next step.

    abcd1234
    ```

4. generate API Key

    ```zsh
    $ sh ./generate_api_key.sh user1 abcd1234
    API Key generated successfully.
    {
        "id": "abscdefg123",
        "value": "abcdefghijklmnopqrstuvwxyz1234567890",
        "name": "user1",
        "enabled": true,
        "createdDate": 1580802241,
        "lastUpdatedDate": 1580802241,
        "stageKeys": []
    }
    ```

