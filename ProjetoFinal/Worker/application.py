"""
Entry point para o Worker no Elastic Beanstalk
Cria uma aplicação Flask simples e roda o worker em background
"""
import sys
import os
import threading
from flask import Flask

# Adiciona o diretório atual ao path
sys.path.insert(0, os.path.dirname(__file__))

from main import main as worker_main

# Cria aplicação Flask mínima (para o health check do EB)
application = Flask(__name__)

@application.route('/')
def health_check():
    return {'status': 'Worker running', 'service': 'crimes-worker'}, 200

@application.route('/health')
def health():
    return {'status': 'healthy'}, 200

# Inicia o worker em uma thread separada
def start_worker():
    print("Starting Crime Worker in background thread...")
    worker_main()

worker_thread = threading.Thread(target=start_worker, daemon=True)
worker_thread.start()

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8000)
