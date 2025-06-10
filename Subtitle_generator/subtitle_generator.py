import gradio as gr
from vosk import Model, KaldiRecognizer
import wave
import json
from translate import Translator


# Load Vosk model once
vosk_model = Model(
    r"C:\Gradio projects\Subtitle_generator\models\vosk-model-small-cn-0.22"
)  # put your Simplified Chinese Vosk model folder path here


def transcribe_with_vosk(audio_filepath):
    wf = wave.open(audio_filepath, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        raise ValueError("Audio file must be WAV format mono PCM.")
    rec = KaldiRecognizer(vosk_model, wf.getframerate())
    results = []

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            results.append(res.get("text", ""))
    # get final partial result
    res = json.loads(rec.FinalResult())
    results.append(res.get("text", ""))

    text = " ".join(results).strip()
    return text


def translate_chinese_to_english(ch_text):
    translator = Translator(from_lang="zh", to_lang="en")
    en_text = translator.translate(ch_text)
    return en_text


def voice_to_text_translate(audio_file):
    # Step 1: Transcribe Chinese speech to text
    try:
        chinese_text = transcribe_with_vosk(audio_file)
        if not chinese_text:
            return "No speech recognized.", ""
    except Exception as e:
        return f"Transcription error: {str(e)}", ""

    # Step 2: Translate Chinese text to English
    try:
        english_text = translate_chinese_to_english(chinese_text)
    except Exception as e:
        return f"Translation error: {str(e)}", ""

    return chinese_text, english_text


audio_input = gr.Audio(source="microphone", type="filepath")

demo = gr.Interface(
    fn=voice_to_text_translate,
    inputs=audio_input,
    outputs=[
        gr.Textbox(label="Chinese Transcription"),
        gr.Textbox(label="English Translation"),
    ],
)

if __name__ == "__main__":
    demo.launch()
