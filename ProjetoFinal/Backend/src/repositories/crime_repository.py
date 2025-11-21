from typing import List, Optional
import boto3
import os
from models.crime import CrimeAggregation
from decimal import Decimal


class CrimeRepository:
    """Repository para acessar dados agregados de crimes do DynamoDB"""
    
    def __init__(self):
        # Configuração do DynamoDB
        self.dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        )
        self.table = self.dynamodb.Table('CrimeAggregations')
    
    def _convert_decimals(self, obj):
        """Converte Decimal para float recursivamente"""
        if isinstance(obj, list):
            return [self._convert_decimals(i) for i in obj]
        elif isinstance(obj, dict):
            return {k: self._convert_decimals(v) for k, v in obj.items()}
        elif isinstance(obj, Decimal):
            return float(obj)
        else:
            return obj
    
    def get_all_aggregations(self) -> List[CrimeAggregation]:
        """Retorna todas as agregações do DynamoDB"""
        try:
            response = self.table.scan()
            items = response.get('Items', [])
            
            result = []
            for item in items:
                item = self._convert_decimals(item)
                result.append(CrimeAggregation(
                    bairro=item.get('bairro', ''),
                    total_crimes=item.get('total_crimes', 0),
                    latitude_media=item.get('latitude_media', 0.0),
                    longitude_media=item.get('longitude_media', 0.0),
                    prejuizo_total=item.get('prejuizo_total', 0.0)
                ))
            
            return result
        except Exception as e:
            print(f"Erro ao buscar agregações: {str(e)}")
            return []
    
    def get_by_bairro(self, bairro: str) -> Optional[CrimeAggregation]:
        """Retorna agregação de um bairro específico do DynamoDB"""
        try:
            response = self.table.get_item(Key={'bairro': bairro})
            
            if 'Item' not in response:
                return None
            
            item = self._convert_decimals(response['Item'])
            
            return CrimeAggregation(
                bairro=item.get('bairro', ''),
                total_crimes=item.get('total_crimes', 0),
                latitude_media=item.get('latitude_media', 0.0),
                longitude_media=item.get('longitude_media', 0.0),
                prejuizo_total=item.get('prejuizo_total', 0.0)
            )
        except Exception as e:
            print(f"Erro ao buscar bairro {bairro}: {str(e)}")
            return None
    
    def clear_all(self):
        """Limpa todos os dados do DynamoDB"""
        try:
            response = self.table.scan()
            items = response.get('Items', [])
            
            with self.table.batch_writer() as batch:
                for item in items:
                    batch.delete_item(Key={'bairro': item['bairro']})
            
            print("Todos os dados foram limpos do DynamoDB")
        except Exception as e:
            print(f"Erro ao limpar dados: {str(e)}")
    
    def count(self) -> int:
        """Retorna o número de bairros com dados agregados"""
        try:
            response = self.table.scan(Select='COUNT')
            return response.get('Count', 0)
        except Exception as e:
            print(f"Erro ao contar registros: {str(e)}")
            return 0
