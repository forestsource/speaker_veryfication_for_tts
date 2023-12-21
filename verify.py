import os
import pathlib
import argparse
import pprint
import csv
import shutil

import nemo.collections.asr as nemo_asr
from pydub import AudioSegment
from tqdm import tqdm

speaker_model = nemo_asr.models.EncDecSpeakerLabelModel.from_pretrained(
    model_name="titanet_large"
)


def convert(audio_file, convert_dir):
    audio = AudioSegment.from_file(audio_file)
    mono_audio = audio.set_channels(1)
    resampled_audio = mono_audio.set_frame_rate(16000)
    path = pathlib.Path(audio_file).with_suffix(".wav")
    path = pathlib.Path(convert_dir).joinpath(path.name)
    resampled_audio.export(path, format="wav")


def verify(ground, target):
    result = speaker_model.verify_speakers(ground, target)
    return result


def get_audio_files(dir_path, only_wav=False):
    audio_files = []
    for p in pathlib.Path(dir_path).iterdir():
        if only_wav:
            if p.suffix == ".wav":
                audio_files.append(p)
        else:
            audio_files.append(p)
    return audio_files


def convert_audio_files(audio_files, convert_dir="convert"):
    print("Converting audio files...")
    for audio_file in tqdm(audio_files):
        convert(audio_file, convert_dir)


def to_csv(results, output_file):
    with open(output_file, "w", newline="") as csvfile:
        fieldnames = ["file", "result"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in results:
            writer.writerow(data)


def move_original_file(target_file, original_files, output_dir):
    for original_file in original_files:
        if original_file.stem == target_file.stem:
            print(f"Moving {original_file.name} to {output_dir}")
            out_path = pathlib.Path(output_dir).joinpath(original_file.name)
            shutil.move(original_file, out_path)
            break


def clean_dirs(output_dir):
    shutil.rmtree(output_dir, ignore_errors=True)
    shutil.rmtree("convert", ignore_errors=True)
    shutil.rmtree("outputs", ignore_errors=True)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs("convert", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)


if __name__ == "__main__":
    ground_file = "ground.wav"
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--gt", type=str, help="ground truth audio file", default="ground.wav"
    )
    parser.add_argument(
        "--target_dir",
        "-t",
        type=str,
        help="target audio file directory",
        default="inputs",
    )
    parser.add_argument(
        "--output_dir", "-o", type=str, help="output directory", default="outputs"
    )
    args = parser.parse_args()

    clean_dirs(args.output_dir)

    audio_files = get_audio_files(args.target_dir)
    convert_audio_files(audio_files, "convert")
    wav_files = get_audio_files("convert", only_wav=True)
    results = []
    print(f"Verifying...")
    for file in tqdm(wav_files):
        r = verify(ground_file, file)
        results.append({"file": file, "result": r})
        if r:
            move_original_file(file, audio_files, args.output_dir)

    pprint.pprint(results)
    to_csv(results, "results.csv")
