import os
import boto3
from botocore.client import Config
import requests
import logging


class ObjectStorageClient:
  endpoint_url = None
  bucket_name = os.getenv("BUCKET_NAME")

  def __init__(self):
    # set options for signatures
    self.client_v2 = self.build_client("s3")
    self.client_v4 = self.build_client("s3v4")

  def build_client(self, signature_version: str = "s3v4"):
    scw_access_key = os.getenv("SCW_ACCESS_KEY")
    scw_secret_key = os.getenv("SCW_SECRET_KEY")
    if not scw_access_key or not scw_secret_key:
      raise ValueError("SCW_ACCESS_KEY and SCW_SECRET_KEY environment variables must be set. Refer to README.md")
    return boto3.session.Session().client(
      service_name="s3",
      config=Config(signature_version=signature_version),
      region_name=os.getenv("REGION_NAME"),
      use_ssl=True,
      endpoint_url=ObjectStorageClient.endpoint_url,
            aws_access_key_id=scw_access_key,
            aws_secret_access_key=scw_secret_key,
        )
    
  def list_buckets(self):
    try:
      response = self.client_v4.list_buckets()
      return response['Buckets']
    except Exception as e:
      logging.error(f"Error listing buckets: {e}")
      raise
  
  def list_objects(self):
    try:
      response = self.client_v4.list_objects(Bucket=self.bucket_name)
      return response.get("Contents", [])
    except Exception as e:
      logging.error(f"Looking for bucket named '{self.bucket_name}'. Error listing objects: {e}")
      raise
  
  def download_object_local(self, file_key, local_path):
    try:
      self.client_v4.download_file(self.bucket_name, file_key, local_path)
    except Exception as e:
      logging.error(f"Error downloading object: {e}")
      raise
  
  def upload_object_local(self, local_path, file_key=None, public_read=False):
    if file_key is None:
      file_key = os.path.basename(local_path)
    try:
      self.client_v2.upload_file(
        local_path,
        self.bucket_name,
        file_key,
        ExtraArgs={"ACL": "public-read"} if public_read else None,
        )
    except Exception as e:
      logging.error(f"Error uploading object: {e}")
      raise

  def upload_object_url(self, url, file_key):
    try:
      response = requests.get(url)
      if response.status_code == 200:
        self.client_v4.put_object(Bucket=self.bucket_name, Key=file_key, Body=response.content)
    except requests.RequestException as e:
      logging.error(f"Error fetching URL: {e}")
      raise
    except Exception as e:
      logging.error(f"Error uploading object from URL '{url}' into bucket '{self.bucket_name}': {e}")
      raise
      
  def delete_object(self, key):
    try:
      self.client_v4.delete_object(Bucket=self.bucket_name, Key=key)
    except Exception as e:
      logging.error(f"Error deleting object: {e}")
      raise
