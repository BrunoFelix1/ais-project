from typing import List, Optional, Dict, Any
from models.item import Item
from repositories.item_repository import ItemRepository


class ItemService:
    """Serviço para gerenciar a lógica de negócio dos itens"""
    
    def __init__(self, repository: ItemRepository):
        self.repository = repository
    
    def get_all_items(self) -> Dict[str, Any]:
        """Retorna todos os itens"""
        items = self.repository.find_all()
        return {
            "success": True,
            "data": [item.to_dict() for item in items],
            "total": self.repository.count()
        }
    
    def get_item_by_id(self, item_id: int) -> Dict[str, Any]:
        """Retorna um item específico pelo ID"""
        item = self.repository.find_by_id(item_id)
        
        if item:
            return {
                "success": True,
                "data": item.to_dict()
            }
        else:
            return {
                "success": False,
                "mensagem": "Item não encontrado"
            }
    
    def create_item(self, data: dict) -> Dict[str, Any]:
        """Cria um novo item"""
        # Validação
        if not data or 'nome' not in data:
            return {
                "success": False,
                "mensagem": "Nome é obrigatório"
            }
        
        # Validação adicional do nome
        if not data['nome'].strip():
            return {
                "success": False,
                "mensagem": "Nome não pode estar vazio"
            }
        
        # Criação do item
        item = Item(
            nome=data['nome'],
            descricao=data.get('descricao', '')
        )
        
        created_item = self.repository.create(item)
        
        return {
            "success": True,
            "mensagem": "Item criado com sucesso",
            "data": created_item.to_dict()
        }
    
    def update_item(self, item_id: int, data: dict) -> Dict[str, Any]:
        """Atualiza um item existente"""
        existing_item = self.repository.find_by_id(item_id)
        
        if not existing_item:
            return {
                "success": False,
                "mensagem": "Item não encontrado"
            }
        
        # Atualiza apenas os campos fornecidos
        updated_item = Item(
            id=item_id,
            nome=data.get('nome', existing_item.nome),
            descricao=data.get('descricao', existing_item.descricao),
            criado_em=existing_item.criado_em
        )
        
        # Validação
        if not updated_item.nome.strip():
            return {
                "success": False,
                "mensagem": "Nome não pode estar vazio"
            }
        
        result = self.repository.update(item_id, updated_item)
        
        if result:
            return {
                "success": True,
                "mensagem": "Item atualizado com sucesso",
                "data": result.to_dict()
            }
        else:
            return {
                "success": False,
                "mensagem": "Erro ao atualizar item"
            }
    
    def delete_item(self, item_id: int) -> Dict[str, Any]:
        """Deleta um item"""
        item = self.repository.find_by_id(item_id)
        
        if not item:
            return {
                "success": False,
                "mensagem": "Item não encontrado"
            }
        
        deleted = self.repository.delete(item_id)
        
        if deleted:
            return {
                "success": True,
                "mensagem": "Item deletado com sucesso"
            }
        else:
            return {
                "success": False,
                "mensagem": "Erro ao deletar item"
            }
