from flask import Flask, request, render_template
import boto3

KEY_ID = "ASIAVF37VDXB3QWEBSFA"
KEY_SECRET = "iPVmVQznT1zXh7IMB4eULiXoEUMim9FlBGgFcpEs"
TOKEN = "FwoGZXIvYXdzEJn//////////wEaDD3Ukzq5hVEnIK2jMyLUAeFLFjjRenH+7oKvWibeb/mdtRi9ZHTMsLTFsD3X5x50jXHXuxVUqwirCzsIY3kSGwEI1NoNldZ0f3XH2G7VAmshYf1Vlo9y29W+A6Am/K9hV7AgmrsGJ0UbjSG07a3TAMnN0JqVXnYY2vRs+VdvIaSEqJ2OxJ5DPXA4Cu2Ji98s+zkJ3taRausIw7ntAdTIElbsXHhAcbm6ZkJmW77zX3Wpc1Dq5e5dSysU+6uHGBWhTwoqSS5Qr0omknU/QwxtZ9rOlnUl33AFCTNyItC+eL5df9AzKIXp9YwGMi3j6doxyS4XPPVuNCqfVCAWBK/LZ/DwTPnHYct/71uhY8IEkMf+OPzqnsnGWYI="

textractcliente = boto3.client("textract", aws_access_key_id=KEY_ID, aws_secret_access_key=KEY_SECRET, region_name="us-east-1", aws_session_token=TOKEN)
s3client = boto3.client('s3', aws_access_key_id=KEY_ID, aws_secret_access_key=KEY_SECRET, region_name="us-east-1", aws_session_token=TOKEN)
pollyclient = boto3.client('polly', aws_access_key_id=KEY_ID, aws_secret_access_key=KEY_SECRET, region_name="us-east-1", aws_session_token=TOKEN)



app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def main():
    name = 'World' if (request.args.get('name') == None) else request.args.get('name')
    return f"Hello, {name}!"

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

app.run("0.0.0.0", port="5000", debug=True)
