from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET','POST'])
def index():
    return render_template("index.html")

@app.route('/match', methods=['GET', 'POST'])
def match():
    generated_img = request.files.get('img')
    generated_img.save('./test.jpg')

    image_paths = ['./static/img/me.jpg', './static/img/test.jpg', './static/img/me.jpg', './static/img/test.jpg']
    images_data = []

    for path in image_paths:
        with open(path, 'rb') as f:
            image_bytes = f.read()
            base64_data = base64.b64encode(image_bytes).decode('utf-8')
            images_data.append(base64_data)

    return jsonify(images=images_data)

if __name__ == '__main__':
    app.run()