from boto3 import resource, client
from os import getenv


dynamodb = resource("dynamodb")

search_table = dynamodb.Table(getenv("SEARCH_GAME_TABLE"))
game_table = dynamodb.Table(getenv("GAME_TABLE"))


endpoint_url = f'{getenv("API_ENDPOINT").replace("wss", "https", 1)}'

apiGatewayClient = client(
    "apigatewaymanagementapi",
    endpoint_url=endpoint_url,
)
