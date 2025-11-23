import stomp
import time
from dotenv import load_dotenv
from CrimeProcessor import CrimeProcessor

load_dotenv()

def main():
    """Função principal do worker"""
    print("=== Crime Processing Worker ===")
    print("Conectando ao ActiveMQ...")
    
    # Configurações
    ACTIVEMQ_HOST = 'localhost'
    ACTIVEMQ_PORT = 61613
    QUEUE_NAME = '/queue/crimes.processing'
    
    # Cria o listener
    processor = CrimeProcessor()
    
    # Conecta ao ActiveMQ
    conn = stomp.Connection([(ACTIVEMQ_HOST, ACTIVEMQ_PORT)])
    conn.set_listener('crime-processor', processor)
    conn.connect('admin', 'admin', wait=True)
    
    # Subscreve na fila
    conn.subscribe(destination=QUEUE_NAME, id=1, ack='auto')
    
    print(f"Worker conectado e aguardando mensagens na fila: {QUEUE_NAME}")
    print("Pressione CTRL+C para parar\n")
    
    try:
        # Mantém o worker rodando
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nEncerrando worker...")
        
        # Exibe estatísticas finais
        processor.print_statistics()
        
        # Desconecta
        conn.disconnect()
        print("Worker encerrado.")


if __name__ == '__main__':
    main()
