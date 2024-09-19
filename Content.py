import boto3
from dotenv import load_dotenv
import os

import ContentDelivery as delivery

# Initialize S3 client
s3 = boto3.client('s3')

def get_object_properties(bucket_name, object_key):
    try:
        # Retrieve the object's metadata using head_object
        response = s3.head_object(Bucket=bucket_name, Key=object_key)
        
        # Return object properties (e.g., Metadata, ContentLength, ContentType)
        return {
            'LastModified': response['LastModified'],
            'ContentLength': response['ContentLength'],
            'ContentType': response['ContentType'],
            'ETag': response['ETag'],
            'Metadata': response['Metadata'],
            'StorageClass': response.get('StorageClass', 'STANDARD'),  # Default to 'STANDARD' if not present
        }
    except Exception as e:
        print(f"Error retrieving object properties: {e}")
        return None




# Example usage
if __name__ == '__main__':
    # Example usage
    bucket_name = 'dims-streaming'
    

    s3_bucket_name = os.getenv('S3_BUCKET_NAME')
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    # Initialize the content delivery class
    cdn = delivery.ContentDelivery(s3_bucket_name, aws_access_key_id, aws_secret_access_key)

    base_url = cdn.get_cloudfront_url() # Provide if your bucket is public

    # Get S3 object URLs
    s3_urls = cdn.get_s3_object_urls(base_url=base_url)  # Pass base_url if the bucket is public
    # OR
    # s3_urls = cdn.get_s3_object_urls()  # For pre-signed URLs (private bucket)

    if s3_urls:
        print("S3 URLs:")
        for url in s3_urls:
            print(url)

            object_key = url

            properties = get_object_properties(bucket_name, object_key)
            print(properties)

