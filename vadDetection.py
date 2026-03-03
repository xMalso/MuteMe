import webrtcvad

def create_voice_detected(level):
    vad = webrtcvad.Vad(level)
    def voice_detected(data):
        try:
            return vad.is_speech(data, 16000)
        # except Exception as e:
        except:
            # print("VAD error:", e)
            return True
    return voice_detected