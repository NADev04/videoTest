# Video Processor

This project is a video processing application built with Flask and FFmpeg. It allows users to start video streams, retrieve stream manifests, and monitor stream health metrics.

## Features

- Start video streams from a given input URL.
- Generate HLS manifests for different video qualities.
- Monitor the health of active streams.

## Requirements

- Python 3.x
- FFmpeg
- Flask
- Postman (for testing API endpoints)

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd video_processor
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Ensure FFmpeg is installed:**

   - On macOS: `brew install ffmpeg`
   - On Ubuntu: `sudo apt-get install ffmpeg`
   - On Windows: Download from [FFmpeg official site](https://ffmpeg.org/download.html) and add to PATH.

## Usage

1. **Start the Flask application:**
   ```bash
   python src/api.py   ```

   The server will start on `http://127.0.0.1:5000`.

2. **Test API Endpoints using Postman:**

   - **Start a Stream:**
     - Method: `POST`
     - URL: `http://127.0.0.1:5000/stream/start`
     - Body:        ```json
       {
           "input_url": "/path/to/your/video.mp4"
       }       ```

   - **Get Stream Manifest:**
     - Method: `GET`
     - URL: `http://127.0.0.1:5000/stream/{stream_id}`

   - **Get Stream Metrics:**
     - Method: `GET`
     - URL: `http://127.0.0.1:5000/metrics/{stream_id}`

## Testing

1. **Run Unit Tests:**
   ```bash
   python -m unittest discover tests   ```

   This will run the tests defined in `tests/test.py`.

## Logging

Logging is set up using Python's `logging` module. You can adjust the logging level in `src/utils.py`.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
