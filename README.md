todo-app
===

Please see `docs/ARCHITECTURE.md` for architecture, and see [https://michimani.github.io/todo-app/todo-app-api-reference/](https://michimani.github.io/todo-app/todo-app-api-reference/) for API reference.



# Preparing

## Install tools

- AWS CLI

    ```zsh
    $ aws --version
    aws-cli/1.17.7 Python/3.7.6 Darwin/18.7.0 botocore/1.14.9
    ```
    
    Version 2.0.0 is available.
    
    ```zsh
    $ aws --version
    aws-cli/2.0.0 Python/3.7.4 Darwin/19.3.0 botocore/2.0.0dev4
    ```

- jq
    
- HTTPie
    
    This is a command line HTTP client that replaces curl. Although not required, it simplifies HTTP requests from the command line.
    
    [HTTPie – command line HTTP client](https://httpie.org/)

## Clone repository

1. Clone this repository

    ```zsh
    $ git clone https://github.com/michimani/todo-app.git
    $ cd todo-app
    ```

2. Creating a virtual environment of Python 3
    
    ```zsh
    $ python3 -V
    Python 3.7.6
    ```
    
    Creating a virtual environment of Python 3 is recommended. 
    
    ```zsh
    $ python3 -m venv .venv && source ./.venv/bin/activate
    ```
    
    The rest of this README assumes that you are working in that virtual environment.

3. Install Python packages

    ```zsh
    $ pip install -r requirements.txt
    ```

## Setup DynamoDB local

1. Download DynamoDB local from [DynamoDB (ダウンロード可能バージョン) - Amazon DynamoDB](https://docs.aws.amazon.com/ja_jp/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html)

2. Run following command to start DynamoDB local
  
    ```zsh
    $ export DYNAMODB_LOCAL_DIR=your_dynamo_db_local_path
    $ sh ./scripts/start_local_db.sh
    ```

3. Create table
  
    ```zsh
    $ aws dynamodb create-table \
    --cli-input-json file://local/dynamodb_local_schema.json \
    --endpoint-url http://localhost:8001
    ```

# Run at local

1. Start DynamoDB local

    ```zsh
    $ sh ./scripts/start_local_db.sh
    ```

2. Run following command to start app

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

0. Start DynamoDB local

    ```zsh
    $ sh ./scripts/start_local_db.sh
    ```

1. Create table for test and insert test data

    ```zsh
    $ sh ./scripts/clean_db_for_api_tests.sh
    ```

2. Run at local with stage `test`

    ```zsh
    $ chalice local --stage test
    ```
    
3. Test

    ```zsh
    $ python -m pytest ./tests/2_api_tests/
    ```

# Deploy to AWS

1. Create DynamoDB table

    ```zsh
    $ sh ./cfn/00-dynamodb.sh deploy
    ```

2. Deploy app

    ```zsh
    $ chalice deploy --stage prod
    ```

3. Create API Gateway Usage Plan

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

4. Generate API Key

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

5. Use custom domain (option)

    Before executing the following command, please do following actions.
    
    - create a host zone in Route 53
    - create a SSL certificate for the domain you want to use in ACM

    ```zsh
    $ export TD_ACM_ARN=your_acm_arn
    $ export TD_CUSTOM_DOMAIN_NAME=your_custom_domain_name
    $ export TD_DOMAIN_HOST_ZONE_ID=your_domain_host_zone_id
    $ sh ./cfn/02-api-custom-doman.sh deploy
    ```

## Delete resources

0. Delete AWS resources related to custom domain

    If you create resources for using custom domain, please delete them first.

    ```zsh
    $ aws cloudformation delete-stack --stack-name "TodoApiCustomDomain"
    ```

1. Delete chalice app

    ```zsh
    $ chalice delete --stage prod
    ```

2. Delete other AWS resources

    ```zsh
    $ sh ./scripts/clean_aws_resources.sh
    ```
