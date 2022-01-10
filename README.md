# Batalha naval com websockets

## Jogo clássico de tabuleiro para jogar com jogador aleatório

## Tecnologias utilizadas

* Python
* Aws
    * Lambda
    * Api-gateway

## Setup

1. Use o template.yaml no cloudformation
1. Preencha o .env com o nome do bucket com o código da lambda
1. Crie e inicie o ambiente virtual:
    ```shell
    python -m venv .venv

    .venv\Scripts\activate
    ```
1. Instalar dependências
    ```shell
    pip install -r requirements.txt
    ```
1. Enviar código para lambda
    ```shell
    python scripts\update.py
    ```

## Routes examples

* Encontrar jogo
    ```json
    {
        "action": "searchGame"
    }
    ```

* Posicionar barcos
    ```json
    {
        "action": "setBoats",
        "gameId": "43b3efb8-4989-417e-8ee7-7046cd6d14aa",
        "tug": "[
            ['A1', 'A2'],
            ['B1', 'B2'],
            ['C1', 'C2']
        ]",
        "destroyer": "[
            ['D1', 'D3'],
            ['E1', 'E3']
        ]",
        "cruiser": "[
            ['F1', 'F4'],
            ['G1', 'G4']
        ]",
        "aircraft_carrier": "[
            ['H1', 'H5']
        ]"
    }
    ```

* Atirar bomba
    ```json
    {
        "action": "shoot",
        "gameId": "43b3efb8-4989-417e-8ee7-7046cd6d14aa",
        "target": "J10"
    }
    ```

## License

[MIT](https://api.github.com/licenses/mit)
