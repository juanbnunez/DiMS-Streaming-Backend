import boto3
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class ContentDelivery:
    def __init__(self, s3_bucket_name, aws_access_key_id=None, aws_secret_access_key=None, region_name='us-east-2'):
        self.s3_bucket_name = s3_bucket_name

        # Initialize S3 client with optional credentials
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    def get_cloudfront_url(self):
        # Get distribution ID from environment variable
        distribution_id = os.getenv('CLOUDFRONT_DISTRIBUTION_ID')
        
        # Print the loaded distribution ID for debugging
        print(f"Loaded CloudFront Distribution ID: {distribution_id}")
        
        if not distribution_id:
            raise ValueError("CLOUDFRONT_DISTRIBUTION_ID is not set or loaded from the .env file.")

        # Initialize the CloudFront client
        client = boto3.client('cloudfront')

        # Get distribution information
        response = client.get_distribution(Id=distribution_id)

        # Extract the domain name (URL) from the response
        domain_name = response['Distribution']['DomainName']

        return domain_name

    def list_s3_objects(self):
        """List all objects in the S3 bucket and return their keys."""
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.s3_bucket_name)
            if 'Contents' in response:
                return [obj['Key'] for obj in response['Contents']]
            else:
                print("No objects found in the bucket.")
                return []
        except Exception as e:
            print(f"Error listing objects in S3 bucket: {e}")
            return []

    def get_s3_object_urls(self, base_url=None):
        """Generate URLs for all objects in the S3 bucket.
        
        If base_url is provided, it assumes the bucket is publicly accessible and constructs
        the URLs accordingly. Otherwise, it generates pre-signed URLs.
        """
        object_keys = self.list_s3_objects()
        
        if base_url:
            # Construct public URLs assuming the bucket is publicly accessible
            return [f'{base_url}/{key}' for key in object_keys]
        else:
            # Generate pre-signed URLs for private S3 objects
            urls = []
            for key in object_keys:
                url = self.s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': self.s3_bucket_name, 'Key': key},
                    ExpiresIn=3600  # URL expires in 1 hour
                )
                urls.append(url)
            return urls

if __name__ == '__main__':
    load_dotenv()  # Cargar variables de entorno desde .env

    s3_bucket_name = os.getenv('S3_BUCKET_NAME')
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    # Inicializar la clase ContentDelivery
    cdn = ContentDelivery(s3_bucket_name, aws_access_key_id, aws_secret_access_key)

    base_url = 'https://' + cdn.get_cloudfront_url()  # Proporcionar la URL de CloudFront si el bucket es público

    # Obtener las URLs de objetos en S3
    s3_urls = cdn.get_s3_object_urls(base_url=base_url)  # Pasar base_url si el bucket es público
    # OR
    # s3_urls = cdn.get_s3_object_urls()  # Para URLs pre-firmadas (bucket privado)

    if s3_urls:
        print("S3 URLs:")
        # content = Content()  # Crear una instancia de la clase Content
        for url in s3_urls:
            print(url)
            # properties = content.get_s3_object_properties(url)  # Llamar al método get_s3_object_properties a través de la instancia
            # print("Properties:", properties)

