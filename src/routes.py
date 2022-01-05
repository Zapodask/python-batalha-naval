import random
import uuid

from datetime import datetime

from src.utils import Utils
from src.services import search_table, game_table


class Routes:
    utils = Utils()

    def connect(self, id: str):
        return

    def disconnect(self, id: str):
        return

    def default(self, id: str):
        self.utils.response(id, "Action not allowed")

    def searchGame(self, id: str):
        scan = search_table.scan().get("Items")

        if scan != []:
            opponent = scan[0].get("connectionId")

            self.utils.response([id, opponent], "Oponente encontrado")

            with open("board.json", "r") as f:
                board = str(f.read())

                data = {
                    "id": str(uuid.uuid4()),
                    "turn": random.choice(["red", "blue"]),
                    "redPlayer": id,
                    "bluePlayer": opponent,
                    "redSide": board,
                    "blueSide": board,
                    "toRedBlueSide": board,
                    "toBlueRedSide": board,
                    "redBoats": "[]",
                    "blueBoats": "[]",
                    "createdAt": str(datetime.now()),
                }

                game_table.put_item(Item=data)

            search_table.delete_item(Key={"connectionId": opponent})

        else:
            search_table.put_item(Item={"connectionId": id})

            self.utils.response(id, "Procurando jogo...")
