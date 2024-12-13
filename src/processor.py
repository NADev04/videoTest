import subprocess
import os
import threading
from typing import Dict

class StreamProcessor:
    def __init__(self, stream_id: str, input_url: str, output_dir: str):
        self.stream_id = stream_id
        self.input_url = input_url
        self.output_dir = output_dir
        self.health_metrics = {}
        self.process = None

    def start_stream(self) -> None:
        """Initialize stream processing."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        threading.Thread(target=self._process_stream).start()

    def _process_stream(self) -> None:
        # try:
            command = [
                'ffmpeg', '-i', self.input_url,
                '-vf', 'scale=-1:720', '-c:v', 'libx264', f'{self.output_dir}/720p.m3u8',
                '-vf', 'scale=-1:480', '-c:v', 'libx264', f'{self.output_dir}/480p.m3u8',
                '-hls_time', '4', '-hls_playlist_type', 'event'
            ]
            print(f"Running command: {' '.join(command)}")
            self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.process.wait()
            print(f"Output directory: {self.output_dir}")
        # except Exception as e:
        #     print(f"Error processing stream: {e}")

    def generate_variants(self) -> None:
        """Handle transcoding to different qualities."""
        # Included in the start_stream FFmpeg process
        pass

    def create_manifest(self) -> None:
        """Generate HLS manifest."""
        # HLS manifest files (.m3u8) are auto-generated in start_stream
        pass

    def monitor_health(self) -> Dict[str, str]:
        """Return stream health metrics."""
        if self.process and self.process.poll() is None:
            self.health_metrics['status'] = 'running'
        else:
            self.health_metrics['status'] = 'stopped'
        return self.health_metrics