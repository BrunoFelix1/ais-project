import os
import boto3
from dotenv import load_dotenv
import tkinter as tk
from tkinter import filedialog

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION')

s3 = boto3.resource(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_DEFAULT_REGION
)

def upload_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Selecione o arquivo para upload")
    root.destroy()
    if not file_path or not os.path.isfile(file_path):
        print("Arquivo não selecionado ou não encontrado. Abortando upload.")
        return
    bucket = input("Nome do bucket de destino: ")
    key = input("Nome do arquivo no bucket (key): ")
    try:
        s3.Bucket(bucket).upload_file(file_path, key)
        print(f"Arquivo '{file_path}' enviado para '{bucket}/{key}'.")
    except Exception as e:
        print(f"Erro ao enviar arquivo: {e}")

def download_file():
    bucket = input("Nome do bucket de origem: ")
    print("Listando arquivos do bucket...")
    try:
        objetos = list(s3.Bucket(bucket).objects.all())
        if not objetos:
            print("Nenhum arquivo encontrado no bucket.")
            return
        print("Selecione o arquivo para download:")
        for idx, obj in enumerate(objetos, 1):
            print(f"{idx} - {obj.key}")
        while True:
            escolha = input(f"Digite o número do arquivo (1-{len(objetos)}): ")
            if escolha.isdigit() and 1 <= int(escolha) <= len(objetos):
                key = objetos[int(escolha)-1].key
                break
            else:
                print("Opção inválida. Tente novamente.")
        dest = os.path.join(os.path.dirname(__file__), key)
        s3.Bucket(bucket).download_file(key, dest)
        print(f"Arquivo '{key}' baixado de '{bucket}' para '{dest}'.")
    except Exception as e:
        print(f"Erro ao baixar arquivo: {e}")

def main():
    while True:
        print("\nO que deseja fazer?")
        print("1 - Upload para S3")
        print("2 - Download do S3")
        print("3 - Sair")
        action = input("Escolha uma opção (1/2/3): ")
        if action == "1":
            upload_file()
        elif action == "2":
            download_file()
        elif action == "3":
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    print("Iniciando interface S3...")
    main()
