import os


class Config:
    """Configurações da aplicação"""
    
    # Flask
    JSON_AS_ASCII = False
    JSONIFY_MIMETYPE = 'application/json; charset=utf-8'
    
    # Server
    HOST = '0.0.0.0'
    PORT = int(os.environ.get('PORT', 5000))
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
    
    # API
    API_VERSION = '1.0.0'
    API_TITLE = 'API Backend'


class DevelopmentConfig(Config):
    """Configurações de desenvolvimento"""
    DEBUG = True


class ProductionConfig(Config):
    """Configurações de produção"""
    DEBUG = False


# Mapeia o ambiente para a configuração correspondente
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(env_name: str = None) -> Config:
    """Retorna a configuração baseada no ambiente"""
    if env_name is None:
        env_name = os.environ.get('FLASK_ENV', 'default')
    return config_by_name.get(env_name, DevelopmentConfig)
