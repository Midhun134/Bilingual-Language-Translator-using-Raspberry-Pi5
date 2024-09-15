import speech_recognition as sr
from transformers import MarianMTModel, MarianTokenizer
from gtts import gTTS
import os
import pyaudio
import wave
from pydub import AudioSegment

# Initialize the recognizer
r = sr.Recognizer()

# Load translation models and tokenizers
en_to_ml_model_name = 'Helsinki-NLP/opus-mt-en-ml'
ml_to_en_model_name = 'Helsinki-NLP/opus-mt-ml-en'

en_to_ml_tokenizer = MarianTokenizer.from_pretrained(en_to_ml_model_name)
en_to_ml_model = MarianMTModel.from_pretrained(en_to_ml_model_name)

ml_to_en_tokenizer = MarianTokenizer.from_pretrained(ml_to_en_model_name)
ml_to_en_model = MarianMTModel.from_pretrained(ml_to_en_model_name)

def translate(text, tokenizer, model):
    translated = model.generate(**tokenizer(text, return_tensors="pt"))
    tgt_text = tokenizer.decode(translated[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
    return tgt_text

def play_audio(filename, device_index):
    chunk = 1024
    wf = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()

    # Open stream on the specified device index
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    output_device_index=device_index)

    data = wf.readframes(chunk)

    while data:
        stream.write(data)
        data = wf.readframes(chunk)

    stream.stop_stream()
    stream.close()
    p.terminate()

# Use the combined index
play_audio('your_audio_file.wav', 3)

def speak(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")
    
    # Convert MP3 to WAV
    sound = AudioSegment.from_mp3("output.mp3")
    sound.export("output.wav", format="wav")
    
    play_audio("output.wav")

def listen_and_translate(src_lang='en', tgt_lang='ml'):
    try:
        with sr.Microphone() as source:
            print(f"Speak something in {src_lang}...")
            audio = r.listen(source)

            print("Recognizing...")
            if src_lang == 'en':
                text = r.recognize_google(audio, language='en-US')
                translated_text = translate(text, en_to_ml_tokenizer, en_to_ml_model)
            else:
                text = r.recognize_google(audio, language='ml-IN')
                translated_text = translate(text, ml_to_en_tokenizer, ml_to_en_model)

            print(f"Original ({src_lang}): {text}")
            print(f"Translated ({tgt_lang}): {translated_text}")

            speak(translated_text, lang=tgt_lang)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    while True:
        print("\n1. English to Malayalam")
        print("2. Malayalam to English")
        choice = input("Choose the translation direction (1 or 2, q to quit): ")
        if choice == '1':
            listen_and_translate('en', 'ml')
        elif choice == '2':
            listen_and_translate('ml', 'en')
        elif choice.lower() == 'q':
            break
        else:
            print("Invalid choice. Please choose 1 or 2.")