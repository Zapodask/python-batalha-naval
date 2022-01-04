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

## Routes



## License

[MIT](https://api.github.com/licenses/mit)
