
from synthesizer.inference import Synthesizer
from encoder import inference as encoder
from vocoder import inference as vocoder
from pathlib import Path
import numpy as np
import librosa
import soundfile as sf
import argparse
import sounddevice as sd
import os



encoder_weights = Path("encoder/saved_models/pretrained.pt")
vocoder_weights = Path("vocoder/saved_models/pretrained/pretrained.pt")
syn_dir = Path("synthesizer/saved_models/pretrained/pretrained.pt")

myvoice  = "/home/paulina/Desktop/visitors/test/enhancedAudio.mp3"
encoder.load_model(encoder_weights)
synthesizer = Synthesizer(syn_dir)
vocoder.load_model(vocoder_weights)



def synth():
    
    text = "What are you still doing here? It's over.      You can leave now." # @param {type:"string"}

    preprocessed_wav = encoder.preprocess_wav(myvoice)
    original_wav, sampling_rate = librosa.load(myvoice)
    preprocessed_wav = encoder.preprocess_wav(original_wav, sampling_rate)
    embed = encoder.embed_utterance(preprocessed_wav)
    print("Synthesizing new audio...")

    specs = synthesizer.synthesize_spectrograms([text], [embed])
    generated_wav = vocoder.infer_waveform(specs[0])
    generated_wav = np.pad(
        generated_wav, (0, synthesizer.sample_rate), mode="constant")


    counter = 0
    desktop = "/home/paulina/Desktop/"
    filename = desktop + "demo_output_{}.wav"
    while os.path.isfile(filename.format(counter)):
            counter += 1
    filename = filename.format(counter)
    print(generated_wav.dtype)
    sf.write(filename, generated_wav.astype(np.float32), synthesizer.sample_rate)

    print("\nSaved output as %s\n\n" % filename)


synth()
