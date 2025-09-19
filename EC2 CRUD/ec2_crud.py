import boto3
import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
    print("Credenciais não encontradas no .env")
    exit(1)

ec2 = boto3.resource(
    "ec2",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

print("Recurso de EC2 inicializado!")

def listar_instancias():
    print("\n=== Lista de instâncias ===")
    for instance in ec2.instances.all():
        name = next((tag["Value"] for tag in (instance.tags or []) if tag["Key"] == "Name"), "Sem nome")
        print(f"ID: {instance.id} | Nome: {name} | State: {instance.state['Name']} | IP: {instance.public_ip_address}")

def criar_instancia():
    nome = input("Nome da instância: ")
    tipo = input("Tipo da instância (default: t3.micro): ") or "t3.micro"
    key_name = input("Nome da key pair para SSH (deve existir na AWS): ") # adicionar no dotenv isso
    sg_id = input("ID do Security Group já criado na AWS (liberado para SSH): ")

    instance = ec2.create_instances(
        ImageId="ami-0c02fb55956c7d316",  
        MinCount=1,
        MaxCount=1,
        InstanceType=tipo,
        KeyName=key_name,
        SecurityGroupIds=[sg_id],
        TagSpecifications=[{
            "ResourceType": "instance",
            "Tags": [{"Key": "Name", "Value": nome}]
        }]
    )[0]

    print(f"Instância criada: {instance.id}")
    print("Aguarde a inicialização e obtenha o IP público para conectar via SSH:")
    print("Exemplo de comando:")
    print("ssh -i /caminho/para/sua/key.pem ubuntu@<IP_PUBLICO>")

def iniciar_instancia():
    id = input("ID da instância: ")
    ec2.Instance(id).start()
    print(f"Iniciando instância {id}...")

def parar_instancia():
    id = input("ID da instância: ")
    ec2.Instance(id).stop()
    print(f"Parando instância {id}...")

def terminar_instancia():
    id = input("ID da instância: ")
    ec2.Instance(id).terminate()
    print(f"Encerrando instância {id}...")

def menu():
    while True:
        print("\n=== Menu EC2 CRUD ===")
        print("1. Listar instâncias")
        print("2. Criar instância")
        print("3. Iniciar instância")
        print("4. Parar instância")
        print("5. Encerrar instância")
        print("0. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            listar_instancias()
        elif escolha == "2":
            criar_instancia()
        elif escolha == "3":
            iniciar_instancia()
        elif escolha == "4":
            parar_instancia()
        elif escolha == "5":
            terminar_instancia()
        elif escolha == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()
