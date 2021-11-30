from flask import Flask, request, render_template, send_file
import boto3

KEY_ID = "ASIAVF37VDXBXGIWNWCK"
KEY_SECRET = "xdZfpGcObC6mIocqj1/yy3zw7cZXsQz3zV2JmYLM"
TOKEN = "FwoGZXIvYXdzEDYaDGCQXSLr8xJSf7hyVCLUAae1N4mMVLj6MljkSxpPtUn0jnj02nFrzMLDy/WJ7orqzJabixV6iS5hfjBAfPtMt+7pqKlCCJ+GpJ84WMt3KoWERsovQALqWbRzh0z6qAO/DSoTNo0c85LImLsTmGXim1Gtp9kSu2HOX6v9Eafs29UMV3S1dHAqwL3eRwcKC2F3Gm8nucAdjUomirCQW+R/GwOplP/T+M/MrvfUFjjegHLgcoGlvsX/ftp8xYhWwNi8caXMfgVgwzbYcMrWcirFwmKRLygMKIfjNkCpGJsk4kQdr2LdKLS+mI0GMi2X4HMhrNKfG8ny+ZGyqZR8i238I5BweufbG12vpbipzOxR6Gl86EB+dSN9HrM="

textractcliente = boto3.client("textract", aws_access_key_id=KEY_ID, aws_secret_access_key=KEY_SECRET, region_name="us-east-1", aws_session_token=TOKEN)
s3client = boto3.client('s3', aws_access_key_id=KEY_ID, aws_secret_access_key=KEY_SECRET, region_name="us-east-1", aws_session_token=TOKEN)
pollyclient = boto3.client('polly', aws_access_key_id=KEY_ID, aws_secret_access_key=KEY_SECRET, region_name="us-east-1", aws_session_token=TOKEN)

class ObjFile():
    def __init__(self, txt):
        self.txt = txt

    def read(self, *args):
        return str.encode(self.txt)


app = Flask(__name__)

# Assets
@app.route('/logo', methods=["GET"])
def logo():
    return send_file('../assets/img/b_UFRPE.png', mimetype='image/png')

@app.route('/css', methods=["GET", "POST"])
def css():
    return send_file('../assets/css/style.css', mimetype='text/css')

@app.route('/js', methods=["GET", "POST"])
def js():
    return send_file('../assets/js/script.js', mimetype='text/js')


# Pages
@app.route("/", methods=["GET", "POST", "PUT"])
def main():
    return render_template('index.html')

@app.route("/reprodutor", methods=["GET", "POST", "PUT"])
def reprodutor():
    return render_template('reproducao.html')

# Features

@app.route("/extract", methods=["POST", "GET"])
def extractImage():
    file = request.files.get("file")
    binaryFile = file.read()
    response = textractcliente.detect_document_text(Document = {"Bytes": binaryFile})
    text = ""
    for block in response["Blocks"]:
        if (block["BlockType"] == "LINE"):
            text+= block["Text"]+' '

    return text

@app.route("/createbucket", methods=["POST"])
def createBucket():
    name = request.args.get('name')
    response = s3client.create_bucket(Bucket=name)
    return response

@app.route("/upfile", methods=["POST"])
def upFile():
    file = request.files.get("file")
    response = s3client.put_object(Body=file, Bucket='stefany-img-bucket', Key='img.png')
    return response


@app.route("/polly", methods=["POST"])
def polly():
    txt = request.args.get('txt')
    response = pollyclient.synthesize_speech(
        OutputFormat='mp3',
        LanguageCode='pt-BR',
        Text=txt,
        VoiceId='Camila'
    )
    s3client.upload_fileobj(response['AudioStream'], 'stefany-polly-bucket', 'texto-falado.mp3')
    return response['ResponseMetadata']['RequestId']

@app.route('/voice', methods=["GET", "POST"])
def voice():
    # Recuperando o audio
    response = s3client.get_object(
        Bucket='stefany-polly-bucket',
        Key='texto-falado.mp3'
    )
    return send_file(response['Body'], mimetype='audio/mp3')

@app.route('/img', methods=["GET", "POST"])
def img():
    # Recuperando a imagem
    response = s3client.get_object(
        Bucket='stefany-img-bucket',
        Key='img.png'
    )
    print(response['Body'].read())
    return send_file(response['Body'], mimetype='image/png')


@app.route('/aws', methods=["GET", "POST"])
def aws():
    file = request.files.get("file")

    #Extração do texto
    binaryFile = file.read()
    response = textractcliente.detect_document_text(Document = {"Bytes": binaryFile})
    text = ""
    for block in response["Blocks"]:
        if (block["BlockType"] == "LINE"):
            text+= block["Text"]+' '

    #Armazenando o texto
    text = ObjFile(text)
    s3client.upload_fileobj(text, 'stefany-txt-bucket', 'texto-extraido.txt')

    #Criando Audio
    response = pollyclient.synthesize_speech(
        OutputFormat='mp3',
        LanguageCode='pt-BR',
        Text=text.txt,
        VoiceId='Camila'
    )

    #Armazenando o audio
    s3client.upload_fileobj(response['AudioStream'], 'stefany-polly-bucket', 'texto-falado.mp3')

    return render_template('reproducao.html')


app.run("127.0.0.1", port="5000")


