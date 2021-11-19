from flask import Flask, render_template, redirect, url_for, jsonify, request, Response, send_from_directory
import shutil
import os
import subprocess
from subprocess import run, PIPE
import datetime
import time
import json
import serial
import serial.tools.list_ports
import shutil
import random
import PIL
from PIL import Image
import threading
import webbrowser


app = Flask(__name__, static_folder='static', static_url_path='/static')


command_dir = '/home/paulina/Desktop/exhibition-code/scripts'
best_pose = os.path.join(command_dir, "choose_best_pose.py")
synthesize_file = os.path.join(command_dir, "exhibition_script.py")
crop_picture = os.path.join(command_dir, "preprocess_image.py")
deepVoice = os.path.join(command_dir, "deep_vocoder.py")
driving_videos_dir = '/home/paulina/Desktop/driving_videos'
predictor_file = '/home/paulina/Desktop/exhibition-code/predictor/shape_predictor_68_face_landmarks.dat'
path_dir = '/home/paulina/Desktop/visitors/'

SHARED_DIR = '/home/paulina/Desktop/td_share'
SHARED_SUBDIR = '/home/paulina/Desktop/td_share/finish'

DRIVING_VIDEOS_SUBDIR = ''
VISITOR_RESULT_DIR = ''
CURRENT_DIR = ''

tddata = {
    'started': False,
}

ports = serial.tools.list_ports.comports(include_links=False)


@app.route("/", methods=['GET', 'POST'])
def index():
    removeFiles()

    return render_template('welcome.html')


def removeFiles():
    for f in os.listdir(SHARED_DIR):
        if f.endswith(".mp4") or f.endswith(".mp3") or f.endswith(".png"):
            os.remove(os.path.join(SHARED_DIR, f))

    for ff in os.listdir(SHARED_SUBDIR):
         os.remove(os.path.join(SHARED_SUBDIR, ff))

    return "folder emptied"


@app.route("/agreement", methods=['POST'])
def agree():

    if request.method == 'POST':
        if request.form.get("consent"):
            print(request.form.get("consent"))
            global CURRENT_DIR
            CURRENT_DIR = os.path.join(
            path_dir, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
            os.makedirs(CURRENT_DIR)
            return redirect(url_for('testIntro'))

    return render_template('mainpage.html')


@app.route("/personalityTestIntro")
def testIntro():
    return render_template('personalityTestIntro.html')


@app.route("/personalityTest", methods=['POST', 'GET'])
def takeTest():
    return render_template('personalityTest.html')


@app.route('/postmethod', methods=['POST', 'GET'])
def get_json_data():
    jsdata = request.form['javascript_data']
    print("JSON Data: %s" % jsdata)
    global DRIVING_VIDEOS_SUBDIR
    DRIVING_VIDEOS_SUBDIR = driving_videos_dir + '/' + jsdata
    return DRIVING_VIDEOS_SUBDIR

@app.route("/videoInstructions", methods=['GET', 'POST'])
def videoIns():
    return render_template('videoInstructions.html')

@app.route("/takeVideo", methods=['GET', 'POST'])
def takeVideo():
    return render_template('takeVideo.html')

@app.route("/turnLEDon", methods=['POST'])
def turnLedOn():
    if request.method == 'POST':
        for port in ports:
            ser = serial.Serial('%s' % port.device, 115200)
            ser.write(b'1')
    return 'ok'

@app.route("/turnLEDoff", methods=['POST'])
def turnLedOff():
    if request.method == 'POST':
        for port in ports:
            ser = serial.Serial('%s' % port.device, 115200)
            ser.write(b'0')
    return 'ok'

@app.route('/saveVideo', methods=['POST'])
def download_file():
    global CURRENT_DIR
    with open(CURRENT_DIR + "/visitor.webm" , 'wb') as f:
        f.write(request.data)
        f.close()
    return "Video saved!"

@app.route("/video2images", methods=['GET', 'POST'])
def video2images():
     
    global CURRENT_DIR
    input_video = CURRENT_DIR + "/" + "visitor.webm"
    output_path = CURRENT_DIR 
    cmd = ["ffmpeg", "-i", input_video, "-vsync", "vfr", "-q:v", "100", output_path + "/img_%03d.png"]
    subprocess.Popen(cmd).wait() 

    return render_template('videocomplete.html')


@app.route('/video2images_background_task',  methods=['POST'])
def findBestPose():
    if request.method == 'POST':
        global CURRENT_DIR
        path_bestPose = CURRENT_DIR + "/"
        calibration_video = "/home/paulina/Desktop/driving_videos/calibration.mkv"
        cmd = ["python", best_pose, calibration_video, path_bestPose, predictor_file]
        subprocess.Popen(cmd).wait()
    return ("Pose found!")


@app.route("/takeAudio", methods=['GET', 'POST'])
def takeAudio():
    return render_template('takeAudio.html')


@app.route('/saveAudio', methods=['POST'])
def downloadAudio():
    global CURRENT_DIR

    if os.path.exists(CURRENT_DIR + "/" + "audio.mp3" ):
        os.remove(CURRENT_DIR + "/" + "audio.mp3" ) 

    with open(CURRENT_DIR + '/audio.mp3', 'wb') as f:
        f.write(request.data)
        f.close()
    proc = run(['ffprobe', '-of', 'default=noprint_wrappers=1', CURRENT_DIR + '/audio.mp3'], text=True, stderr=PIPE)
    cutOff()
    return proc.stderr 


def cutOff():
    global CURRENT_DIR

    if os.path.exists( CURRENT_DIR + "/" + "enhancedAudio.mp3" ):
        os.remove( CURRENT_DIR + "/" + "enhancedAudio.mp3" ) 
        
    cmd =['ffmpeg', '-i' , CURRENT_DIR + "/" + 'audio.mp3', '-ss', '00:00:03', '-to', '00:00:13' ,'-c', 'copy', CURRENT_DIR + "/" +'enhancedAudio.mp3']
    subprocess.Popen(cmd).wait()
    return "Voice trimmed"  


@app.route('/preprocess', methods=['GET', 'POST'])
def deepfake():
    return render_template('preprocess.html')

@app.route('/touchTD', methods=['GET'])
def start_TD():
    global tddata
    if 'started' in request.args:
        started = bool(int(request.args.get('started')))
        tddata['started'] = started
    return jsonify(tddata)
   

@app.route('/preprocess_background_task', methods=['POST'])
def preprocessVideo():
   
    """ # paths used for testing 
    DRIVING_VIDEOS_SUBDIR = '/home/paulina/Desktop/driving_videos/1/'
    VISITOR_RESULT_DIR = '/home/paulina/Desktop/visitors/2021-05-05_18-35-44/deepfakes'
    counter = 0
    counter1 = 0
    visitor_best_image = '/home/paulina/Desktop/visitors/test/best_pose.png'
    visitor_voice_sample = '/home/paulina/Desktop/visitors/test/enhancedAudio.mp3' """
    
    
    global CURRENT_DIR
    global DRIVING_VIDEOS_SUBDIR
    
    counter = 0
    counter1 = 0
    
    if request.method == 'POST':
        if not os.path.isfile(synthesize_file):
            raise Exception("{}: no such file".format(synthesize_file))
    
        if not os.path.exists(CURRENT_DIR + "/deepfakes"):
            deepfakes_dir = "deepfakes"
            global VISITOR_RESULT_DIR
            VISITOR_RESULT_DIR = os.path.join(CURRENT_DIR, deepfakes_dir)
            os.makedirs(VISITOR_RESULT_DIR)
            print("Directory '%s' created" %VISITOR_RESULT_DIR)
        else:
            VISITOR_RESULT_DIR = CURRENT_DIR + "/deepfakes"


    visitor_best_image = CURRENT_DIR + "/" + "best_pose.png"
    crop_image(visitor_best_image, VISITOR_RESULT_DIR)                 
    visitor_voice_sample = CURRENT_DIR + "/" + "enhancedAudio.mp3" 
    shutil.copy2(visitor_best_image , SHARED_DIR)
    shutil.copy2(visitor_voice_sample, SHARED_DIR)

    time.sleep(5)

    for textFile in sorted(os.listdir(DRIVING_VIDEOS_SUBDIR)):
        if textFile.endswith(".txt"):
            with open(DRIVING_VIDEOS_SUBDIR + "/" + textFile, 'r', encoding='utf-8-sig') as f:
                file_content = f.read().replace('\n', '')
                deepfakeAudio(deepVoice, file_content, visitor_voice_sample, VISITOR_RESULT_DIR)

    time.sleep(5)
    
    for filename in sorted(os.listdir(DRIVING_VIDEOS_SUBDIR)):
        if filename.endswith(".mkv") :
            driving_video = DRIVING_VIDEOS_SUBDIR + "/" + filename
            visitor_result_video = VISITOR_RESULT_DIR + "/" + "deepfake%s" % counter + ".mp4"
            # visitor_result_video_enhanced = VISITOR_RESULT_DIR + "/" + "enhanced%s" % counter + ".mp4"
            counter += 1
            deepfakeVideo(synthesize_file, driving_video, visitor_best_image, visitor_result_video)
            # deepfakeVideoEnhanced(synthesize_file, driving_video, visitor_best_image, visitor_result_video, visitor_result_video_enhanced)  
     
    time.sleep(5)

    for videoOrAudio in sorted(os.listdir(VISITOR_RESULT_DIR + "/")):
          # if videoOrAudio.startswith("enhanced") and videoOrAudio.endswith(".mp4"):
          if videoOrAudio.endswith(".mp4"):
            videoname = VISITOR_RESULT_DIR +  "/" + videoOrAudio
            print(videoname)
            audioname = os.path.splitext(videoname)[0] + ".wav"
            print(audioname)
            combined_output = VISITOR_RESULT_DIR  + "/" + "avDeepfake%s" % counter1 + ".mp4"
            combineAudioVideo(videoname, audioname, combined_output)
            counter1 += 1
            shutil.copy2(combined_output, SHARED_DIR)

    finalVideo(visitor_best_image, visitor_voice_sample) 

    return "Preprocessing finished successfuly!" 

    
def crop_image(readyToCrop, output_path):
    image = PIL.Image.open(readyToCrop)
    width, height = image.size
    smaller = min(width, height)
    if(width < height):
        center = height/2
        upperbound = center + width/2
        lowerbound = center - width/2
        box = (0, lowerbound, width, upperbound)
        crop = image.crop(box)
        crop.save(os.path.join(output_path,readyToCrop))
    elif(width > height):
        center = width / 2
        upperbound = center + height / 2
        lowerbound = center - height / 2
        box = (lowerbound, 0, upperbound, height)
        crop = image.crop(box)
        crop.save(os.path.join(output_path,readyToCrop))
    else:
        print("")
    
    return "Image Cropped" 

def deepfakeAudio(input_script, input_file, input_visitor_file, output_visitor_file):
    cmd = ['python', input_script, input_file, input_visitor_file, output_visitor_file]
    subprocess.Popen(cmd).wait()

    return "Done with audio" 

def deepfakeVideo(input_script, input_file, input_visitor_file, output_visitor_file):
    cmd = ['python', input_script, input_file, input_visitor_file, output_visitor_file]
    subprocess.Popen(cmd).wait()
    return "Done with video" 

def combineAudioVideo(input_video, input_audio, output_video):
    cmd = ["ffmpeg","-i", input_video, "-itsoffset", "1.5", "-i", input_audio, "-c:v", "copy", "-map", "0:v:0", "-map", "1:a:0", output_video]      
    subprocess.Popen(cmd).wait() 
    return "Done combining"
 
def finalVideo(input_visitor_fileVideo, input_visitor_fileAudio):
    finishVideo = "/home/paulina/Desktop/driving_videos/finish/finish.mkv"
    finishAudio = "/home/paulina/Desktop/driving_videos/finish/finish.txt"
    with open(finishAudio, 'r', encoding='utf-8-sig') as f:
        audio_content =  f.read().replace('\n', '')
        deepfakeAudio(deepVoice,audio_content,input_visitor_fileAudio, VISITOR_RESULT_DIR)

    finish_output = VISITOR_RESULT_DIR  + "/" + "getOut" + ".mp4"
    deepfakeVideo(synthesize_file, finishVideo, input_visitor_fileVideo, finish_output)
    
    finish_AudioOutput= VISITOR_RESULT_DIR  + "/" + "deepfake3.wav"
    final_Combined = VISITOR_RESULT_DIR  + "/" + "avGetOut" + ".mp4"
    combineAudioVideo(finish_output, finish_AudioOutput,final_Combined )
    shutil.copy2(final_Combined, SHARED_SUBDIR)
    
    return "Final Video rendered" 

@app.route('/reload/<int:param>', methods=['POST'])
def loading(param):
    time.sleep(param)
    return redirect(url_for('index'))


if __name__ == '__main__':
    port = 5000 + random.randint(0, 999)
    url = "http://127.0.0.1:{0}".format(port)

    threading.Timer(1.25, lambda: webbrowser.open_new(url) ).start()

    app.run(host="0.0.0.0", port=port, debug=True)
