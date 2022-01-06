import random
import json
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

        if scan != [] and scan[0].get("connectionId") != id:
            opponent = scan[0].get("connectionId")

            if opponent == id:
                self.utils.response(id, "você já está buscando um jogo")
                return

            game_id = str(uuid.uuid4())

            with open("board.json", "r") as f:
                board = str(json.loads(f.read()))

                data = {
                    "gameId": game_id,
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

            self.utils.response(
                [id, opponent],
                f"Oponente encontrado, gameId: {game_id}",
            )

            search_table.delete_item(Key={"connectionId": opponent})

        else:
            search_table.put_item(Item={"connectionId": id})

            self.utils.response(id, "Procurando jogo...")

    def setBoats(self, id: str, body: dict):
        game_id = body.get("gameId")
        tug = body.get("tug")
        destroyer = body.get("destroyer")
        cruiser = body.get("cruiser")
        aircraft_carrier = body.get("aircraft_carrier")

        validation_list = [
            {"key": "tug", "value": tug, "qty": 3, "size": 2},
            {"key": "destroyer", "value": destroyer, "qty": 2, "size": 3},
            {"key": "cruiser", "value": cruiser, "qty": 2, "size": 4},
            {"key": "aircraft_carrier", "value": aircraft_carrier, "qty": 1, "size": 5},
        ]

        game = dict(game_table.get_item(Key={"gameId": game_id})["Item"])
        blue_player = game.get("bluePlayer")
        red_player = game.get("redPlayer")

        errors = []
        validate_list = []

        side = ""

        if game.get("redPlayer") == id:
            side = "red"

        elif game.get("bluePlayer") == id:
            side = "blue"

        else:
            self.utils.response(id, "você não está nesse jogo")
            return

        to_add_board = game.get(f"{side}Side")

        # Validate if not None
        for validation in validation_list:
            if validation["value"] == None:
                errors.append(f"{validation['key']} é necessário")

        if errors != []:
            self.utils.response(id, str(errors))
            return

        # Validate quantity
        for validation in validation_list:
            qty = validation["qty"]

            if len(validation["value"]) != qty:
                errors.append(f"{validation['key']} tem {qty} de quantidade")

        if errors != []:
            self.utils.response(id, str(errors))
            return

        for validation in validation_list:
            for boat in validation["value"]:
                if len(boat) == 2:
                    for b in boat:
                        init_col = b[0].upper()
                        final_col = b[0].upper()

                        init_col_n = self.utils.getCol(init_col)
                        final_col_n = self.utils.getCol(final_col)

                        init_row = int(b[1])
                        final_row = int(b[1])

                        if (
                            final_row - init_row + 1 == validation["size"]
                            or final_col_n - init_col_n + 1 == validation["size"]
                        ):
                            if init_col == final_col:
                                i = init_row

                                while i <= final_row:
                                    ret = f"{init_col}{i}"

                                    if ret in validate_list:
                                        errors.append(f"{ret} já está em uso")

                                    else:
                                        validate_list.append(ret)

                                    i += 1

                            elif b[1] == b[1]:
                                i = init_col_n

                                while i <= final_col_n:
                                    ret = f"{self.utils.getCol(i)}{b[1]}"

                                    if ret in validate_list:
                                        errors.append(f"{ret} já está em uso")

                                    else:
                                        validate_list.append(ret)

                                    i += 1

                            if errors != []:
                                self.utils.response(id, str(errors))

                                return

                            if init_col == final_col:
                                i = init_row

                                while i <= final_row:
                                    to_add_board[init_col][str(i)] = 2

                                    i += 1

                            if b[1] == b[1]:
                                i = init_col_n

                                while i <= final_col_n:
                                    i_n = self.utils.getCol(i)

                                    to_add_board[i_n][boat[1]] = 2

                                    i += 1

                else:
                    self.utils.response(
                        id, "barcos são listas com 2 itens: inicio e fim"
                    )
                    return

        game_table.update_item(
            Key={"gameId": game_id},
            UpdateExpression=f"SET #{side}Side=:s, #{side}Boats=:b",
            ExpressionAttributeNames={
                f"#{side}Side": f"{side}Side",
                f"#{side}Boats": f"{side}Boats",
            },
            ExpressionAttributeValues={
                ":s": str(to_add_board),
                ":b": str(validate_list),
            },
        )

        if (
            side == "red"
            and game.get("blueBoats") != "[]"
            or side == "blue"
            and game.get("redeBoats") != "[]"
        ):
            self.utils.response(red_player, "você é o vermelho")
            self.utils.response(blue_player, "você é o azul")
            self.utils.response(
                [blue_player, red_player],
                f"Começando o jogo, "
                + ("vermelho" if game.get("turn") == "red" else "azul")
                + " começa",
            )

        else:
            self.utils.response(id, "aguardando o outro jogador")
