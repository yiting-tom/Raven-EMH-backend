import boto3
import websocket
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


class RealTimeTranscriber:
    def __init__(self, region_name='us-west-2', language_code='en-US', sample_rate=16000, encoding='pcm', vocabulary_name=None):
        self.transcribe_client = boto3.client('transcribe', region_name=region_name)
        self.language_code = language_code
        self.sample_rate = sample_rate
        self.encoding = encoding
        self.vocabulary_name = vocabulary_name

    def start_transcription(self, audio_file_path):
        try:
            # Create a streaming transcription job
            response = self.transcribe_client.start_stream_transcription(
                LanguageCode=self.language_code,
                MediaSampleRateHertz=self.sample_rate,
                MediaEncoding=self.encoding,
                VocabularyName=self.vocabulary_name  # Optional
            )

            # Extract the WebSocket URL from the response
            websocket_url = response['TranscriptResultStream']['Url']

            # Connect to the WebSocket
            ws = websocket.create_connection(websocket_url)

            # Stream the audio data to the WebSocket connection.
            with open(audio_file_path, 'rb') as audio_file:
                while (chunk := audio_file.read(1024)):  # Read 1KB at a time
                    ws.send_binary(chunk)

            # Receive transcription results in real-time
            while True:
                response = ws.recv()
                print(response)  # Handle and display the transcription response as needed

        except NoCredentialsError:
            print("Credentials not available")

        except PartialCredentialsError:
            print("Incomplete credentials provided")