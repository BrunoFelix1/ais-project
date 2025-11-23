from flask import Flask
from flask_cors import CORS
from config.config import get_config
from repositories.crime_repository import CrimeRepository
from services.crime_service import CrimeService
from controllers.crime_controller import CrimeController
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
    crime_repository = CrimeRepository()
    crime_service = CrimeService()
    crime_controller = CrimeController(crime_service, crime_repository)
    health_controller = HealthController()
    
    # Registro de rotas
    register_routes(app, crime_controller, health_controller)
    
    return app


def register_routes(app, crime_controller, health_controller):
    """Registra todas as rotas da aplicação"""
    
    # Rotas de saúde
    app.add_url_rule('/', 'home', health_controller.home, methods=['GET'])
    app.add_url_rule('/api/health', 'health_check', health_controller.health_check, methods=['GET'])
    
    # Rotas de crimes
    app.add_url_rule('/api/crimes/upload', 'upload_csv', crime_controller.upload_csv, methods=['POST'])
    app.add_url_rule('/api/crimes/aggregations', 'get_aggregations', crime_controller.get_aggregations, methods=['GET'])
    app.add_url_rule('/api/crimes/aggregations/<string:bairro>', 'get_aggregation_by_bairro', crime_controller.get_aggregation_by_bairro, methods=['GET'])
    app.add_url_rule('/api/crimes/stats', 'get_stats', crime_controller.get_stats, methods=['GET'])
    app.add_url_rule('/api/crimes/clear', 'clear_data', crime_controller.clear_data, methods=['DELETE'])


if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'])
