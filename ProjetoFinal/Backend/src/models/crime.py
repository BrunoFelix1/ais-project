from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Crime:
    """Modelo de dados para representar um crime do dataset"""
    id: Optional[int] = None
    bairro: Optional[str] = None
    created_at: Optional[str] = None
    descricao: Optional[str] = None
    endereco: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    registrou_bo: Optional[bool] = None
    sexo: Optional[int] = None
    tipo_assalto_id: Optional[int] = None
    titulo: Optional[str] = None
    valor_prejuizo: Optional[float] = None
    time: Optional[str] = None
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            "id": self.id,
            "bairro": self.bairro,
            "created_at": self.created_at,
            "descricao": self.descricao,
            "endereco": self.endereco,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "registrou_bo": self.registrou_bo,
            "sexo": self.sexo,
            "tipo_assalto_id": self.tipo_assalto_id,
            "titulo": self.titulo,
            "valor_prejuizo": self.valor_prejuizo,
            "time": self.time
        }
    
    @staticmethod
    def from_csv_row(row: dict):
        """Cria um Crime a partir de uma linha do CSV"""
        return Crime(
            id=int(row['id']) if row.get('id') and row['id'].strip() else None,
            bairro=row.get('bairro', '').strip() or None,
            created_at=row.get('created_at', '').strip() or None,
            descricao=row.get('descricao', '').strip() or None,
            endereco=row.get('endereco', '').strip() or None,
            latitude=float(row['latitude']) if row.get('latitude') and row['latitude'].strip() else None,
            longitude=float(row['longitude']) if row.get('longitude') and row['longitude'].strip() else None,
            registrou_bo=row.get('registrou_bo', '').strip().lower() == 'true',
            sexo=int(row['sexo']) if row.get('sexo') and row['sexo'].strip() else None,
            tipo_assalto_id=int(row['tipo_assalto_id']) if row.get('tipo_assalto_id') and row['tipo_assalto_id'].strip() else None,
            titulo=row.get('titulo', '').strip() or None,
            valor_prejuizo=float(row['valor_prejuizo']) if row.get('valor_prejuizo') and row['valor_prejuizo'].strip() else None,
            time=row.get('time', '').strip() or None
        )


@dataclass
class CrimeAggregation:
    """Modelo para dados agregados de crimes por bairro"""
    bairro: str
    total_crimes: int
    latitude_media: float
    longitude_media: float
    prejuizo_total: float
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            "bairro": self.bairro,
            "total_crimes": self.total_crimes,
            "latitude_media": self.latitude_media,
            "longitude_media": self.longitude_media,
            "prejuizo_total": self.prejuizo_total
        }
