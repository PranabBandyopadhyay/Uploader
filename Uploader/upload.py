import os
import urllib.request
from app import app
from flask import Flask, flash, request, redirect, render_template, session
from werkzeug.utils import secure_filename
import subprocess
import json

ALLOWED_EXTENSIONS = set(['control', 'data'])


def allowed_file(filename):
    return '_' in filename and filename.rsplit('_', -1)[0].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def login_form():
    return render_template('login.html')

@app.route('/upload')
def upload_form():
    if session.get('user'):
        flash('Welcome :' + session.get('user'))
        return render_template('upload.html')
    else:
        return redirect('/')

@app.route('/', methods=['POST'])
def login():
    if request.method == 'POST':
        uname = str(request.form['uname'])
        pword = str(request.form['pword'])
        cred_filename = "cred.json"
        with open(cred_filename, 'r') as open_file:
            database = json.load(open_file)
        if uname in database.keys():
            if pword == database[uname]:
                print("Here. correct value")
                session['user'] = uname
                return redirect('/upload')
            else:
                print("Here. incorrect pass value")
                flash('Username or Password wrong')
                #return redirect(request.url)
        else:
            print("Here. incorrect user value")
            flash('Username or Password wrong')
            #return redirect(request.url)
        return redirect('/')


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST' and session.get('user'):
        os.popen("bash clean.sh")
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')
        path = request.form['path']
        env = request.form['env']
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash('File(s) successfully uploaded')
                process = subprocess.Popen("bash upload.sh " + path + " " + env, shell=True, stdout=subprocess.PIPE)
                process.wait()
                ret = process.returncode
                if ret:
                    flash('Files transfer failed')
                else:
                    flash('Files transferred to ' + env + ' at path : '+ path)
            else:
                flash('File(s) invalid, cannot be uploaded')
        return redirect('/upload')
    else:
        return redirect('/')


@app.route('/signout', methods=['POST'])
def signout():
    if request.method == 'POST':
        session.clear()
        return redirect('/')


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=61112)