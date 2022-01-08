from typing import Any
from src.services import apiGatewayClient as client, game_table


class Utils:
    def response(self, id: str or list, data: str):
        if type(id) == str:
            id = [id]

        for i in id:
            client.post_to_connection(ConnectionId=i, Data=data)

    def getPlayerSide(self, id: str, game_id: str):
        res = game_table.get_item(Key={"gameId": game_id})

        if res["redPlayer"] == id:
            return "red"

        elif res["bluePlayer"] == id:
            return "blue"

        else:
            return "você não está nesse jogo"

    def getCol(self, letter: str or int):
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        if type(letter) == str:
            index = letters.index(letter)

            return numbers[index]
        else:
            index = numbers.index(letter)

            return letters[index]
