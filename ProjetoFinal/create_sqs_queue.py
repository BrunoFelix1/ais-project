"""
Script para criar a fila SQS para processamento de crimes
Execute este script antes de usar o Worker
"""

import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def create_sqs_queue():
    """Cria a fila SQS para processamento de crimes"""
    
    sqs = boto3.client(
        'sqs',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    )
    
    queue_name = 'crimes-processing-queue'
    
    try:
        # Tenta obter a fila existente
        try:
            response = sqs.get_queue_url(QueueName=queue_name)
            queue_url = response['QueueUrl']
            print(f"✓ Fila '{queue_name}' já existe!")
            print(f"  URL: {queue_url}")
            return queue_url
        except sqs.exceptions.QueueDoesNotExist:
            pass
        
        # Cria a fila
        print(f"Criando fila SQS '{queue_name}'...")
        
        response = sqs.create_queue(
            QueueName=queue_name,
            Attributes={
                'VisibilityTimeout': '300',  # 5 minutos
                'MessageRetentionPeriod': '345600',  # 4 dias
                'ReceiveMessageWaitTimeSeconds': '20',  # Long polling
                'DelaySeconds': '0'
            }
        )
        
        queue_url = response['QueueUrl']
        
        print(f"✓ Fila '{queue_name}' criada com sucesso!")
        print(f"  URL: {queue_url}")
        print(f"SQS_QUEUE_URL={queue_url}")
        
        return queue_url
        
    except Exception as e:
        print(f"✗ Erro ao criar fila: {str(e)}")
        return None


if __name__ == '__main__':
    print("=== Criação de Fila SQS ===\n")
    create_sqs_queue()
