from flask import make_response
import json


def json_response(data, status_code=200):
    """
    Cria uma resposta JSON com UTF-8 encoding
    
    Args:
        data: Dados a serem serializados em JSON
        status_code: Código de status HTTP (padrão: 200)
    
    Returns:
        Response object do Flask
    """
    response = make_response(json.dumps(data, ensure_ascii=False, indent=2))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.status_code = status_code
    return response
