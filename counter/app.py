import json
import os
from decimal import Decimal
import boto3

def incrementdbcounter(path):

    # only use DYNAMODB_ENDPOINT if specified and not empty - for localstack development
    if os.getenv("DYNAMODB_ENDPOINT"):
        dynamodb = boto3.resource('dynamodb', endpoint_url=os.environ['DYNAMODB_ENDPOINT'])
    else:
        dynamodb = boto3.resource('dynamodb')

    # tablename specified in ENV
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # update counter call to dynamodb
    response = table.update_item(
        Key={
            'path': path
        },
        UpdateExpression="ADD hits :inc",
        ExpressionAttributeValues={
            ':inc': Decimal(1)
        },
        ReturnValues="UPDATED_NEW",
    )
    return response

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    path = event["queryStringParameters"]["path"]

    updatednewrecord = incrementdbcounter(path)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "count": int(updatednewrecord["Attributes"]["hits"])
        }),
    }
