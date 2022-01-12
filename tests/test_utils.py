from src.utils import Utils


utils = Utils()


def test_getCol():
    send_letter = utils.getCol("c")

    send_number = utils.getCol(7)

    assert send_letter == 3 and send_number == "G"


def test_getCol_errors():
    send_invalid_letter = utils.getCol("S")

    send_invalid_number = utils.getCol(21)

    assert (
        send_invalid_letter == "letra inválida, escolha de a-j"
        and send_invalid_number == "numero inválido, escolha de 1-10"
    )


def test_translateSide():
    send_red = utils.translateSide("red")

    send_blue = utils.translateSide("blue")

    send_none = utils.translateSide("")

    assert (
        send_red == "vermelho" and send_blue == "azul" and send_none == "lado inválido"
    )
