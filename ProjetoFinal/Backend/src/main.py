from flask import Flask
from flask_cors import CORS
from config import get_config
from repositories.item_repository import ItemRepository
from services.item_service import ItemService
from controllers.item_controller import ItemController
from controllers.health_controller import HealthController


def create_app(config_name=None):
    """Factory function para criar a aplicação Flask"""
    app = Flask(__name__)
    
    # Configuração
    config = get_config(config_name)
    app.config.from_object(config)
    
    # CORS
    CORS(app)
    
    # Dependências (Injeção de Dependência)
    item_repository = ItemRepository()
    item_service = ItemService(item_repository)
    item_controller = ItemController(item_service)
    health_controller = HealthController()
    
    # Registro de rotas
    register_routes(app, item_controller, health_controller)
    
    return app


def register_routes(app, item_controller, health_controller):
    """Registra todas as rotas da aplicação"""
    
    # Rotas de saúde
    app.add_url_rule('/', 'home', health_controller.home, methods=['GET'])
    app.add_url_rule('/api/health', 'health_check', health_controller.health_check, methods=['GET'])
    
    # Rotas de itens
    app.add_url_rule('/api/items', 'get_items', item_controller.get_all, methods=['GET'])
    app.add_url_rule('/api/items/<int:item_id>', 'get_item', item_controller.get_by_id, methods=['GET'])
    app.add_url_rule('/api/items', 'create_item', item_controller.create, methods=['POST'])
    app.add_url_rule('/api/items/<int:item_id>', 'update_item', item_controller.update, methods=['PUT'])
    app.add_url_rule('/api/items/<int:item_id>', 'delete_item', item_controller.delete, methods=['DELETE'])


if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'])
