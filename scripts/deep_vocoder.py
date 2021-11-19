'''Aim: find the best matching between the first frame of the driving video, and several others images.
How to use the script:
python choose_best_pose.py path_of_the_video path_of_image_folder path_of_predictor_file
'''


from synthesizer.inference import Synthesizer
from encoder import inference as encoder
from vocoder import inference as vocoder
import numpy as np
from pathlib import Path
import librosa
import soundfile as sf
import argparse
import sounddevice as sd
import os
import sys


os.environ['MKL_SERVICE_FORCE_INTEL'] = '1'

full_path = "/home/paulina/Desktop/exhibition-code/scripts"
encoder_weights = (str(Path(full_path).parents[0])+ "/encoder/saved_models/pretrained.pt")
vocoder_weights = (str(Path(full_path).parents[0])+ "/vocoder/saved_models/pretrained/pretrained.pt") 
syn_dir = (str(Path(full_path).parents[0])+ "/synthesizer/saved_models/pretrained/pretrained.pt")  
#myvoice = "/home/paulina/Desktop/visitors/2021-04-18_16-20-57/audio.wav"

encoder.load_model(encoder_weights)
synthesizer = Synthesizer(syn_dir)
vocoder.load_model(vocoder_weights)



def synth(text, input_audio, output_audio):
  
    preprocessed_wav = encoder.preprocess_wav(input_audio)
    original_wav, sampling_rate = librosa.load(input_audio)
    preprocessed_wav = encoder.preprocess_wav(original_wav, sampling_rate)
    embed = encoder.embed_utterance(preprocessed_wav)
    print("Synthesizing new audio...")

    specs = synthesizer.synthesize_spectrograms([text], [embed])
    generated_wav = vocoder.infer_waveform(specs[0])
    generated_wav = np.pad(
        generated_wav, (0, synthesizer.sample_rate), mode="constant")


    counter = 0
    filename =  output_audio + "/" + "deepfake{}.wav"
    while os.path.isfile(filename.format(counter)):
            counter += 1
    filename = filename.format(counter)
    print(generated_wav.dtype)
    sf.write(filename, generated_wav.astype(np.float32), synthesizer.sample_rate)

    print("\nSaved output as %s\n\n" % filename)

# Get full command-line arguments
full_cmd_arguments = sys.argv

# Keep all but the first
argument_list = full_cmd_arguments[1:]
print(argument_list)
synth(argument_list[0], argument_list[1], argument_list[2])

