import boto3
import os
import shutil

from dotenv import load_dotenv


load_dotenv()

cwd = os.getcwd()

project_name = os.path.basename(cwd)
bucket_name = os.getenv("BUCKET_NAME")

s3_client = boto3.client("s3")
lambda_client = boto3.client("lambda", region_name="us-east-1")


class update:
    def __init__(self):
        self.updateS3()

        self.updateLambda()

    # Atualiza o código no bucket
    def updateS3(self):
        # Variáveis de diretório
        path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(path + "/../")
        dirs = os.listdir()

        # Remove resquícios da atualização anterior
        os.remove("build") if "build" in dirs else None
        os.remove("build.zip") if "build.zip" in dirs else None

        # Instalando as dependências
        os.system(
            f"pip3 install -r ./requirements.txt \
            --upgrade --target {cwd}/build/"
        )

        # Copiando arquivos
        to_move = ["index.py", "board.json"]
        [shutil.copyfile(file, f"build/{file}") for file in to_move]

        if "src" in dirs:
            shutil.copytree("src", "build/src")

        # Zipando código
        shutil.make_archive("build", "zip", "build")

        # Remover pasta
        shutil.rmtree("build")

        # Atualizando
        s3_client.upload_file(
            "build.zip",
            bucket_name,
            "build.zip",
            {"ContentType": "application/zip"},
        )

        # Remover arquivo zip
        os.remove("build.zip")

        print("S3 updated")

    # Atualiza a função lambda para o código no bucket
    def updateLambda(self):
        lambda_client.update_function_code(
            FunctionName=project_name,
            S3Bucket=bucket_name,
            S3Key="build.zip",
            Publish=True,
        )

        print("Lambda updated")


update()
