from flask import Flask, request, jsonify, render_template
import cv2
import easyocr
import os
import time  # Import time module

app = Flask(__name__, static_url_path='/static')

# Function to preprocess the image
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    inverted = cv2.bitwise_not(thresh)
    return inverted

# Endpoint to handle image upload and text recognition
@app.route('/upload', methods=['POST'])
def upload_image():
    start_time = time.time()  # Record start time

    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['image']
    image_path = "temp.png"  # Temporary path to save the uploaded image
    file.save(image_path)

    preprocessed_image = preprocess_image(image_path)

    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(preprocessed_image)

    # Convert result into a JSON-serializable format
    json_result = []
    for detection in result:
        text = detection[1]
        confidence = detection[2]
        json_result.append({'text': text})

    # Clean up temporary image file
    os.remove(image_path)

    end_time = time.time()  # Record end time
    execution_time = end_time - start_time  # Calculate execution time

    return jsonify({'result': json_result, 'execution_time': execution_time})

@app.route('/')
def index():
    return render_template('index1.html')

if __name__ == '__main__':
    app.run(debug=True)
