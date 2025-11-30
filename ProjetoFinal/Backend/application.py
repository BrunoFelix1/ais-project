import sys
from pathlib import Path

# Adiciona o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from main import create_app

# Elastic Beanstalk espera uma variável chamada 'application'
application = create_app()

if __name__ == '__main__':
    application.run()
