import gradio as gr


from vosk import Model

model_path = r"C:\Python projects\models\vosk-model-small-cn-0.22"

try:
    model = Model(model_path)
    print("Vosk model loaded successfully.")
except Exception as e:
    print(f"Error loading Vosk model: {e}")
