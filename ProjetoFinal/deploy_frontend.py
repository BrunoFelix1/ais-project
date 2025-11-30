"""
Script para fazer deploy do Frontend no S3
"""

import boto3
import os
import mimetypes
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def upload_to_s3(bucket_name, dist_folder='Frontend/dist'):
    """Faz upload dos arquivos buildados para o S3"""
    
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )
    
    dist_path = Path(dist_folder)
    
    if not dist_path.exists():
        print(f"❌ Pasta '{dist_folder}' não encontrada!")
        print("Execute 'npm run build' primeiro!")
        return
    
    print(f"📦 Fazendo upload para s3://{bucket_name}/...")
    
    files_uploaded = 0
    
    # Percorre todos os arquivos na pasta dist
    for file_path in dist_path.rglob('*'):
        if file_path.is_file():
            # Caminho relativo para usar como key no S3
            relative_path = file_path.relative_to(dist_path)
            s3_key = str(relative_path).replace('\\', '/')
            
            # Detecta o content type
            content_type, _ = mimetypes.guess_type(str(file_path))
            if not content_type:
                content_type = 'application/octet-stream'
            
            # Upload do arquivo
            print(f"  Uploading {s3_key}...")
            s3.upload_file(
                str(file_path),
                bucket_name,
                s3_key,
                ExtraArgs={
                    'ContentType': content_type
                }
            )
            files_uploaded += 1
    
    print(f"\n✅ {files_uploaded} arquivos enviados com sucesso!")
    print(f"🌐 URL do site: http://{bucket_name}.s3-website-us-east-1.amazonaws.com")


def create_bucket(bucket_name):
    """Cria o bucket S3 e configura para hosting estático"""
    
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )
    
    try:
        # Cria o bucket
        print(f"Criando bucket '{bucket_name}'...")
        s3.create_bucket(Bucket=bucket_name)
        print(f"✅ Bucket '{bucket_name}' criado!")
        
    except s3.exceptions.BucketAlreadyOwnedByYou:
        print(f"✓ Bucket '{bucket_name}' já existe!")
    except Exception as e:
        print(f"❌ Erro ao criar bucket: {str(e)}")
    
    try:
        # Remove bloqueio de acesso público
        print("Removendo bloqueio de acesso público...")
        s3.delete_public_access_block(Bucket=bucket_name)
        print("✓ Bloqueio removido")
    except Exception as e:
        print(f"⚠️ Aviso ao remover bloqueio: {str(e)}")
    
    try:
        # Configura política pública
        print("Configurando política do bucket...")
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [{
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": ["s3:GetObject"],
                "Resource": [f"arn:aws:s3:::{bucket_name}/*"]
            }]
        }
        
        import json
        s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(bucket_policy))
        print("✓ Política configurada")
        
    except Exception as e:
        print(f"❌ Erro ao configurar política: {str(e)}")
    
    try:
        # Configura para website estático
        print("Configurando website hosting...")
        website_configuration = {
            'IndexDocument': {'Suffix': 'index.html'},
            'ErrorDocument': {'Key': 'index.html'}  # SPA routing
        }
        s3.put_bucket_website(Bucket=bucket_name, WebsiteConfiguration=website_configuration)
        print("✓ Website hosting configurado")
        
    except Exception as e:
        print(f"❌ Erro ao configurar website: {str(e)}")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python deploy_frontend.py <nome-do-bucket>")
        print("Exemplo: python deploy_frontend.py crimes-frontend-app")
        sys.exit(1)
    
    bucket_name = sys.argv[1]
    
    print("=== Deploy Frontend para S3 ===\n")
    create_bucket(bucket_name)
    print()
    upload_to_s3(bucket_name)
