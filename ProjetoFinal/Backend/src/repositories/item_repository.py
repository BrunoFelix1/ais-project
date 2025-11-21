from typing import List, Optional
from models.item import Item


class ItemRepository:
    """Repositório para gerenciar a persistência de itens"""
    
    def __init__(self):
        # Simulação de banco de dados em memória
        self._items: List[dict] = [
            {"id": 1, "nome": "Item 1", "descricao": "Descrição do item 1", "criado_em": "2025-11-21"},
            {"id": 2, "nome": "Item 2", "descricao": "Descrição do item 2", "criado_em": "2025-11-21"},
        ]
        self._next_id = 3
    
    def find_all(self) -> List[Item]:
        """Retorna todos os itens"""
        return [Item.from_dict(item) for item in self._items]
    
    def find_by_id(self, item_id: int) -> Optional[Item]:
        """Busca um item pelo ID"""
        item_dict = next((item for item in self._items if item["id"] == item_id), None)
        return Item.from_dict(item_dict) if item_dict else None
    
    def create(self, item: Item) -> Item:
        """Cria um novo item"""
        item.id = self._next_id
        self._next_id += 1
        self._items.append(item.to_dict())
        return item
    
    def update(self, item_id: int, item: Item) -> Optional[Item]:
        """Atualiza um item existente"""
        for i, existing_item in enumerate(self._items):
            if existing_item["id"] == item_id:
                item.id = item_id
                item.criado_em = existing_item["criado_em"]  # Mantém a data original
                self._items[i] = item.to_dict()
                return item
        return None
    
    def delete(self, item_id: int) -> bool:
        """Deleta um item pelo ID"""
        initial_length = len(self._items)
        self._items = [item for item in self._items if item["id"] != item_id]
        return len(self._items) < initial_length
    
    def count(self) -> int:
        """Retorna o total de itens"""
        return len(self._items)
