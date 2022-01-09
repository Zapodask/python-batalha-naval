import random
import json
import uuid
import ast

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
            {
                "key": "tug",
                "value": ast.literal_eval(tug),
                "qty": 3,
                "size": 2,
            },
            {
                "key": "destroyer",
                "value": ast.literal_eval(destroyer),
                "qty": 2,
                "size": 3,
            },
            {
                "key": "cruiser",
                "value": ast.literal_eval(cruiser),
                "qty": 2,
                "size": 4,
            },
            {
                "key": "aircraft_carrier",
                "value": ast.literal_eval(aircraft_carrier),
                "qty": 1,
                "size": 5,
            },
        ]

        game = game_table.get_item(Key={"gameId": game_id}).get("Item")

        if game == None:
            self.utils.response(id, "jogo não existe ou já acabou")
            return

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

        to_add_board = json.loads(game.get(f"{side}Side").replace("'", '"'))

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
                    init_col = boat[0][0].upper()
                    final_col = boat[1][0].upper()

                    init_col_n = self.utils.getCol(init_col)
                    final_col_n = self.utils.getCol(final_col)

                    init_row = int(boat[0][1])
                    final_row = int(boat[1][1])

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

                        elif boat[0][1] == boat[1][1]:
                            i = init_col_n

                            while i <= final_col_n:
                                ret = f"{self.utils.getCol(i)}{boat[1][1]}"

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

                        if boat[0][1] == boat[1][1]:
                            i = init_col_n

                            while i <= final_col_n:
                                i_n = self.utils.getCol(i)

                                to_add_board[i_n][boat[1]] = 2

                                i += 1

                    else:
                        print(
                            f"init_row: {init_row}, final_row: {final_row}, init_col_n: {init_col_n}, final_col_n: {final_col_n}, validation_size: {type(validation['size'])}"
                        )
                        errors.append(
                            "um " + validation["key"] + " não possui o tamanho certo"
                        )

                else:
                    self.utils.response(
                        id, "barcos são listas com 2 itens: inicio e fim"
                    )
                    return

        if errors != []:
            self.utils.response(id, str(errors))

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

        if (side == "red" and game.get("blueBoats") != "[]") or (
            side == "blue" and game.get("redeBoats") != "[]"
        ):
            self.utils.response(red_player, "você é o vermelho")
            self.utils.response(blue_player, "você é o azul")
            self.utils.response(
                [blue_player, red_player],
                f"começando o jogo, "
                + ("vermelho" if game.get("turn") == "red" else "azul")
                + " começa",
            )

        else:
            self.utils.response(id, "aguardando o outro jogador")

    def move(self, id: str, body: dict):
        game_id = body.get("gameId")
        target = body.get("target")

        side = self.utils.getPlayerSide(id, game_id)
        i_side = "blue" if side == "red" else "red"

        game = game_table.get_item(game_id)["Item"]

        if game == []:
            self.utils.response(id, "jogo não encontrado")
            return

        to_side_str = "to" + ("RedBlue" if side == "red" else "BlueRed") + "Side"

        board = dict(game.get(f"{i_side}Side"))
        to_board = dict(game.get(to_side_str))
        boats = list(game.get(f"{i_side}Boats"))

        if len(target) != 2:
            self.utils.response(id, "movimento invalido")
            return

        col = target[0].upper()
        row = target[1]

        position = board[col][row]

        if position == 1 or position == 3:
            self.utils.response(id, "você já atacou este local")
            return

        if position == 0:
            board[col][row] = 1
            to_board[col][row] = 1

            self.utils.response(
                [game.get("redPlayer"), game.get("bluePlayer")],
                ("vermelho" if side == "red" else "azul")
                + f" jogou {col}{row} e acertou a água",
            )

        if position == 2:
            board[col][row] = 3
            to_board[col][row] = 3
            boats.remove(f"{col}{row}")

            self.utils.response(
                [game.get("redPlayer"), game.get("bluePlayer")],
                ("vermelho" if side == "red" else "azul")
                + f" jogou {col}{row} e acertou um barco",
            )

            if boats == []:
                self.utils.response(
                    [game.get("redPlayer"), game.get("bluePlayer")],
                    ("vermelho" if side == "red" else "azul") + " ganhou",
                )

                game_table.remove_item(Key={"gameId": game_id})
                return

        game.update_item(
            Key={"gameId": game_id},
            UpdateExpression=f"SET #{i_side}Side=:s, #{to_side_str}=:t, #{i_side}Boats=:b",
            ExpressionAttributeNames={
                f"#{i_side}Side": f"{i_side}Side",
                f"#{to_side_str}": to_side_str,
                f"#{i_side}Boats": f"{i_side}Boats",
            },
            ExpressionAttributeValues={
                ":s": str(board),
                ":t": str(to_board),
                ":b": str(boats),
            },
        )
