from src.services import apiGatewayClient as client, game_table


class Utils:
    def response(self, id: str or list, msg: str or list, err: bool = False) -> None:
        """
        Envia mensagem para o usuário

        :param id: id de conexão do usuário
        :param msg: mensagem ou lista de erros
        :param err: se a mensagem for uma lista de erros
        :type id: string ou lista
        :type msg: string ou lista
        :type err: bool
        """
        ret = {}

        if type(id) == str:
            id = [id]

        if err:
            ret["errors"] = []

            for m in msg:
                ret["errors"].append(m.capitalize())
        else:
            ret["message"] = msg.capitalize()

        for i in id:
            client.post_to_connection(ConnectionId=i, Data=str(ret))

    def validations(self, id: str, game_id: str) -> bool and dict or str:
        """
        Validação básica

        :param id: id de conexão do usuário
        :param game_id: id do jogo
        :type id: string
        :type game_id: string
        :return: status do retorno e dict com game, blue player, red player e side ou erro
        :rtype: bool, dict ou string
        """
        ret = {}

        game = game_table.get_item(Key={"gameId": game_id}).get("Item")

        if game is None:
            return False, "jogo não existe ou já acabou"

        ret["game"] = game

        ret["bluePlayer"] = game.get("bluePlayer")
        ret["redPlayer"] = game.get("redPlayer")

        if ret["redPlayer"] == id:
            ret["side"] = "red"

        elif ret["bluePlayer"] == id:
            ret["side"] = "blue"

        else:
            return False, "você não está neste jogo"

        return True, ret

    def getCol(self, l: str or int) -> str or int:
        """
        Transforma a letra para seu respectivo número em ordem alfabética e vice-versa

        :param l: letra ou número para transformar
        :type l: string ou int
        :return: letra ou número para transformado
        :rtype: string ou int
        """
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        if type(l) == str:
            l = l.upper()

            if l in letters:
                index = letters.index(l)

                return numbers[index]
            else:
                return "letra inválida, escolha de a-j"

        elif type(l) == int:
            if l in numbers:
                index = numbers.index(l)

                return letters[index]
            else:
                return "numero inválido, escolha de 1-10"

    def translateSide(self, s: str) -> str:
        """
        Transforma o lado do jogador de inglês para português

        :param s: lado em inglês
        :type s: string = 'red' ou 'blue'
        :return: lado em português
        :rtype: string = 'vermelho' ou 'azul'
        """
        t = {"red": "vermelho", "blue": "azul"}

        try:
            return t[s]
        except KeyError:
            return "lado inválido"
