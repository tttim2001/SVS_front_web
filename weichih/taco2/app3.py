from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from preprocess_v1_1_function import preprocess
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)     # 建立Application物件

UPLOAD_FOLDER = './filelists/f1'
ALLOWED_EXTENSIONS = {'txt', 'mid'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

# 建立網站首頁的回應方式
@app.route("/", methods=['GET', 'POST'])  # 創造出網域下名為"/"的網址
def home():
    if request.method == 'POST':
        if request.form.get('action1') == 'preprocess':
            preprocess()
            return render_template("home.html")
        # 檢查POST有沒有符合檔名
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # 如果沒有選檔案，瀏覽器會送出一個沒有檔名的檔案
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 上傳檔案到目標資料夾
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    '''elif request.method == 'GET':
        return render_template("home.html")   # 回傳網站首頁內容
    '''
    return render_template("home.html")
    
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 檢查POST有沒有符合檔名
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # 如果沒有選檔案，瀏覽器會送出一個沒有檔名的檔案
        if  file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if  file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 上傳檔案到目標資料夾
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html> 
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''



#@app.route("/pred")
#def pred():
#    preprocess()
#    return render_template("pred.html")

if __name__ == "__main__":
    app.run() 