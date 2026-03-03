import json

from vosk import Model, KaldiRecognizer

model = Model("voice models/vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)


def create_audio_callback(q):
    def audio_callback(indata, frames, time, status):
        q.put(bytes(indata))
    return audio_callback


def process_speech_data(data):
    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        return result.get("text", "").lower()
