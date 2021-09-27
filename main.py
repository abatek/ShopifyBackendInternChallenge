import os
import shutil
import sqlite3
from flask import g, Flask, render_template, request


DATABASE = r"pythonsqlite.db"

IMAGE_FOLDER = os.path.join('static', 'images')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER

@app.route('/')
@app.route('/index')
def show_index():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'dog.png')
    return render_template("index.html", user_image = full_filename)

@app.route('/add_image', methods=['POST'])
def add_image():
    try:
        key = request.form['key']
        path = request.form['path']

        con = get_db()
        cur = con.cursor()

        image_blob = convert_to_binary_data(path)
        print(image_blob)
        cur.execute("INSERT INTO images (key, image)VALUES(?, ?);", (key, image_blob))
        print('executed')
        con.commit()

        msg = "Record successfully added"
    except Exception as e:
        print(e)
        con.rollback()
        msg = "error in insert operation"

    return msg

@app.route('/get_image', methods=['GET'])
def get_image():
    try:
        key = request.args.get('key')

        con = get_db()
        cur = con.cursor()

        cur.execute(f'SELECT * FROM images WHERE key="{key}"')

        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], f'{key}.png')
        key, binary_image = cur.fetchone()
        write_file(binary_image, full_filename)

        msg = "Record successfully added"

        return render_template("index.html", user_image=full_filename)
    except:
        con.rollback()
        msg = "error in insert operation"

        return msg




def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def convert_to_binary_data(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binary_data = file.read()
    return binary_data

def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)

@app.route('/clear_images', methods=['GET'])
def clear_images():
    folder = 'static/images'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            return ('Failed to delete %s. Reason: %s' % (file_path, e))

    return "success"

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()



if __name__ == '__main__':
    app.run(debug=True)
