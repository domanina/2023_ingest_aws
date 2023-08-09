import copy
import allure
import jwt
import boto3

from http import HTTPStatus
from typing import Optional
from requests import Response
from config.config import SECRET
from consts import consts
from db.db_reader import DBReader
from tools.helper import make_graphql_boby, check_status_code, not_empty_wait
from tools.logger import get_logger

logger = get_logger(name="main_logger")
db_reader = DBReader()


def meta3_request(item: str, meta3_api_client) -> Response:
    with allure.step("...."):
        token = copy.deepcopy(TOKEN)
        token["smth_ids"] = {item: {}}
        encoded_jwt = jwt.encode(token, SECRET, headers=TOKEN_HEADERS)
        response = meta3_api_client.get_meta3_data(params={"token": encoded_jwt})
    check_status_code(response, HTTPStatus.OK)
    return response


def ingest(id: str, test_url: str, md5_test: str, meta1_api_client) -> str:
    variables = copy.deepcopy(VARIABLES)
    variables["..."]["..."] = id
    variables["..."]["..."]["url"] = test_url
    variables["..."]["..."]["md5"] = md5_test

    body = make_graphql_boby(QUERY, variables)
    with allure.step("POST request to DMS to updateImage"):
        response = meta1_api_client.post_meta1_data(payload=body, headers=HEADERS)
        check_status_code(response, HTTPStatus.OK)
        image_id = response.json()['data']['updateImage']['content_id']
    return image_id


def get_status(payload: str, meta2_api_client) -> str:
    response = meta1_api_client.post_meta2_data(payload=payload, headers=HEADERS)
    check_status_code(response, HTTPStatus.OK)
    ingest_status = response.json()['..']['..']['status']
    return ingest_status


def wait_status_success(id: str, meta2_api_client):
    with allure.step("..."):
        variables = copy.deepcopy(VARIABLES)
        variables["id"] = id
        body = make_graphql_boby(QUERY, variables)
        response = not_empty_wait(lambda: get_status(body, meta2_api_client))
    return response


def sqs_request(message_body: str, sqs_url: str, message_group_id: Optional[str] = None, message_deduplication_id: Optional[str] = None) -> str:
    with allure.step("Set up AWS Credentials and Region and create SQS session"):
        sqs = boto3.resource('sqs', region_name="", endpoint_url="")
        queue = sqs.Queue(sqs_url)
        logger.info(f"{consts.Colors.GREEN.value}Send message to: {consts.SQS_NLD_PREPROD_URL}")
        logger.info(f"Message body is : {message_body}{consts.Colors.BLACK.value}")
        if message_group_id and message_deduplication_id is not None:
            response = queue.send_message(MessageBody=message_body,
                                          MessageGroupId=message_group_id,
                                          MessageDeduplicationId=message_deduplication_id)
        else:
            response = queue.send_message(MessageBody=message_body)
            assert response["ResponseMetadata"]["HTTPStatusCode"] == HTTPStatus.OK, \
            f"Test failed. HTTP status is : {response['ResponseMetadata']['HTTPStatusCode']}, " \
            f"x-amzn-requestid is: {response['ResponseMetadata']['x-amzn-requestid']}"
        message_id = (response['MessageId'])
        logger.info(f"Got message_id from SQS : [{message_id}]")
    return message_id


def s3_request(s3_url: str) -> dict:
    with allure.step("Check s3 location"):
        s3_bucket = s3_url.split('/')[3]
        s3_key = s3_url.split(s3_bucket)[1][1:]
        s3client = boto3.client('s3')
        logger.info(f"S3 Bucket: {s3_bucket}")
        logger.info(f"S3 Key: {s3_key}")
        response = s3client.head_object(Bucket=s3_bucket, Key=s3_key)
        logger.info(f"Response is: {response}")
    return response
