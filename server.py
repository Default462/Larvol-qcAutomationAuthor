from flask import Flask, render_template, jsonify, request, send_file
import subprocess
from flask_cors import CORS
import os

UPLOAD_FOLDER = 'uploadedFiles'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)


with open("sampleConfig.py",'r', encoding='utf-8') as f:
    configSample = f.read()
    # print(configSample)

def runQCScript():
    # Specify the path to your external Python script
    script_path = './qc_automation.py'
    # command = ['python', script_path, '--myvar=' + str(4)]
    command = ['python', script_path]
    # Run the external script using subprocess
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, text=True)    
    # Access the captured output using result.stdout
    script_output = result.stdout
    print(script_output)
    # Return a response indicating success
    return({'status': 'success', 'message': script_output})

def runAuthorScript():
    script_path = './separate_authors.py'
    command = ['python', script_path]
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, text=True)
    script_output = result.stdout
    print(script_output)
    return({'status': 'success', 'message': script_output})

# runScript()
@app.route("/")
def hello_world():
    return render_template('./index.html')

@app.route('/test', methods=['GET'])
def handle_get():
    fileName = request.headers.get('fileName')
    with open('config.py','w') as f:
        f.write(configSample.replace('fileName',fileName))    
    return ({'status': 'success'})

@app.route('/runQcScript', methods=['POST'])
def handle_post():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    # print(request.files['file'])
    # print(request.data)
    
    file = request.files['file']
    # print('----',file.filename[-6:])
    if '.xlsx' not in file.filename[-5:]:
        return ({'status': 'failed','message':'Incorrect File type'})
    fileName = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(fileName)
    print('fileName')
    # return
    with open('config.py','w') as f:        
        f.write(configSample.replace('fileName',file.filename))
    output = runQCScript()    
    with open(f'{fileName.rstrip('.xlsx')}_QC_comments.txt','r',encoding='utf-8') as f:
        qcComments = f.read()
    with open(f'{fileName.rstrip('.xlsx')}_sponsor.txt','r',encoding='utf-8') as f:
        sponsorInfo = f.read()
    os.remove(f'{fileName.rstrip('.xlsx')}_QC_comments.txt')
    os.remove(f'{fileName.rstrip('.xlsx')}_sponsor.txt')
    os.remove(f'{fileName}')
    return ({'status': 'success','qcComments':qcComments,'sponsorInfo':sponsorInfo})

@app.route('/runAuthor', methods=['POST'])
def handle_post_author():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})    
    file = request.files['file']
    if '.xlsx' not in file.filename[-5:]:
        return ({'status': 'failed','message':'Incorrect File type'})
    fileName = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(fileName)
    print('fileName')
    with open('config.py','w') as f:        
        f.write(configSample.replace('fileName',file.filename))
    output = runQCScript()

    # with open(f'final.xlsx','r') as f:
    #     authors = f.read()
    # return ({'status': 'success','authors':authors})
    return send_file('final.xlsx', as_attachment=True)

