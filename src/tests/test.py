import unittest
import os
import uuid
from processor import StreamProcessor
from api import app

class TestStreamProcessor(unittest.TestCase):

    def setUp(self):
        self.stream_id = str(uuid.uuid4())
        self.input_url = "sample_input_url"
        self.output_dir = os.path.join("test_output", self.stream_id)
        self.processor = StreamProcessor(self.stream_id, self.input_url, self.output_dir)

    def tearDown(self):
        if os.path.exists(self.output_dir):
            for file in os.listdir(self.output_dir):
                os.remove(os.path.join(self.output_dir, file))
            os.rmdir(self.output_dir)

    def test_start_stream(self):
        self.processor.start_stream()
        self.assertTrue(os.path.exists(self.output_dir))

    def test_monitor_health(self):
        self.processor.start_stream()
        metrics = self.processor.monitor_health()
        self.assertIn("status", metrics)

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_start_stream_endpoint(self):
        response = self.client.post('/stream/start', json={"input_url": "sample_input_url"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("stream_id", response.json)

    def test_get_stream_manifest(self):
        stream_id = str(uuid.uuid4())
        output_dir = os.path.join("output", stream_id)
        os.makedirs(output_dir)
        with open(os.path.join(output_dir, "720p.m3u8"), "w") as file:
            file.write("#EXTM3U\n#EXT-X-VERSION:3")

        response = self.client.get(f'/stream/{stream_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("manifest", response.json)

    def test_get_metrics(self):
        response = self.client.get('/metrics/nonexistent')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()