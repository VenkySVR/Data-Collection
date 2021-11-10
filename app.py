from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import os
VIDEO_FOLDER = 'uploads/videos/'
AUDIO_FOLDER = 'uploads/audios/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = VIDEO_FOLDER
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///form.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

import moviepy.editor as mp
from pydub import AudioSegment
from datetime import datetime

def name_gen(languageid,gender):
    basename = languageid +"_"+ gender
    suffix = datetime.now().strftime("%y%m%d_%H%M%S")
    filename = "_".join([basename, suffix]) # e.g. 'hindi_male_120508_171442'
    return filename + ".webm"


def to_audio(videofile):
    video_path = VIDEO_FOLDER + videofile + '.webm'
    audio_path = AUDIO_FOLDER + videofile + '.wav'
    video_clip = mp.VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_path)
    audio = AudioSegment.from_file(audio_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export(audio_path, format="wav")



class Form(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    speakerid = db.Column(db.Integer,nullable=False)
    languageid = db.Column(db.String,nullable=False)
    gender = db.Column(db.String,nullable=False)
    agegroup = db.Column(db.String,nullable=False)
    videoname = db.Column(db.String,nullable=False)
    date_created = db.Column(db.DateTime , default=datetime.utcnow)
    def __repr__(self) -> str:
        return f"{self.sno} - {self.speakerid}"

@app.route("/",methods=['GET','POST'])
def home():
    if request.method=='POST':
        languageid = request.form['languageid']
        gender = request.form['gender']
        agegroup = request.form['agegroup']
        speakerid = request.form['speakerid']
        video_name = name_gen(languageid,gender)
        recFile = request.files['file']
        recFile.save(os.path.join(app.config['UPLOAD_FOLDER'], video_name))
        print(languageid,gender,agegroup,speakerid,video_name)
        data = Form(languageid=languageid,gender=gender,agegroup=agegroup,speakerid=speakerid , videoname= video_name )
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('index.html')

@app.route("/details")
def details():
    details=Form.query.all()
    # print(details)
    return render_template('details.html',details=details)


if __name__=="__main__":
    db.create_all()
    app.run(debug=False,port=8113)    