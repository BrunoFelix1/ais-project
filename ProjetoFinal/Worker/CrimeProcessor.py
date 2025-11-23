from decimal import Decimal
import json
import os
from typing import Any, Dict
import boto3
import stomp


class CrimeProcessor(stomp.ConnectionListener):
    """Listener que processa mensagens da fila de crimes"""
    
    def __init__(self):
        self.aggregations = {}
        
        # Configuração do DynamoDB
        self.dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        )
        self.table = self.dynamodb.Table('CrimeAggregations')
    
    def on_message(self, frame):
        """Callback chamado quando uma mensagem é recebida"""
        try:
            # Parse da mensagem JSON
            crime_data = json.loads(frame.body)
            
            bairro = crime_data.get('bairro')
            print(f"Processando crime: ID={crime_data.get('id')}, Bairro={bairro}")
            
            # Agrega os dados por bairro
            self.aggregate_crime(crime_data)
            
            # Salva no DynamoDB imediatamente
            if bairro:
                self.save_aggregation_to_dynamodb(bairro)
            
        except Exception as e:
            print(f"Erro ao processar mensagem: {str(e)}")
    
    def aggregate_crime(self, crime_data: Dict[str, Any]):
        """Agrega dados do crime por bairro"""
        bairro = crime_data.get('bairro')
        
        if not bairro:
            return
        
        # Inicializa agregação do bairro se não existir
        if bairro not in self.aggregations:
            self.aggregations[bairro] = {
                'total_crimes': 0,
                'latitude_sum': 0.0,
                'longitude_sum': 0.0,
                'prejuizo_total': 0.0,
                'count_with_coords': 0
            }
        
        agg = self.aggregations[bairro]
        agg['total_crimes'] += 1
        
        # Soma coordenadas se existirem
        if crime_data.get('latitude') and crime_data.get('longitude'):
            agg['latitude_sum'] += crime_data['latitude']
            agg['longitude_sum'] += crime_data['longitude']
            agg['count_with_coords'] += 1
        
        # Soma prejuízo se existir
        if crime_data.get('valor_prejuizo'):
            agg['prejuizo_total'] += crime_data['valor_prejuizo']
    
    def save_aggregation_to_dynamodb(self, bairro: str):
        """Salva/atualiza agregação de um bairro específico no DynamoDB"""
        if bairro not in self.aggregations:
            return
        
        try:
            data = self.aggregations[bairro]
            
            # Calcula médias
            count_coords = data['count_with_coords']
            lat_media = (data['latitude_sum'] / count_coords) if count_coords > 0 else 0
            lon_media = (data['longitude_sum'] / count_coords) if count_coords > 0 else 0
            
            # Salva no DynamoDB (converte float para Decimal)
            self.table.put_item(
                Item={
                    'bairro': bairro,
                    'total_crimes': data['total_crimes'],
                    'latitude_media': Decimal(str(lat_media)),
                    'longitude_media': Decimal(str(lon_media)),
                    'prejuizo_total': Decimal(str(data['prejuizo_total']))
                }
            )
            
            print(f"✓ Agregação de {bairro} atualizada no DynamoDB (Total: {data['total_crimes']} crimes)")
            
        except Exception as e:
            print(f"✗ Erro ao salvar agregação de {bairro}: {str(e)}")
    
    def print_statistics(self):
        """Exibe estatísticas do processamento"""
        total_crimes = sum(a['total_crimes'] for a in self.aggregations.values())
        print("\n=== Estatísticas ===")
        print(f"Total de bairros processados: {len(self.aggregations)}")
        print(f"Total de crimes agregados: {total_crimes}")
        print("===================")