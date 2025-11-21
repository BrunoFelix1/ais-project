import csv
import json
import stomp
from typing import Dict, Any
from werkzeug.datastructures import FileStorage
from models.crime import Crime
from io import StringIO


class CrimeService:
    """Serviço para processar upload de CSV e enviar mensagens para a fila"""
    
    def __init__(self, activemq_host='localhost', activemq_port=61613):
        self.activemq_host = activemq_host
        self.activemq_port = activemq_port
        self.queue_name = '/queue/crimes.processing'
    
    def process_csv_upload(self, file: FileStorage) -> Dict[str, Any]:
        """
        Processa o upload do arquivo CSV:
        1. Lê o arquivo via stream
        2. Envia cada linha como mensagem para a fila ActiveMQ
        """
        if not file:
            return {
                "success": False,
                "mensagem": "Nenhum arquivo foi enviado"
            }
        
        if not file.filename.endswith('.csv'):
            return {
                "success": False,
                "mensagem": "O arquivo deve ser um CSV"
            }
        
        try:
            # Conecta ao ActiveMQ
            conn = stomp.Connection([(self.activemq_host, self.activemq_port)])
            conn.connect('admin', 'admin', wait=True)
            
            # Lê o arquivo via stream
            stream = StringIO(file.stream.read().decode("UTF-8"))
            csv_reader = csv.DictReader(stream)
            
            rows_processed = 0
            errors = []
            
            # Processa linha por linha
            for row_num, row in enumerate(csv_reader, start=2):  # Start=2 pois linha 1 é o header
                try:
                    # Cria objeto Crime a partir da linha
                    crime = Crime.from_csv_row(row)
                    
                    # Converte para JSON e envia para a fila
                    message = json.dumps(crime.to_dict())
                    conn.send(destination=self.queue_name, body=message)
                    
                    rows_processed += 1
                    
                except Exception as e:
                    errors.append(f"Erro na linha {row_num}: {str(e)}")
                    if len(errors) >= 10:  # Limita erros para não sobrecarregar a resposta
                        errors.append("... mais erros foram suprimidos")
                        break
            
            # Desconecta do ActiveMQ
            conn.disconnect()
            
            if errors:
                return {
                    "success": True,
                    "mensagem": "Processamento concluído com avisos",
                    "rows_processed": rows_processed,
                    "errors": errors
                }
            
            return {
                "success": True,
                "mensagem": "Arquivo processado com sucesso",
                "rows_processed": rows_processed
            }
            
        except Exception as e:
            return {
                "success": False,
                "mensagem": f"Erro ao processar arquivo: {str(e)}"
            }
