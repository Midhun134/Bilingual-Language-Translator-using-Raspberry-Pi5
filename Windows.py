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

def play_audio(filename):
    # Play audio file through both headset and external speaker
    chunk = 1024
    wf = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()

    # Get the list of available audio devices
    def get_device_info():
        info = p.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        devices = []
        for i in range(num_devices):
            device = p.get_device_info_by_host_api_device_index(0, i)
            devices.append((i, device['name']))
        return devices

    devices = get_device_info()
    print("Available audio devices:")
    for idx, name in devices:
        print(f"{idx}: {name}")

    # Ensure the device indices are correct
    headset_index = 6  # Adjust this to your actual headset index
    speaker_index = 4  # Adjust this to your actual speaker index

    if headset_index >= len(devices) or speaker_index >= len(devices):
        print("Invalid device index")
        return

    # Open stream for headset
    try:
        stream_headset = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                                channels=wf.getnchannels(),
                                rate=wf.getframerate(),
                                output=True,
                                output_device_index=headset_index)
    except Exception as e:
        print(f"Failed to open headset stream: {e}")
        return

    # Open stream for external speaker
    try:
        stream_speaker = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                                channels=wf.getnchannels(),
                                rate=wf.getframerate(),
                                output=True,
                                output_device_index=speaker_index)
    except Exception as e:
        print(f"Failed to open speaker stream: {e}")
        stream_headset.close()
        return

    # Read data in chunks and play
    data = wf.readframes(chunk)
    while data:
        stream_headset.write(data)
        stream_speaker.write(data)
        data = wf.readframes(chunk)
    # Stop and close streams
    stream_headset.stop_stream()
    stream_headset.close()
    stream_speaker.stop_stream()
    stream_speaker.close()
    # Terminate PyAudio
    p.terminate()

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