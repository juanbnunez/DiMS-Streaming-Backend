import boto3
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_cloudfront_url():
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

# Example usage
if __name__ == "__main__":
    cloudfront_url = get_cloudfront_url()
    print(f"CloudFront URL: https://{cloudfront_url}")
