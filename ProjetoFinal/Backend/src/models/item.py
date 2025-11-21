from datetime import datetime
from typing import Optional


class Item:
    """Modelo de Item"""
    
    def __init__(self, id: Optional[int] = None, nome: str = "", 
                 descricao: str = "", criado_em: Optional[str] = None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.criado_em = criado_em or datetime.now().strftime('%Y-%m-%d')
    
    def to_dict(self) -> dict:
        """Converte o objeto para dicionário"""
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "criado_em": self.criado_em
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Item':
        """Cria um objeto Item a partir de um dicionário"""
        return Item(
            id=data.get('id'),
            nome=data.get('nome', ''),
            descricao=data.get('descricao', ''),
            criado_em=data.get('criado_em')
        )
    
    def __repr__(self):
        return f"<Item(id={self.id}, nome='{self.nome}')>"
