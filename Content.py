import boto3
from dotenv import load_dotenv
from urllib.parse import urlparse
import os
import ContentDelivery

class Content:
    def __init__(self):
        pass

    # Parsear la URL para obtener el nombre del bucket y la clave del objeto
    def get_s3_bucket_key_from_url(self, s3_url):
        parsed_url = urlparse(s3_url)
        bucket_name = parsed_url.netloc.split('.')[0]  # Obtener el bucket de la URL
        object_key = parsed_url.path.lstrip('/')  # Obtener la clave del objeto
        return bucket_name, object_key

    # Obtener las propiedades del objeto
    def get_s3_object_properties(self, s3_url):
        # Inicializar el cliente de S3
        s3_client = boto3.client('s3')

        # Parsear la URL para obtener el bucket y la clave del objeto
        bucket_name, object_key = self.get_s3_bucket_key_from_url(s3_url)

        # Obtener el objeto
        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
        
        # Devolver las propiedades del objeto
        return response
    
# Example usage
if __name__ == '__main__':
    load_dotenv()  # Cargar variables de entorno desde .env

    s3_bucket_name = os.getenv('S3_BUCKET_NAME')
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    # Inicializar la clase ContentDelivery
    cdn = ContentDelivery.ContentDelivery(s3_bucket_name, aws_access_key_id, aws_secret_access_key)

    base_url = 'https://' + cdn.get_cloudfront_url()  # Proporcionar la URL de CloudFront si el bucket es público

    # Obtener las URLs de objetos en S3
    s3_urls = cdn.get_s3_object_urls(base_url=base_url)  # Pasar base_url si el bucket es público
    # OR
    # s3_urls = cdn.get_s3_object_urls()  # Para URLs pre-firmadas (bucket privado)

    if s3_urls:
        print("S3 URLs:")
        content = Content()  # Crear una instancia de la clase Content
        for url in s3_urls:
            print(url)
            properties = content.get_s3_object_properties(url)  # Llamar al método get_s3_object_properties a través de la instancia
            print("Properties:", properties)
