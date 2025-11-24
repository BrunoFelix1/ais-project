from decimal import Decimal, ROUND_HALF_UP
import json
import os
from typing import Any, Dict
import boto3
import stomp


class CrimeProcessor(stomp.ConnectionListener):
    """Listener que processa mensagens da fila de crimes"""

    def __init__(self):
        self.processed_messages = 0

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
            crime_data = json.loads(frame.body)

            bairro = crime_data.get('bairro')
            print(f"Processando crime: ID={crime_data.get('id')}, Bairro={bairro}")

            if not bairro:
                print("Mensagem ignorada: bairro não informado")
                return

            self.upsert_crime_aggregation(bairro, crime_data)
            self.processed_messages += 1

        except Exception as e:
            print(f"Erro ao processar mensagem: {str(e)}")

    def upsert_crime_aggregation(self, bairro: str, crime_data: Dict[str, Any]):
        """Atualiza o agregado do bairro diretamente no DynamoDB"""
        try:
            existing = self.table.get_item(Key={'bairro': bairro}).get('Item', {})

            total_crimes = int(existing.get('total_crimes', 0)) + 1
            prejuizo_total = self._decimal(existing.get('prejuizo_total', 0))
            prejuizo_total += self._decimal(crime_data.get('valor_prejuizo') or 0)

            latitude_media = self._decimal(existing.get('latitude_media', 0))
            longitude_media = self._decimal(existing.get('longitude_media', 0))
            count_with_coords = int(existing.get('count_with_coords', 0))

            has_coordinates = (
                crime_data.get('latitude') not in (None, '')
                and crime_data.get('longitude') not in (None, '')
            )

            if has_coordinates:
                count_with_coords += 1
                latitude_media = self._incremental_average(
                    latitude_media, self._decimal(crime_data.get('latitude') or 0), count_with_coords
                )
                longitude_media = self._incremental_average(
                    longitude_media, self._decimal(crime_data.get('longitude') or 0), count_with_coords
                )

            item = {
                'bairro': bairro,
                'total_crimes': total_crimes,
                'prejuizo_total': prejuizo_total,
                'latitude_media': latitude_media,
                'longitude_media': longitude_media,
                'count_with_coords': count_with_coords,
            }

            self.table.put_item(Item=item)

            print(
                f"✓ Dados de {bairro} atualizados (Total: {total_crimes} | Prejuízo: {prejuizo_total})"
            )

        except Exception as e:
            print(f"✗ Erro ao atualizar {bairro}: {str(e)}")

    @staticmethod
    def _decimal(value) -> Decimal:
        if value is None:
            return Decimal('0')
        if isinstance(value, Decimal):
            return value
        return Decimal(str(value))

    @staticmethod
    def _incremental_average(previous_avg: Decimal, new_value: Decimal, total_count: int) -> Decimal:
        if total_count <= 0:
            return Decimal('0')
        # Fórmula incremental: new_avg = (prev_avg * (n-1) + x_n) / n
        numerator = previous_avg * Decimal(total_count - 1) + new_value
        return (numerator / Decimal(total_count)).quantize(Decimal('0.0000001'), rounding=ROUND_HALF_UP)

    def print_statistics(self):
        """Exibe estatísticas simples do processamento"""
        print("\n=== Estatísticas ===")
        print(f"Mensagens processadas nesta execução: {self.processed_messages}")
        print("===================")