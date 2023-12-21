import os
import pathlib

from pydub import AudioSegment
from tqdm import tqdm


def convert(audio_file):
    audio = AudioSegment.from_file(audio_file)
    mono_audio = audio.set_channels(1)
    resampled_audio = mono_audio.set_frame_rate(16000)
    path = pathlib.Path(audio_file).with_suffix(".wav")
    resampled_audio.export(path, format="wav")


def convert_audio_files(dir_path):
    audio_files = []
    for p in pathlib.Path(dir_path).iterdir():
        audio_files.append(p)
    print("Converting audio files...")
    for audio_file in tqdm(audio_files):
        convert(audio_file)


def concat_audio_files(directory):
    audio_files = [f for f in os.listdir(directory) if f.endswith(".wav")]
    combined_audio = AudioSegment.empty()
    for audio_file in audio_files:
        audio = AudioSegment.from_wav(os.path.join(directory, audio_file))
        combined_audio += audio
    combined_audio.set_channels(1)
    combined_audio.set_frame_rate(16000)
    combined_audio.export("ground.wav", format="wav")


convert_audio_files("concat")
concat_audio_files("concat")
