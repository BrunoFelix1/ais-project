from datetime import datetime
from utils.response_helper import json_response


class HealthController:
    """Controller para gerenciar rotas de saúde e informações da API"""
    
    def home(self):
        """GET / - Rota principal"""
        return json_response({
            "mensagem": "Bem-vindo à API Backend!",
            "status": "online",
            "versao": "1.0.0"
        })
    
    def health_check(self):
        """GET /api/health - Verifica o status da API"""
        return json_response({
            "status": "healthy",
            "timestamp": datetime.now().isoformat()
        })
