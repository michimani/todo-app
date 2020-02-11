todo-app
===

Please see `docs/ARCHITECTURE.md` for architecture, and see [https://michimani.github.io/todo-app/todo-app-api-reference/](https://michimani.github.io/todo-app/todo-app-api-reference/) for API reference.



# Preparing

## Tools

- AWS CLI

    ```zsh
    $ aws --version
    aws-cli/1.17.7 Python/3.7.6 Darwin/18.7.0 botocore/1.14.9
    ```

- jq
    
- Python 3
    
    ```zsh
    $ python3 -V
    Python 3.7.6
    ```
    
    Creating a virtual environment of Python 3 is recommended. 
    
    ```zsh
    $ python3 -m venv .venv && source ./.venv/bin/activate
    ```
    
    The rest of this README assumes that you are working in that virtual environment.

- Python packages

    ```zsh
    $ pip install -r requirements.txt
    ```

- HTTPie
    
    This is a command line HTTP client that replaces curl. Although not required, it simplifies HTTP requests from the command line.
    
    [HTTPie – command line HTTP client](https://httpie.org/)

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
$ python -m pytest ./tests/1_unit_tests/
```

## API test

0. start DynamoDB local

    ```zsh
    $ sh ./scripts/start_local_db.sh
    ```

1. create table for test and insert test data

    ```zsh
    $ sh ./scripts/clean_db_for_api_tests.sh
    ```

2. run at local with stage `test`

    ```zsh
    $ chalice local --stage test
    ```
    
3. test

    ```zsh
    $ python -m pytest ./tests/2_api_tests/
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
    $ sh ./scripts/generate_api_key.sh user1 abcd1234
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

## Delete resources

1. delete chalice app

    ```zsh
    $ chalice delete --stage prod
    ```

2. delete CFn stacks

    ```zsh
    $ sh ./scripts/clean_aws_resources.sh
    ```