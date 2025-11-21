from flask import request
from services.item_service import ItemService
from utils.response_helper import json_response


class ItemController:
    """Controller para gerenciar as rotas de itens"""
    
    def __init__(self, service: ItemService):
        self.service = service
    
    def get_all(self):
        """GET /api/items - Retorna todos os itens"""
        result = self.service.get_all_items()
        return json_response(result)
    
    def get_by_id(self, item_id: int):
        """GET /api/items/<id> - Retorna um item específico"""
        result = self.service.get_item_by_id(item_id)
        status_code = 200 if result["success"] else 404
        return json_response(result, status_code)
    
    def create(self):
        """POST /api/items - Cria um novo item"""
        data = request.get_json()
        result = self.service.create_item(data)
        status_code = 201 if result["success"] else 400
        return json_response(result, status_code)
    
    def update(self, item_id: int):
        """PUT /api/items/<id> - Atualiza um item existente"""
        data = request.get_json()
        result = self.service.update_item(item_id, data)
        status_code = 200 if result["success"] else 404
        return json_response(result, status_code)
    
    def delete(self, item_id: int):
        """DELETE /api/items/<id> - Deleta um item"""
        result = self.service.delete_item(item_id)
        status_code = 200 if result["success"] else 404
        return json_response(result, status_code)
