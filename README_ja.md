# TTS のデータセット作成のための話者識別

## インストール

```
git clone https://github.com/forestsource/speaker_veryfication_for_tts.git
cd speaker_veryfication_for_tts
python -m venv venv
venv\Scripts\activate
# use lightning, no torch
pip install -r requirements.txt
```

## 準備

元の話者のファイルが必要です。
同一人物による様々な演技が含まれているオーディオファイルが好ましいです。
複数のオーディオファイルを結合するとよいでしょう。

```
ffmpeg -i laugh.wav -i angry.wav -i sad.wav -filter_complex “concat=n=3:v=0:a=1” ground.wav
```

or

`concat`フォルダに結合したいオーディオファイルをすべて保存する。

```
python concat.py
```

## 実行

```
python verify.py

```

or

```
python verify.py --gt ground.wav -t inputs -o outputs
```

## Detail

| dir         | desc                                                                                  |
| ----------- | ------------------------------------------------------------------------------------- |
| concat      | このフォルダ内のファイルを使用して `ground.wav` ファイルを作成します。                |
| convert     | `concat.py`によって自動的に作られます。 `.wav` files.(sampling rate 16000, mono)      |
| inputs      | 話者認識にかけたいオーディオファイル                                                  |
| outputs     | 結果が`True`のオーディオファイル。                                                    |
| ground.wav  | Ground Truth オーディオファイル。 準備する必要があります。(16000 sampling rate, mono) |
| results.csv | 結果のファイル                                                                        |
