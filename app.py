from flask import Flask,jsonify,request
from flask_cors import CORS
app = Flask(__name__)
from werkzeug.utils import secure_filename
import os

CORS(app)
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'wav'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

import speech_recognition as sr
r = sr.Recognizer()
def getLanguage(argument):
    switcher = {
        1: "en-IN",
        2: "hi-IN",
        3: "kn-IN"
    }
    return switcher.get(argument, 0)
def getSelection():
    while True:
        try:
            userInput = int(input())
            if (userInput<1 or userInput>3):
                print("Not an integer! Try again.")
                continue
        except ValueError:
            print("Not an integer! Try again.")
            continue
        else:
            return userInput
            break
# Reading Audio file as source
# listening the audio file and store in audio_text variable
def startConvertion(path = 'sample.wav',lang = 'en-IN'):
    with sr.AudioFile(path) as source:
        print('Fetching File')
        audio_text = r.listen(source)
        # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        try:
        
            # using google speech recognition
            print('Converting audio transcripts into text ...')
            text = r.recognize_google(audio_text, language = lang)
            print(text)
            return text
        except Exception as e:
            print('Sorry.. run again...',e)
            return None

   

    


    
def WorkerAPI(filename,feature,language=None):
    print('feature-->',feature)
    if feature == 'cleanAudio':
        return jsonify({'status': 'success', 'message': 'cleaned audio file'})
    elif feature == 'transcribe' and language:
        languageSelection = getLanguage(int(language))
        # calling startConvertion method to start process
        text = startConvertion(filename,languageSelection) 
        if text:
            print('text-->',text)
            return jsonify({'status': 'success', 'message': 'Transcribed audio file','text':text})
        else:
            return jsonify({'status': 'failed', 'message': 'Unable to transcribe audio file'})
    elif feature == 'translate':
        return jsonify({'status': 'success', 'message': 'translated audio file'})
    elif feature == 'detectLanguage':
        return jsonify({'status': 'success', 'message': 'detected language'})
    elif feature == 'detectLanguageAndTranslate':
        return jsonify({'status': 'success', 'message': 'detected language and translated audio file'})
    elif feature == 'detectLanguageAndTranscribe':
        return jsonify({'status': 'success', 'message': 'detected language and transcribed audio'})
    
    

@app.route('/api/audioAI',methods=['GET','POST'])
def AudioAPI():
    print(request.files)
    #if file not found 
    if 'file' not in request.files:
        return jsonify({"status": "error","message": "Please Upload a file"})
    
    file = request.files['file']
    # if file found then we will store that file in upload folder
    # call our main function
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        data = request.form
        response = WorkerAPI(os.path.join(app.config['UPLOAD_FOLDER'], filename),data.get('feature'),data.get('language'))
        # print(data.get('feature'),data.get('language'))

        return response
    
    else: 
        return jsonify({"status": "error","message": 'Allowed file types are wav'})
    

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)