import io
from os import system
from flask import Flask, request, render_template, send_file
import boto3

KEY_ID = "ASIAVF37VDXB7OSXSKB6"
KEY_SECRET = "yST6qEvKExQ06mi1ANXY8zu83j2jtPHcwdbeCKGd"
TOKEN = "FwoGZXIvYXdzELH//////////wEaDKSyWF9tGKyJkOd1qSLUAY0A8eJAgzjnLSWNqhQ7xA0g+LGsPgaObE0tSIlRXUkfPq5T747esykj7QI61ipAghC2R8vgDp+N2qPzX7AOiyRuT9mNOp8O6Pua7ZsyXLRHSISLNJsXmHwN1XoznSal0NVou/doG1N58TDfoksdCBHDpGdPz5WGt8LviaXjvhTWqZ+zRAwlQBqqqFdjaB4jc4p6A3+nQQrCQ49eoXhswIsiNJ3Glr3ycD6A5PM3ozs4Z2IK3XZtQ9nFRngFLfS+kYFQfbcFCxhkLaC+wdwKC1cp+03KKIKP+4wGMi2gof1mfcPXHaWEFCIGsPvz4IxjfSTUiduWSzeFeYX9mfnHNo9H4xzl7iDwcr8="
textractcliente = boto3.client("textract", aws_access_key_id=KEY_ID, aws_secret_access_key=KEY_SECRET, region_name="us-east-1", aws_session_token=TOKEN)
s3client = boto3.client('s3', aws_access_key_id=KEY_ID, aws_secret_access_key=KEY_SECRET, region_name="us-east-1", aws_session_token=TOKEN)
pollyclient = boto3.client('polly', aws_access_key_id=KEY_ID, aws_secret_access_key=KEY_SECRET, region_name="us-east-1", aws_session_token=TOKEN)



app = Flask(__name__)


@app.route('/logo', methods=["GET"])
def logo():
    return send_file('../assets/img/b_UFRPE.png', mimetype='image/png')

@app.route('/css', methods=["GET", "POST"])
def css():
    return send_file('../assets/css/style.css', mimetype='text/css')

@app.route('/js', methods=["GET", "POST"])
def js():
    return send_file('../assets/js/script.js', mimetype='text/js')


@app.route("/", methods=["GET", "POST", "PUT"])
def main():
    return render_template('index.html')

@app.route("/extract", methods=["POST"])
def extractImage():

    file = request.files.get("file")
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
    file = open('text.txt', mode='w')
    file.write(text)
    file.close()

    return text

@app.route("/upfile", methods=["POST"])
def upFile():
    response = s3client.upload_file('./text.txt', 'stefany-txt-bucket', 'hello.txt')

    return response

@app.route("/createbucket", methods=["POST"])
def createBucket():
    response = s3client.create_bucket(Bucket='stefany-txt-bucket-teste')

    return response

@app.route("/polly", methods=["POST"])
def polly():
    response = pollyclient.synthesize_speech(
    OutputFormat='mp3',
    Text='hello, how are you?',
    VoiceId='Amy'
    )

    file = open("voice.mp3", 'wb')
    file.write(response['AudioStream'].read())
    file.close()
    return response['ResponseMetadata']['RequestId']


@app.route('/teste', methods=["GET", "POST"])
def teste():
    file = request.get_json()
    print(file)
    return 'stefany'



app.run("127.0.0.1", port="5000", debug=True)
