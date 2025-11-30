import json
import os
import time
import boto3
from dotenv import load_dotenv
from CrimeProcessor import CrimeProcessor

load_dotenv()

def main():
    """Função principal do worker"""
    print("=== Crime Processing Worker (SQS) ===")
    print("Conectando ao Amazon SQS...")
    
    # Configurações
    queue_url = os.getenv('SQS_QUEUE_URL')
    region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    
    if not queue_url:
        print("ERRO: Variável de ambiente SQS_QUEUE_URL não configurada!")
        return
    
    # Cria cliente SQS
    sqs = boto3.client(
        'sqs',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=region
    )
    
    # Cria o processador
    processor = CrimeProcessor()
    
    print(f"Worker conectado e aguardando mensagens na fila: {queue_url}")
    print("Pressione CTRL+C para parar\n")
    
    try:
        # Loop de processamento
        while True:
            # Recebe mensagens (long polling de 20 segundos)
            response = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=10,  # Processa até 10 mensagens por vez
                WaitTimeSeconds=20,  # Long polling
                AttributeNames=['All'],
                MessageAttributeNames=['All']
            )
            
            messages = response.get('Messages', [])
            
            if not messages:
                print(".", end="", flush=True)  # Indica que está aguardando
                continue
            
            print(f"\nRecebidas {len(messages)} mensagens")
            
            # Processa cada mensagem
            for message in messages:
                try:
                    # Parse do corpo da mensagem
                    crime_data = json.loads(message['Body'])
                    
                    # Processa o crime
                    processor.process_crime(crime_data)
                    
                    # Remove a mensagem da fila após processamento bem-sucedido
                    sqs.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=message['ReceiptHandle']
                    )
                    
                except Exception as e:
                    print(f"Erro ao processar mensagem: {str(e)}")
                    # Mensagem não é deletada e volta para a fila após visibility timeout
            
    except KeyboardInterrupt:
        print("\n\nEncerrando worker...")
        
        # Exibe estatísticas finais
        processor.print_statistics()
        
        print("Worker encerrado.")


if __name__ == '__main__':
    main()
