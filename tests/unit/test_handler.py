import json
import pytest
import boto3
import os
from moto import mock_dynamodb2

from counter import app

@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""
    with open("events/event.json") as json_file:
        return json.load(json_file)

def createtable():

    table = os.environ['DYNAMODB_TABLE']

    dynamodb = boto3.resource('dynamodb')

    dynamodb.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'path',
                'AttributeType': 'S'
            },
        ],
        KeySchema=[
            {
                'AttributeName': 'path',
                'KeyType': 'HASH'
            },
        ],
        TableName=table,
        BillingMode = "PAY_PER_REQUEST"
    )

@mock_dynamodb2
def test_lambda_handler(apigw_event, monkeypatch):
    
    monkeypatch.setenv('DYNAMODB_TABLE', 'test')

    createtable()

    response = app.lambda_handler(apigw_event, "")
    data = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert data["count"] == 1
    
    response = app.lambda_handler(apigw_event, "")
    data = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert data["count"] == 2
    