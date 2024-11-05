import os
import uuid
import datetime
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'

# Ensure the upload and output directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def generate_uid():
    """
    Generate a unique identifier (UUID).
    
    Returns:
        str: A unique identifier.
    """
    return str(uuid.uuid4())

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload via POST request.
    
    Returns:
        JSON: A JSON response containing the UID of the uploaded file or an error message.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        uid = generate_uid()
        filename = f"{timestamp}_{uid}_{file.filename}"
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return jsonify({'uid': uid})

@app.route('/status/<uid>', methods=['GET'])
def check_status(uid):
    """
    Check the processing status of an uploaded file.
    
    Args:
        uid (str): The unique identifier of the file.
    
    Returns:
        JSON: A JSON response containing the status of the file and its explanation if processed, or an error message.
    """
    uploads = os.listdir(UPLOAD_FOLDER)
    for upload in uploads:
        if uid in upload:
            timestamp, _, original_filename = upload.split('_', 2)
            output_path = os.path.join(OUTPUT_FOLDER, f"{timestamp}_{uid}_{original_filename}.json")
            if os.path.exists(output_path):
                with open(output_path, 'r') as f:
                    explanation = f.read()
                return jsonify({
                    'status': 'done',
                    'filename': original_filename,
                    'timestamp': timestamp,
                    'explanation': explanation
                })
            else:
                return jsonify({
                    'status': 'pending',
                    'filename': original_filename,
                    'timestamp': timestamp,
                    'explanation': None
                })
    return jsonify({'error': 'UID not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
