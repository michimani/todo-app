from boto3.dynamodb.conditions import Key, Attr
import boto3
import os

endpoint = os.environ.get('DB_ENDPOINT')
table_name = os.environ.get('DB_TABLE_NAME')


def get_db():
    if endpoint:
        resource = boto3.resource('dynamodb', endpoint_url=endpoint)
    else:
        resource = boto3.resource('dynamodb')

    return resource.Table(table_name)


def get_table_name():
    return table_name


def get_todos(user_id):
    db = get_db()
    return db.query(
        KeyConditionExpression=Key('user_id').eq(user_id))


def get_todos_with_done(user_id, done):
    db = get_db()
    return db.query(
        IndexName='FilterDoneIndex',
        KeyConditionExpression=Key('user_id').eq(user_id) &
        Key('l_idx_done').begins_with(done + '#')
    )


def get_todo(user_id, todo_id):
    db = get_db()
    return db.get_item(Key={'user_id': user_id, 'todo_id': todo_id})


def update_todo(user_id, todo_id, patch_data):
    update_exp_set = ''
    update_exp_remove = ''
    exp_attr_names = {}
    exp_attr_values = {}
    for patch_attr in patch_data.keys():
        exp_attr_names['#' + patch_attr] = patch_attr
        if patch_data[patch_attr] != '':
            update_exp_set += 'set ' if update_exp_set == '' else ', '
            update_exp_set += '#{attr_name} = :new_{attr_name}'.format(
                attr_name=patch_attr)
            exp_attr_values[':new_' +
                            patch_attr] = patch_data[patch_attr]
        else:
            # 値が空文字の場合は項目を削除する
            update_exp_remove += '\n remove ' if update_exp_remove == '' else ', '
            update_exp_remove += '#{attr_name}'.format(attr_name=patch_attr)

    update_expression = update_exp_set + update_exp_remove

    db = get_db()
    return db.update_item(Key={'user_id': user_id, 'todo_id': todo_id},
                          UpdateExpression=update_expression,
                          ConditionExpression=Attr('user_id').eq(user_id) &
                          Attr('todo_id').eq(todo_id),
                          ExpressionAttributeNames=exp_attr_names,
                          ExpressionAttributeValues=exp_attr_values,
                          ReturnValues='ALL_NEW')


def put_todo(todo_data):
    db = get_db()
    return db.put_item(
        Item=todo_data, ConditionExpression=Attr('todo_id').not_exists())


def delete_todo(user_id, todo_id):
    db = get_db()
    return db.delete_item(Key={'user_id': user_id, 'todo_id': todo_id},
                          ReturnValues='ALL_OLD')
