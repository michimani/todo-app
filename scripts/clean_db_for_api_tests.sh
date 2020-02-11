aws dynamodb delete-table --table-name todos_test --endpoint-url http://localhost:8001

aws dynamodb create-table --cli-input-json file://local/dynamodb_local_for_test_schema.json --endpoint-url http://localhost:8001

aws dynamodb batch-write-item --request-items file://local/initial_data.json --endpoint-url http://localhost:8001