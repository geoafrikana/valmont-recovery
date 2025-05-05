import subprocess
import os
import datetime
import boto3
from dotenv import load_dotenv
from pathlib import Path
import logging

logging.basicConfig(
     filename="backup_ovh.log",
     encoding="utf-8",
     filemode="a",
     format="{asctime} - {levelname} - {message}",
     style="{",
     datefmt="%Y-%m-%d %H:%M",
 )

os.chdir(Path(__file__).parent.parent.resolve())
print("Current working directory:", os.getcwd())
load_dotenv()
ENV = os.environ.copy()

username = os.getenv("username")
access_key = os.getenv("access_key")
bucket_name = os.getenv("bucket")
secret_key = os.getenv("secret_key")
endpoint=os.getenv("endpoint")

db_name = os.getenv("db_name")
db_user = os.getenv("db_user")
ENV["PGPASSWORD"] = os.getenv("db_password")
db_host = os.getenv("db_host") or "localhost"

now = datetime.datetime.now()
stamp = now.strftime("%Y_%m_%d_%H_%M_%S")
logging.info(f"Backup started at {stamp}")
backup_file_name = f"db_backup_{stamp}.sql"

try:
  with open(backup_file_name, "w") as backup_file:
      subprocess.run(["docker", "exec", "postgis",
                  'pg_dump', "-h", "localhost",
                    "-U", db_user, "-d", db_name],
                      env=ENV, stdout=backup_file)
  subprocess.run(["zip", "-r", f"valmont_workspace_backup_{stamp}.zip", "valmont_workspace_backup/"])
except Exception as e:
    logging.exception(f"Error during backup postgis DB")


s3 = boto3.client('s3',
                  aws_access_key_id=access_key,
                   aws_secret_access_key=secret_key,
                   endpoint_url=endpoint)
try:
    
  response = s3.list_buckets()

  if bucket_name in [bucket['Name'] for bucket in response['Buckets']]:
      print(backup_file_name)
      s3.upload_file(backup_file_name, bucket_name, backup_file_name)

  s3.upload_file(f"valmont_workspace_backup_{stamp}.zip",
                  bucket_name, "valmont_workspace_backup_" +stamp + ".zip")
except Exception as e:
   logging.exception(f"Error during upload to OVH bucket: {bucket_name}")