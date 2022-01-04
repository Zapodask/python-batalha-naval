from boto3 import resource, client
from os import getenv


table = resource("dynamodb").Table(getenv("USERS_DB"))

endpoint_url = (
    f'{getenv("API_ENDPOINT").replace("wss", "https", 1)}/{getenv("STAGE_NAME")}'
)

apiGatewayClient = client(
    "apigatewaymanagementapi",
    endpoint_url=endpoint_url,
)
