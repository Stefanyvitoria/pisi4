from flask import Flask, request, render_template
import boto3

textractcliente = boto3.client("textract", aws_access_key_id="ASIAVF37VDXBSTJBDRUU", aws_secret_access_key="hLHSkapYMuRF9T7DykNqqwvZvKvGkpOMz2LbS7BT", region_name="us-east-1", aws_session_token="FwoGZXIvYXdzEP7//////////wEaDHORejansjfZAGoNXiLUAeGHVLKTwePERICCbWyHnVzjqMnA0RLBbmuOPfcHRFkqlaP1pY75Vi9yirOoM7C7l4/iuHkU3QyVlryy8evZItlV4bIve/liUsTjQ+6DN89VMutmvngAm/tyfXqZbARkEtXRxMCyBN4vNJ8LFNIQtGbYUab8lP/4qF9TLe8CIpxuwD9CBg8BlWc3/Nn/8tqrnGz60jyhJkFyJ+VUUTUJksvF90KZXhWkOyGg2uQzRV02VX4H9+mI1vkug0EgodPnnBTuN9y+Q++YbMiOkLIlEKMvUcEOKKrw04wGMi2duDXH80VPXUWEOosRtC+hWhAtRSOn20+JTY+4WwNMjgOixFeav4R9WA5HU0M=")


app = Flask(__name__)

@app.route("/", methods=["GET"])
def main():
    return "ok"

@app.route("/extract", methods=["POST"])
def extractImage():

    file = request.files.get("filename")
    binaryFile = file.read()
    response = textractcliente.detect_document_text(
        Document = {
            "Bytes": binaryFile
        }
    )

    text = ""
    for block in response["Blocks"]:
        if (block["BlockType"] == "LINE"):
            text+= block["Text"]+' '

    return text


app.run("0.0.0.0", port="5000", debug=True)