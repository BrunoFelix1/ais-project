import os
import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

table = dynamodb.Table('Aluno')
print(table.creation_date_time) 

def create_aluno():
    nome = input("Nome: ")
    curso = input("Curso: ")
    idade = input("Idade: ")

    table.put_item(
        Item={
            'name': nome,
            'curso': curso,
            'idade': idade
        }
    )
    print("criou")
    
def read_alunos():
    response = table.scan()
    alunos = response.get('Items', [])
    for aluno in alunos:
        print("O aluno é esse aí:", aluno)
        
def update_aluno():
    nome = input("Nome do aluno a ser atualizado: ")
    novo_curso = input("Novo curso: ")
    novo_idade = input("Nova idade: ")

    table.update_item(
        Key={'name': nome},
        UpdateExpression='SET curso = :val1, idade = :val2',
        ExpressionAttributeValues={':val1': novo_curso, ':val2': novo_idade}
    )
    print("atualizou")
    
def delete_aluno():
    nome = input("Nome do aluno a ser deletado: ")

    table.delete_item(
        Key={'name': nome}
    )
    print("deletou")
    
def main():
    while True:
        print("\nEscolha uma operação:")
        print("1. Criar Aluno")
        print("2. Ler Alunos")
        print("3. Atualizar Aluno")
        print("4. Deletar Aluno")
        print("5. Sair")

        choice = input("Opção: ")

        if choice == '1':
            create_aluno()
        elif choice == '2':
            read_alunos()
        elif choice == '3':
            update_aluno()
        elif choice == '4':
            delete_aluno()
        elif choice == '5':
            break
        else:
            print("Opção inválida. Tente novamente.")
            
main()