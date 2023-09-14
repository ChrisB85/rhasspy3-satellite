#!/usr/bin/env python3
import argparse
import logging
import os
import shutil
from pydub import AudioSegment
import hashlib
import sys
from gtts import gTTS
from pathlib import Path

_FILE = Path(__file__)
_DIR = _FILE.parent
_LOGGER = logging.getLogger(_FILE.stem)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", help="Output directory", default="./")
    parser.add_argument("--language", help="Language code")
    parser.add_argument("--text", help="Text to convert", required=False)
    parser.add_argument(
        "--debug", action="store_true", help="Print DEBUG messages to console"
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    if args.text:
        text = args.text
    else:
        text = sys.stdin.read()

    dir = args.dir
    if not dir.endswith("/"):
        dir += "/"

    filename = dir + sha1_string(text)
    mp3_file_name = filename + ".mp3"
    wav_file_name = filename + ".wav"

    if os.path.exists(wav_file_name):
        _LOGGER.info("File exists in cache: " + wav_file_name)
        play_file(wav_file_name)
        return

    tts = gTTS(text=text, lang='pl')
    tts.save(mp3_file_name)
    mp3_to_wav(mp3_file_name, wav_file_name)
    os.unlink(mp3_file_name)
    play_file(wav_file_name)


def sha1_string(input_string):
    # Create a new SHA-1 hash object
    sha1_hash = hashlib.sha1()

    # Update the hash object with the bytes of the input string
    sha1_hash.update(input_string.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    sha1_hex = sha1_hash.hexdigest()

    return sha1_hex


def mp3_to_wav(input_mp3_file, output_wav_file):
    try:
        if not input_mp3_file.endswith(".mp3"):
            input_mp3_file += ".wav"
        if not output_wav_file.endswith(".wav"):
            output_wav_file += ".wav"

        sound = AudioSegment.from_mp3(input_mp3_file)
        sound.export(output_wav_file, format="wav")
    except Exception as e:
        print(f"Error during conversion: {e}")

def play_file(wav_file_name):
    with open(wav_file_name, 'rb') as wav:
        shutil.copyfileobj(wav, sys.stdout.buffer)


if __name__ == "__main__":
    main()
