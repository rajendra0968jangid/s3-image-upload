from flask import Flask, render_template, request
import boto3
import os
from dotenv import load_dotenv
from uuid import uuid4

load_dotenv()

app = Flask(__name__)

# S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

BUCKET = os.getenv("AWS_BUCKET_NAME")
REGION = os.getenv("AWS_REGION")

@app.route("/", methods=["GET", "POST"])
def upload_image():
    image_url = None

    if request.method == "POST":
        file = request.files["image"]

        if file:
            filename = f"uploads/{uuid4()}-{file.filename}"

            s3.upload_fileobj(
                file,
                BUCKET,
                filename,
                ExtraArgs={"ContentType": file.content_type}
            )

            image_url = f"https://{BUCKET}.s3.{REGION}.amazonaws.com/{filename}"

    return render_template("index.html", image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)
