from flask import Flask, request, jsonify
import os
import uuid
from processor import StreamProcessor

app = Flask(__name__)

# In-memory store for active streams
streams = {}

@app.route('/stream/start', methods=['POST'])
def start_stream():
    data = request.get_json()
    input_url = data.get('input_url')
    
    if not input_url:
        return jsonify({"error": "Input URL is required"}), 400

    stream_id = str(uuid.uuid4())
    output_dir = os.path.join('output', stream_id)

    processor = StreamProcessor(stream_id, input_url, output_dir)
    processor.start_stream()

    streams[stream_id] = processor
    return jsonify({"message": "Stream started", "stream_id": stream_id}), 200

@app.route('/stream/<stream_id>', methods=['GET'])
def get_stream_manifest(stream_id):
    processor = streams.get(stream_id)

    if not processor:
        return jsonify({"error": "Stream not found"}), 404

    manifest_path = os.path.join(processor.output_dir, '720p.m3u8')  # Example: returning 720p variant

    if not os.path.exists(manifest_path):
        return jsonify({"error": "Manifest not available yet"}), 404

    with open(manifest_path, 'r') as file:
        manifest_content = file.read()

    return jsonify({"manifest": manifest_content}), 200

@app.route('/metrics/<stream_id>', methods=['GET'])
def get_stream_metrics(stream_id):
    processor = streams.get(stream_id)

    if not processor:
        return jsonify({"error": "Stream not found"}), 404

    metrics = processor.monitor_health()
    return jsonify({"metrics": metrics}), 200

if __name__ == '__main__':
    app.run(debug=True)
