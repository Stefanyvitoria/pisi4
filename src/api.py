import io
from os import system
from flask import Flask, request, render_template, send_file
import boto3

KEY_ID = "ASIAVF37VDXB6VDQZF6K"
KEY_SECRET = "cfC+zwbAPDIkcaXKHtu6PgM7t9bPE2vlwcvcVNv5"
TOKEN = "FwoGZXIvYXdzELT//////////wEaDHDDakd+Npo7Il6PayLUAcZpo2hVbcx2FlMYVeM7dCiZAl/Cky63voEIivHmmp1GAICEyP6TeihnSsRROKCoy6M/4l2YL3lYnbc8joOslo7emgKDHzjfGpg443nMB9pg6wOFKnIcKXRR55XqybX6paNA+Uju0BkJ1inRNshqbn3BTlgCTkNfcXa1c7qryKLsxpKhyoDC7yrp9yACKff1bhvBBsk1HwBCk/wTSHcLBj4ZptDzYq3X0YASdPN9CNmexU40I/k8/OhdaHoBBprPPwzkIZw5vagkx6AXyFPMhURxsVQwKLz4+4wGMi3FX7EzfnKARVYhJXeqlW+laTy0C1M5Jb7bhN6Cf+kCYx3C24KMFm5LZ0lIKY8="

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


@app.route('/aws', methods=["GET", "POST"])
def aws():
    file = request.files.get("file")

    #Extração do texto
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

    #Armazenando o texto
    response = s3client.upload_file('./text.txt', 'stefany-txt-bucket', 'texto-extraido.txt')

    #Criando Audio
    response = pollyclient.synthesize_speech(
    OutputFormat='mp3',
    Text=text,
    VoiceId='Amy'
    )

    file = open("voice.mp3", 'wb')
    file.write(response['AudioStream'].read())
    file.close()

    response = s3client.upload_file('./voice.mp3', 'stefany-polly-bucket', 'texto-falado.mp3')

    return main()



app.run("127.0.0.1", port="5000", debug=True)


