from os import system
from flask import Flask, request, render_template, send_file
import boto3

KEY_ID = "ASIAVF37VDXBV4PUBLOJ"
KEY_SECRET = "JBk//tklrsaaPGT/yZoHPOMqDEpOT/QsCnijAm1I"
TOKEN = "FwoGZXIvYXdzEMv//////////wEaDGFxgrMUrKE228IDuiLUAbw4UK9yVpF7MJ7Q11zPQM0khbJos+RY8bWeQT+DnBztC4KCtyR1ME4v0vdyDfknY0MGvMYVtScHkIra9yIr9qMIenc9SJ+r4oxsdjI1jxgRGGii6bt7dLP5HO8rHzI5KTe5G9oKQDUxjvbTtKIdkbdmHCcznDr2wT5e90KOvZMVszdYDa6Vn9XKgka7ik2r12I2Tar4JeGnN3UeS6JUrGH2W/P/7j89ITYlEKOXN0OWX28J9ZKEdieLiV/RArmALfykbVatgjcOzTRFbJVfk91lTbmoKIr6gI0GMi2EAKKQKaPGqfjWWFYy/t06v4VyxeoftzXPPPQqu3LRNg4EB27vg1bEc033L54="

textractcliente = boto3.client("textract", aws_access_key_id=KEY_ID, aws_secret_access_key=KEY_SECRET, region_name="us-east-1", aws_session_token=TOKEN)
s3client = boto3.client('s3', aws_access_key_id=KEY_ID, aws_secret_access_key=KEY_SECRET, region_name="us-east-1", aws_session_token=TOKEN)
pollyclient = boto3.client('polly', aws_access_key_id=KEY_ID, aws_secret_access_key=KEY_SECRET, region_name="us-east-1", aws_session_token=TOKEN)

class ObjFile():
    def __init__(self, txt):
        self.txt = txt

    def read(self, *args):
        return str.encode(self.txt)


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

@app.route("/reprodutor", methods=["GET", "POST", "PUT"])
def reprodutor():
    return render_template('reproducao.html')

@app.route("/extract", methods=["POST"])
def extractImage():
    file = request.files.get("file")
    binaryFile = file.read()
    response = textractcliente.detect_document_text(Document = {"Bytes": binaryFile})
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
    txt = request.args.get('txt')
    response = pollyclient.synthesize_speech(
    OutputFormat='mp3',
    Text=txt,
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
    response = textractcliente.detect_document_text(Document = {"Bytes": binaryFile})
    text = ""
    for block in response["Blocks"]:
        if (block["BlockType"] == "LINE"):
            text+= block["Text"]+' '

    #Armazenando o texto
    text = ObjFile(text)
    response = s3client.upload_fileobj(text, 'stefany-txt-bucket', 'texto-extraido.txt')

    #Criando Audio
    response = pollyclient.synthesize_speech(
        OutputFormat='mp3',
        LanguageCode='pt-BR',
        Text=text.txt,
        VoiceId='Camila'
    )

    #Armazenando o audio
    response = s3client.upload_fileobj(response['AudioStream'], 'stefany-polly-bucket', 'texto-falado.mp3')
    return render_template('reproducao.html')

@app.route('/voice', methods=["GET", "POST"])
def voice():
    # Recuperando o audio
    response = s3client.get_object(
        Bucket='stefany-polly-bucket',
        Key='texto-falado.mp3'
    )
    return send_file(response['Body'], mimetype='audio/mp3')


app.run("127.0.0.1", port="5000", debug=True)


