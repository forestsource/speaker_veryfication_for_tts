# Speaker Verification for making TTS Dataset

## Install

```
git clone https://github.com/forestsource/speaker_veryfication_for_tts.git
cd speaker_veryfication_for_tts
python -m venv venv
venv\Scripts\activate
# use lightning, no torch
pip install -r requirements.txt
```

## setup

We need audio files for Ground Truth.  
Audio files including various performances by the same person are preferable.
It would be good to create it by combining multiple audio files.

```
ffmpeg -i laugh.wav -i angry.wav -i sad.wav -filter_complex “concat=n=3:v=0:a=1” ground.wav
```

or

Store all the audio files you want to concatenate into the `concat` folder.

```
python concat.py
```

## Run

```
python verify.py

```

or

```
python verify.py --gt ground.wav -t inputs -o outputs
```

## Detail

| dir         | desc                                                                                               |
| ----------- | -------------------------------------------------------------------------------------------------- |
| concat      | It will use the files in this folder to create the GT file(`ground.wav`).                          |
| convert     | This folder will be created automatically by `concat.py`. `.wav` files.(sampling rate 16000, mono) |
| inputs      | Audio files you want to verify.                                                                    |
| outputs     | Audio files with a `True` result                                                                   |
| ground.wav  | Ground Truth audio file. You need to prepare it.(16000 sampling rate, mono)                        |
| results.csv | Results file.                                                                                      |
