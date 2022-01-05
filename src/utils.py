from src.services import apiGatewayClient as client


class Utils:
    def response(self, id: str or list, data: str):
        if type(id) == str:
            id = [id]

        for i in id:
            client.post_to_connection(ConnectionId=i, Data=data)
