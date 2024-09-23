# DiMS-Streaming-Backend
Backend for Distributed Multimedia System for Content Streaming v1.0

## Project Description
DiMS-Streaming-Backend is a cloud-based system that enables users to access and consume multimedia content, such as videos and music, from a web platform. The system is designed to handle multiple simultaneous requests efficiently, manage server-side resources, and deliver content across various network configurations. It ensures fast, reliable content delivery through AWS services, making it scalable and adaptable to different environments like local networks, intranets, and the internet. This project aims to offer a streaming experience similar to popular services like Netflix or Spotify.

## Installation Instructions
### Prerequisites:
- Python 3.x installed
- AWS account with credentials
- AWS CLI configured
- `boto3` and `Flask` Python packages installed
- `.env` file configured with AWS credentials and S3 bucket information
- `pip install -r requirements.txt` to install necessary dependencies

### Steps to Set Up:
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/juanbnunez/DiMS-Streaming-Backend.git
   cd DiMS-Streaming-Backend
   ```

2. **Set Up the Environment:**
   Ensure your AWS credentials and S3 bucket information are stored in a `.env` file:
   ```
   AWS_ACCESS_KEY_ID=your-access-key
   AWS_SECRET_ACCESS_KEY=your-secret-key
   S3_BUCKET_NAME=your-s3-bucket
   CLOUDFRONT_DISTRIBUTION_ID=your-distribution-id
   ```

3. **Install Dependencies:**
   Run the following command to install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the Backend:**
   You can start the Flask server by running:
   ```bash
   python Request.py
   ```

### Network Setup:
- **Local Development:**
  The system can be run locally on `localhost:5000` using Flask.
- **Cloud Deployment:**
  For cloud environments: Vercel, AWS Lambda instances can be configured. Ensure proper network permissions and IAM roles for accessing S3 and CloudFront.

## Usage Guide
### Example Commands:
- To access grouped media files from your S3 bucket via the API, send a `GET` request to the `/get-media` endpoint:
  ```bash
  curl http://localhost:5000/get-media
  ```
  This will return a JSON object with the names and URLs of media files.

### Recommended Configurations:
- **For Local Development:**
  Configure your `.env` file to point to a local S3 bucket and CloudFront distribution for testing purposes.
- **For Cloud Deployment:**
  Ensure that your S3 bucket and CloudFront distribution are set to allow proper public or private access based on your needs. Use AWS IAM policies to secure access to the resources.

## API Documentation
### Endpoints:
1. **`GET /get-media`:**  
   Fetches grouped media files (audio and image) from the S3 bucket, based on their base names.
   - **Response Format:**
     ```json
     [
       {
         "name": "file_base_name",
         "image_url": "http://example.com/image.jpg",
         "audio_url": "http://example.com/audio.mp3"
       }
     ]
     ```
   - **Error Handling:**  
     Returns a 500 error with details if an exception occurs during the request.

## Diagrams
Backend Architecture Diagram:
![Backend Architecture Diagram](https://drive.google.com/uc?export=view&id=1IQDQpbbOB_wACuJcOXRQNDSKeo4Oa48h)

Complete Platform Diagram:
![Complete Platform Diagram](https://drive.google.com/uc?export=view&id=114P-6PvblfqZbKtfffKcamwLzFW6R-nZ)

## Try the Platform
You can try the platform in production on Vercel by visiting the following link: [DiMS Streaming](https://di-ms-streaming-frontend.vercel.app/home.html)

## Contributions and Credits
### Authors:
This project was developed by:

[Jennifer González Solís](https://github.com/JennyGS23) and [Juan B. Núñez](https://github.com/juanbnunez)

Contributions: Together, we designed and implemented both the frontend and backend of the Distributed Multimedia System for Content Streaming. We focused on creating an intuitive user interface, integrating multimedia management, and ensuring seamless communication between components.

- **Third-party Technologies:**
  - **AWS S3**: Storage solution for multimedia content.
  - **AWS CloudFront**: Global CDN for fast content delivery.
  - **Boto3**: AWS SDK for Python.
  - **Flask**: Web framework for API development.
- Acknowledgments to open-source tools used in this project.

Feel free to contribute by submitting issues or pull requests! Any feedback is appreciated.
