from src.services import apiGatewayClient as client


class Utils:
    def response(self, id: str, data: str):
        client.post_to_connection(ConnectionId=id, Data=data)
