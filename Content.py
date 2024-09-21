import boto3
from dotenv import load_dotenv
import os
import ContentDelivery as delivery

class Content:
    def __init__(self):
        # Cargar variables de entorno
        load_dotenv()
        self.s3 = boto3.client('s3')
        self.s3_bucket_name = os.getenv('S3_BUCKET_NAME')
        self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.distribution_id = os.getenv('CLOUDFRONT_DISTRIBUTION_ID')
        self.cdn = delivery.ContentDelivery(self.s3_bucket_name, self.aws_access_key_id, self.aws_secret_access_key, self.distribution_id)

    def get_object_properties(self, object_key):
        try:
            # Obtener metadatos del objeto
            response = self.s3.head_object(Bucket=self.s3_bucket_name, Key=object_key)
            
            # Devolver las propiedades del objeto
            return {
                'LastModified': response['LastModified'],
                'ContentLength': response['ContentLength'],
                'ContentType': response['ContentType'],
                'ETag': response['ETag'],
                'Metadata': response['Metadata'],
                'StorageClass': response.get('StorageClass', 'STANDARD'),  # Por defecto 'STANDARD' si no está presente
            }
        except Exception as e:
            print(f"Error obteniendo propiedades del objeto: {e}")
            return None

    def group_s3_objects_by_name(self):
        # Obtener URLs y nombres de objetos de S3
        s3_urls = self.cdn.get_s3_object_urls()
        s3_names = self.cdn.get_s3_object_names()

        # Diccionario para agrupar archivos por nombre base
        grouped_files = {}

        for url, name in zip(s3_urls, s3_names):
            # Separar el nombre base y la extensión
            name_base, extension = os.path.splitext(name)
            
            # Inicializar una entrada en el diccionario si no existe
            if name_base not in grouped_files:
                grouped_files[name_base] = {"image": None, "audio": None}

            # Asignar la URL al tipo correspondiente (imagen o audio)
            if extension == '.jpg':
                grouped_files[name_base]["image"] = url
            elif extension == '.mp3':
                grouped_files[name_base]["audio"] = url

        return grouped_files

    def display_grouped_s3_objects(self):
        grouped_files = self.group_s3_objects_by_name()

        print("\nArchivos agrupados por nombre:")
        for name_base, files in grouped_files.items():
            print(f"\nNombre: {name_base}")
            print(f"Imagen: {files['image']}")
            print(f"Audio: {files['audio']}")


# Ejemplo de uso
if __name__ == '__main__':
    s3_manager = Content()
    s3_manager.display_grouped_s3_objects()
