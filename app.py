from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import base64
import io
from PIL import Image

# our library
from GMValuator.matching import matching

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET','POST'])
def index():
    return render_template("index.html")

@app.route('/match', methods=['GET', 'POST'])
def match():
    generated_img = request.files.get('img')

    # save
    generated_path = './static/img/generated_img.png'
    generated_img.save(generated_path)

    matched_images, scores = matching(generated_path)

    for idx, img in enumerate(matched_images):
        img.save(f'./static/img/{idx}.jpg')

    image_paths = ['./static/img/0.jpg', './static/img/1.jpg', './static/img/2.jpg', './static/img/3.jpg']
    images_data = []

    for path in image_paths:
        with open(path, 'rb') as f:
            image_bytes = f.read()
            base64_data = base64.b64encode(image_bytes).decode('utf-8')
            images_data.append(base64_data)

    for score in scores:
        images_data.append(score)

    # # transform PIL to base64
    # for img in matched_images:
    #     img = base64.b64encode(img.tobytes()).decode('utf-8')
    #     image_data.append(img)

    return jsonify(images=images_data)

if __name__ == '__main__':
    app.run()