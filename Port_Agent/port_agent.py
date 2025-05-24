import os
import json
import re
import subprocess
from typing import Dict, Optional
import speech_recognition as sr
from pydub import AudioSegment


class PortAgent:
    SUPPORTED_FORMATS = ['.wav', '.aiff', '.aifc', '.flac']
    KNOWN_SHIP_NAMES = [
        "94W4F32", "57K9M18", "83T2X67", "61R8L94", "46Y5N23",
        "78C3Z10", "29B6Q81", "90V7J55", "63H1S42", "35D4K76", "88P9E29"
    ]

    def __init__(self, model_name: str = "llama3.2:1b"):
        self.model_name = model_name

    def check_ffmpeg(self) -> bool:
        try:
            subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True)
            subprocess.run(["ffprobe", "-version"], check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def validate_and_convert_audio(self, audio_file: str) -> Optional[str]:
        if not self.check_ffmpeg() or not os.path.exists(audio_file):
            return None

        file_ext = os.path.splitext(audio_file)[1].lower()
        if file_ext not in self.SUPPORTED_FORMATS:
            try:
                audio = AudioSegment.from_file(audio_file)
                new_file = os.path.splitext(audio_file)[0] + "_converted.wav"
                audio.export(new_file, format="wav")
                return new_file
            except Exception:
                return None
        return audio_file

    def transcribe_audio(self, audio_file: str) -> Optional[str]:
        recognizer = sr.Recognizer()
        validated_audio = self.validate_and_convert_audio(audio_file)
        if not validated_audio:
            return None

        try:
            with sr.AudioFile(validated_audio) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio)
                return text.lower()
        except (sr.UnknownValueError, sr.RequestError, ValueError, Exception):
            return None
        finally:
            if validated_audio != audio_file and os.path.exists(validated_audio):
                os.remove(validated_audio)

    def extract_data(self, transcript: str) -> Dict[str, str]:
        prompt = f"""
Extract structured information in JSON format from the following transcript.

Fields to extract:
- ship_name (must match exactly from the list)
- reach_time (in time format)
- containers_unloaded (number)
- company_name (organization name)

Known ship names: {', '.join(self.KNOWN_SHIP_NAMES)}
Transcript:
\"\"\"{transcript}\"\"\"

Return a JSON object with those fields only.
"""
        try:
            result = subprocess.run(
                ["ollama", "run", self.model_name],
                input=prompt,
                capture_output=True,
                text=True
            )
            output = result.stdout.strip()
            json_match = re.search(r'\{.*\}', output, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception as e:
            print("Error during extraction:", e)

        return {
            "ship_name": "",
            "reach_time": "",
            "containers_unloaded": "",
            "company_name": "",
        }

    def save_output(self, data: Dict[str, str], output_file: str):
        try:
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print("Failed to save data:", e)

    def run(self, audio_file: str, output_file: str) -> Dict[str, str]:
        print("Processing audio...")
        text = self.transcribe_audio(audio_file)
        print('text--',text)
        if text:
            print("Transcription done. Extracting data...")
            data = self.extract_data(text)
            print('data',data)
            self.save_output(data, output_file)
            print("Extraction complete.")
            return data
        else:
            print("No transcription available.")
            return {}


if __name__ == "__main__":
    agent = PortAgent()
    result = agent.run("datasets/ElevenLabs_Text_to_Speech_audio.mp3", "extracted_data.json")
    print("Final Result:", result)
