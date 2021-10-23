from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///form.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class Form(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    speakerid=db.Column(db.Integer,nullable=False)
    languageid=db.Column(db.String,nullable=False)
    gender=db.Column(db.String,nullable=False)
    agegroup=db.Column(db.String,nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.speakerid}"

@app.route("/",methods=['GET','POST'])
def home():
    if request.method=='POST':
        languageid=request.form['languageid']
        gender=request.form['gender']
        agegroup=request.form['agegroup']
        speakerid=request.form['speakerid']
        data=Form(languageid=languageid,gender=gender,agegroup=agegroup,speakerid=speakerid)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('index.html')

@app.route("/details")
def details():
    details=Form.query.all()
    print(details)
    return render_template('details.html',details=details)

if __name__=="__main__":
    app.run(debug=False,port=8000)    