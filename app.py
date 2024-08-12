from flask import Flask, request, jsonify, send_file
from rembg import remove
from PIL import Image
import io
import os

app = Flask(__name__)

@app.route('/remove-background', methods=['POST'])
def remove_background():
    if 'file' not in request.files:
        app.logger.error('No file part in the request')
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        app.logger.error('No file selected for uploading')
        return jsonify({'error': 'No file selected for uploading'}), 400

    try:
        input_image = file.read()

        # Remove the background
        output_image = remove(input_image)

        # Convert the output to an image object
        output = Image.open(io.BytesIO(output_image)).convert("RGBA")

        # Create a white background
        white_background = Image.new("RGBA", output.size, (255, 255, 255, 255))

        # Composite the original image onto the white background
        combined = Image.alpha_composite(white_background, output).convert("RGB")

        # Save the output image to a BytesIO object
        output_bytes = io.BytesIO()
        combined.save(output_bytes, format="PNG")
        output_bytes.seek(0)

        app.logger.info('Image processed and returned as bytes')
        return send_file(output_bytes, mimetype='image/png')

    except Exception as e:
        app.logger.error(f'An error occurred during processing: {str(e)}')
        return jsonify({'error': 'An error occurred during processing'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)