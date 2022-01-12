import random
import json
import uuid
import ast

from datetime import datetime

from src.utils import Utils
from src.services import search_table, game_table


utils = Utils()


class Routes:
    def connect(self, id: str):
        return

    def disconnect(self, id: str):
        return

    def default(self, id: str):
        utils.response(id, "Action not allowed")

    def searchGame(self, id: str):
        scan = search_table.scan().get("Items")

        if scan != [] and scan[0].get("connectionId") != id:
            opponent = scan[0].get("connectionId")

            if opponent == id:
                utils.response(id, "você já está buscando um jogo")

                return False

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

            utils.response(
                [id, opponent],
                f"Oponente encontrado, gameId: {game_id}",
            )

            search_table.delete_item(Key={"connectionId": opponent})

        else:
            search_table.put_item(Item={"connectionId": id})

            utils.response(id, "Procurando jogo...")

            return True

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

        status, val = utils.validations(id, game_id)

        if status == False:
            utils.response(id, [val], True)
            return val

        game = val.get("game")
        blue_player = val.get("bluePlayer")
        red_player = val.get("redPlayer")
        side = val.get("side")

        errors = []
        validate_list = []

        if game.get(f"{side}Boats") != "[]":
            utils.response(id, "barcos já posicionados")
            return

        to_add_board = json.loads(game.get(f"{side}Side").replace("'", '"'))

        for validation in validation_list:
            if validation["value"] == None:
                errors.append(f"{validation['key']} é necessário")

        if errors != []:
            utils.response(id, str(errors))
            return

        for validation in validation_list:
            qty = validation["qty"]

            if len(validation["value"]) != qty:
                errors.append(f"{validation['key']} tem {qty} de quantidade")

        if errors != []:
            utils.response(id, str(errors))
            return

        for validation in validation_list:
            for boat in validation["value"]:
                if len(boat) == 2:
                    init_col = boat[0][0].upper()
                    final_col = boat[1][0].upper()

                    init_col_n = utils.getCol(init_col)
                    final_col_n = utils.getCol(final_col)

                    str_init_row = boat[0][1]
                    str_final_row = boat[1][1]

                    if str_init_row == "1":
                        try:
                            t = boat[0][2]

                            if t == "0":
                                str_init_row += t
                        except:
                            pass

                    if str_final_row == "1":
                        try:
                            t = boat[1][2]

                            if t == "0":
                                str_final_row += t
                        except:
                            pass

                    init_row = int(str_init_row)
                    final_row = int(str_final_row)

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

                        elif str_init_row == str_final_row:
                            i = init_col_n

                            while i <= final_col_n:
                                ret = f"{utils.getCol(i)}{str_final_row}"

                                if ret in validate_list:
                                    errors.append(f"{ret} já está em uso")

                                else:
                                    validate_list.append(ret)

                                i += 1

                        if errors != []:
                            utils.response(id, str(errors))

                            return

                        if init_col == final_col:
                            i = init_row

                            while i <= final_row:
                                to_add_board[init_col][str(i)] = 2

                                i += 1

                        if str_init_row == str_final_row:
                            i = init_col_n

                            while i <= final_col_n:
                                i_n = utils.getCol(i)

                                to_add_board[i_n][boat[1]] = 2

                                i += 1

                    else:
                        errors.append(
                            "um " + validation["key"] + " não possui o tamanho certo"
                        )

                else:
                    utils.response(id, "barcos são listas com 2 itens: inicio e fim")
                    return

        if errors != []:
            utils.response(id, str(errors))

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
            side == "blue" and game.get("redBoats") != "[]"
        ):
            utils.response(red_player, "você é o vermelho")
            utils.response(blue_player, "você é o azul")
            utils.response(
                [blue_player, red_player],
                f"começando o jogo,  {utils.translateSide(side)} começa",
            )

        else:
            utils.response(id, "aguardando o outro jogador")

        return True

    def shoot(self, id: str, body: dict):
        game_id = body.get("gameId")
        target = body.get("target")

        status, val = utils.validations(id, game_id)

        if status == False:
            utils.response(id, [val], True)
            return val

        game = val.get("game")
        blue_player = val.get("bluePlayer")
        red_player = val.get("redPlayer")
        side = val.get("side")

        i_side = "blue" if side == "red" else "red"
        t_side = utils.translateSide(side)

        if game.get("turn") != side:
            utils.response(id, "não é sua vez")
            return

        to_side_str = "to" + ("RedBlue" if side == "red" else "BlueRed") + "Side"

        board = json.loads((game.get(f"{i_side}Side")).replace("'", '"'))
        to_board = json.loads((game.get(to_side_str)).replace("'", '"'))
        boats = ast.literal_eval(game.get(f"{i_side}Boats"))

        if (len(target) == 3 and target[1] != "1") or len(target) != 2:
            utils.response(id, "movimento invalido")
            return

        col = target[0].upper()
        row = target[1]

        if row == "1":
            try:
                t = target[2]

                if t == "0":
                    row += t
            except:
                pass

        position = board[col][row]

        if position == 1 or position == 3:
            utils.response(id, "você já atacou este local")
            return

        if position == 0:
            board[col][row] = 1
            to_board[col][row] = 1

            utils.response(
                [red_player, blue_player],
                f"{t_side} jogou {col}{row} e acertou a água",
            )

        if position == 2:
            board[col][row] = 3
            to_board[col][row] = 3
            boats.remove(col + row)

            utils.response(
                [red_player, blue_player],
                f"{t_side} jogou {col}{row} e acertou um barco",
            )

            if boats == []:
                utils.response(
                    [red_player, blue_player],
                    f"{t_side} ganhou",
                )

                game_table.remove_item(Key={"gameId": game_id})
                return

        game_table.update_item(
            Key={"gameId": game_id},
            UpdateExpression=f"SET #{i_side}Side=:s, #{to_side_str}=:t, #{i_side}Boats=:b, #turn=:u",
            ExpressionAttributeNames={
                f"#{i_side}Side": f"{i_side}Side",
                f"#{to_side_str}": to_side_str,
                f"#{i_side}Boats": f"{i_side}Boats",
                "#turn": "turn",
            },
            ExpressionAttributeValues={
                ":s": str(board),
                ":t": str(to_board),
                ":b": str(boats),
                ":u": i_side,
            },
        )

        return True
