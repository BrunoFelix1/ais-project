from flask import request
from services.crime_service import CrimeService
from repositories.crime_repository import CrimeRepository
from utils.response_helper import json_response


class CrimeController:
    """Controller para gerenciar rotas relacionadas a crimes"""
    
    def __init__(self, crime_service: CrimeService, crime_repository: CrimeRepository):
        self.crime_service = crime_service
        self.crime_repository = crime_repository
    
    def upload_csv(self):
        """POST /api/crimes/upload - Faz upload do CSV e envia para processamento"""
        if 'file' not in request.files:
            return json_response({
                "success": False,
                "mensagem": "Nenhum arquivo foi enviado"
            }, 400)
        
        file = request.files['file']
        
        if file.filename == '':
            return json_response({
                "success": False,
                "mensagem": "Nenhum arquivo selecionado"
            }, 400)
        
        result = self.crime_service.process_csv_upload(file)
        status_code = 200 if result["success"] else 400
        return json_response(result, status_code)
    
    def get_aggregations(self):
        """GET /api/crimes/aggregations - Retorna dados agregados de todos os bairros"""
        aggregations = self.crime_repository.get_all_aggregations()
        
        return json_response({
            "success": True,
            "data": [agg.to_dict() for agg in aggregations],
            "total_bairros": len(aggregations)
        })
    
    def get_aggregation_by_bairro(self, bairro: str):
        """GET /api/crimes/aggregations/<bairro> - Retorna agregação de um bairro específico"""
        aggregation = self.crime_repository.get_by_bairro(bairro)
        
        if aggregation:
            return json_response({
                "success": True,
                "data": aggregation.to_dict()
            })
        else:
            return json_response({
                "success": False,
                "mensagem": f"Bairro '{bairro}' não encontrado"
            }, 404)
    
    def get_stats(self):
        """GET /api/crimes/stats - Retorna estatísticas gerais"""
        aggregations = self.crime_repository.get_all_aggregations()
        
        total_crimes = sum(agg.total_crimes for agg in aggregations)
        total_prejuizo = sum(agg.prejuizo_total for agg in aggregations)
        total_bairros = len(aggregations)
        
        # Bairro com mais crimes
        bairro_mais_crimes = None
        if aggregations:
            bairro_mais_crimes_obj = max(aggregations, key=lambda x: x.total_crimes)
            bairro_mais_crimes = {
                "bairro": bairro_mais_crimes_obj.bairro,
                "total_crimes": bairro_mais_crimes_obj.total_crimes
            }
        
        return json_response({
            "success": True,
            "data": {
                "total_crimes": total_crimes,
                "total_prejuizo": total_prejuizo,
                "total_bairros": total_bairros,
                "bairro_mais_crimes": bairro_mais_crimes
            }
        })
    
    def clear_data(self):
        """DELETE /api/crimes/clear - Limpa todos os dados agregados"""
        self.crime_repository.clear_all()
        return json_response({
            "success": True,
            "mensagem": "Dados limpos com sucesso"
        })
