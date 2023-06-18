from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import traceback
import models
from werkzeug.utils import secure_filename
from sqlalchemy import select
import os
from database import get_db_session as db_session
import mask



UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "PNG", "JPG", "JPEG","jfif"}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    file_ext = filename.split(".")[1]
    if file_ext in ALLOWED_EXTENSIONS:
        return file_ext
    return False


@app.route("/")
def index(db = db_session()):
    return render_template("index.html")

@app.route("/register/", methods = ["GET", "POST"])
def register(db = db_session()):
    try:
        if request.method == "GET":
            return render_template("user_registration.html")
        
        if request.method == "POST":
            name = request.form.get("name")
            aadhar = int(request.form.get("ad_number"))
            a_back = request.files['back']
            
            a_front = request.files["front"]


            if len(str(aadhar))!=12:
                db.close()
                return {"detail":"invalid aadhar number"}, 400
            
            db_user =  select(models.User).where(models.User.aadhar_number == aadhar)

            db_user = db.scalars(db_user).all()
            if db_user !=[]:
                db.close()
                return {"detail":"aadhar already exists"}
            
            if a_back.filename == '' or a_front.filename == '':
                return redirect(request.url)
            
            if allowed_file(a_front.filename) and allowed_file(a_back.filename):
                back_filename = secure_filename(str(aadhar)+"_back.png")
                front_filename = secure_filename(str(aadhar)+"_front.png")

                a_front.save(os.path.join(app.config['UPLOAD_FOLDER'], front_filename))
                a_back.save(os.path.join(app.config['UPLOAD_FOLDER'], back_filename))

                mask.save_masked_aadhar(os.path.join(app.config['UPLOAD_FOLDER'], front_filename), aadhar, "front")
                mask.save_masked_aadhar(os.path.join(app.config['UPLOAD_FOLDER'], back_filename), aadhar, "back")

            

            new_user = models.User(name = name, aadhar_number = aadhar)

            db.add(new_user)
            db.commit()
            db.close()

            return redirect(url_for("index"))

    except Exception as err:
        traceback.print_exc()
        return {"detail":str(err)}, 400

@app.route("/delete/user/<aadhar_number>/")
def delete_user(aadhar_number,db = db_session()):
    try:
        db_user = select(models.User).where(models.User.aadhar_number == aadhar_number)
        db_user = db.scalars(db_user).first()
        db.delete(db_user)
        db.commit()
        db.close()

        return redirect(url_for("user_list"))
    except Exception as err:
        traceback.print_exc
        return {"detail":str(err)}, 400

@app.route("/show/aadhar/<aadhar_number>/")
def show_aadhar(aadhar_number):
    a_front = 'http://127.0.0.1:5000/uploads/' + str(aadhar_number)+"_front.png"
    a_back = 'http://127.0.0.1:5000/uploads/' + str(aadhar_number)+"_back.png"
    return render_template('show.html', back = a_back, front = a_front)


@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/user/all/')
def user_list(db = db_session()):
    try:
        db_users = select(models.User)
        db_users = db.scalars(db_users).all()
        db.close()
        return render_template("users.html", users = db_users)
    
    except Exception as err:
        traceback.print_exc
        return {"detail":str(err)}, 400

if __name__ == "__main__":
    app.run(debug = True)