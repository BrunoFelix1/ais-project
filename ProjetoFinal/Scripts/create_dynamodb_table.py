"""
Script para criar a tabela CrimeAggregations no DynamoDB
Execute este script antes de usar o Worker
"""

import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def create_table():
    """Cria a tabela CrimeAggregations no DynamoDB"""
    
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    )
    
    table_name = 'CrimeAggregations'
    
    try:
        # Verifica se a tabela já existe
        existing_tables = [table.name for table in dynamodb.tables.all()]
        
        if table_name in existing_tables:
            print(f"✓ Tabela '{table_name}' já existe!")
            table = dynamodb.Table(table_name)
            print(f"  Status: {table.table_status}")
            print(f"  Criada em: {table.creation_date_time}")
            return
        
        # Cria a tabela
        print(f"Criando tabela '{table_name}'...")
        
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'bairro',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'bairro',
                    'AttributeType': 'S'  # String
                }
            ],
            BillingMode='PAY_PER_REQUEST'  # On-demand pricing
        )
        
        # Aguarda a tabela ser criada
        print("Aguardando a tabela ser criada...")
        table.wait_until_exists()
        
        print(f"✓ Tabela '{table_name}' criada com sucesso!")
        print(f"  Status: {table.table_status}")
        print("  Partition Key: bairro (String)")
        
    except Exception as e:
        print(f"✗ Erro ao criar tabela: {str(e)}")


if __name__ == '__main__':
    print("=== Criação de Tabela DynamoDB ===\n")
    create_table()
