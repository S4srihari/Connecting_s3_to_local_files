import os
import boto3
from PIL import Image
from botocore.exceptions import NoCredentialsError

# --- CONFIGURATION ---
source_dir = r'src folder path'
dest_dir = r'dest folder path'
bucket_name = 's3 bucket name'
s3_folder = 'folder name in bucket' 

# Initialize S3 Client
s3_client = boto3.client(
    's3',
    aws_access_key_id='access key',
    aws_secret_access_key='secret access key'
)

# Create local destination folder if it doesn't exist
if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

for file in os.listdir(source_dir):
    if file.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff")):
        
        # 1. LOCAL CONVERSION
        input_path = os.path.join(source_dir, file)
        file_name_only = os.path.splitext(file)[0]
        webp_name = file_name_only + ".webp"
        local_output_path = os.path.join(dest_dir, webp_name)
        
        try:
            img = Image.open(input_path)
            img.save(local_output_path, "webp")
            print(f"Converted locally: {webp_name}")

            # 2. AWS S3 UPLOAD
            s3_path = s3_folder + webp_name
            s3_client.upload_file(local_output_path, bucket_name, s3_path)
            print(f"Uploaded to S3: s3://{bucket_name}/{s3_path}")

        except FileNotFoundError:
            print("The file was not found")
        except NoCredentialsError:
            print("Credentials not available")
        except Exception as e:
            print(f"Error: {e}")

print("Done!")