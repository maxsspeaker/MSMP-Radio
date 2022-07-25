from flask import Flask,send_file,request,jsonify,render_template,redirect,url_for,session
from flask import cli
from flask_cors import CORS,cross_origin
import vlc
import requests
from threading import Thread
import time
import traceback
import re

radioList=[]
with open("Radios.txt", "r") as file:
    for radioURL in file:
         radioList.append(radioURL.replace("\n",""))

titleTrekPlayNow="FirkifoxBox463463"
artistTrekPlayNow="Maxsspeaker"
Num=0

Login = 'Maxsspeaker'
Pass = 'admin'

vlc_instance = vlc.Instance()

NewPlaerVLC = vlc_instance.media_player_new()

media = vlc_instance.media_new(radioList[Num])
print(radioList[Num])
     
NewPlaerVLC.set_media(media)

#MediaPlayer.play()

app = Flask("MSMP Radio")
app.config['SECRET_KEY'] = 'firksfirksMyaBox'
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:port"}})
#cli.show_server_banner = lambda *_: None

#@app.route("/PlayBackWeb", methods=['POST','OPTIONS'])
#@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])



Plaer=True

def radioParseDef():
    global StreamUrlPlayNow
    global titleTrekPlayNow
    global artistTrekPlayNow
    global Plaer
    global msmp_streamIcon
    global version
    global NewPlaerVLC
    global discord
    global Num
    global radioList
    print("Start radioParseDef")
    radio_session = requests.Session()
    encoding = 'latin1'
    info = ''
    while Plaer:
      if str(NewPlaerVLC.get_state())=="State.Playing":
       time.sleep(2)   
       try:
        radio = radio_session.get(radioList[Num], headers={'Icy-MetaData': '1'}, stream=True)
    
        metaint = int(radio.headers['icy-metaint'])
    
        stream = radio.raw
    
        audio_data = stream.read(metaint)
        meta_byte = stream.read(1)
    
        if (meta_byte):
            meta_length = ord(meta_byte) * 16
    
            meta_data = stream.read(meta_length).rstrip(b'\0')
    
            stream_title = re.search(br"StreamTitle='([^']*)';", meta_data)
    
    
            if stream_title:
    
                stream_title = stream_title.group(1).decode(encoding, errors='replace')
    
                if info != stream_title:
                   print('Now playing: ', stream_title)
                   info = stream_title
                   if not(stream_title==""):
                    try:
                        stream_title =stream_title.split("- ")
                        titleTrekPlayNow=stream_title[1]
                        artistTrekPlayNow=stream_title[0]
                    except:
                        titleTrekPlayNow=stream_title
                        artistTrekPlayNow=""
                else:
                    pass
    
            else:
                if not str(NewPlaerVLC.get_state())=="State.Playing":
                    titleTrekPlayNow=playlist[Num]["Name"]
                    artistTrekPlayNow=""
                    print('No StreamTitle!')
    
       except:print(traceback.format_exc());time.sleep(10)
      else:time.sleep(10)

radioParsePotoc = Thread(target=radioParseDef)
radioParsePotoc.setDaemon(True)
radioParsePotoc.start()

@app.route('/', methods=['GET', 'POST'])
def mainPG():
     error = None
     if(session.get("logged_in")==True):
         return redirect(url_for('home'))
     else:
         return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    global Login 
    global Pass 
    error = None
    if request.method == 'POST':
        if request.form['username'] != Login or request.form['password'] != Pass:
            error = 'Недействительные учетные данные. Пожалуйста, попробуйте еще раз.'
        else:
            session["logged_in"] = True
            return redirect(url_for('home'))
    if(session.get("logged_in")==True):
         return redirect(url_for('home'))
    else:
         return render_template('login.html', error=error)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
     session["logged_in"] = False
     return redirect(url_for('mainPG'))


@app.route('/RadioBox', methods=['GET'])
def home():
     global titleTrekPlayNow
     global artistTrekPlayNow
     global StreamUrlPlayNow
     if(session.get("logged_in")==True):
          try:command = request.args['cm'] 
          except:command=None
          if(command=="play"):
               NewPlaerVLC.play()
          if(command=="stop"):
               NewPlaerVLC.stop()
          return render_template('home.html',titleTrekPlayNow=titleTrekPlayNow,artistTrekPlayNow=artistTrekPlayNow)

     else:
          return redirect(url_for('login'))

@app.route('/RadioBox', methods=['GET'])
def PlayControl():
     if(session.get("logged_in")==True):
          return "ok"
     else:
          return redirect(url_for('login'))

#MediaPlayer.play()

app.run(debug=False,host='0.0.0.0', port='34681')
Plaer=False
