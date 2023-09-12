import speech_recognition as sr
import argparse


def convert_wav_to_text(wav_file, credentials_file, language_code="en-EN"):
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Load the audio file
    with sr.AudioFile(wav_file) as source:
        audio_data = recognizer.record(source)
        try:

            try:
                return recognizer.recognize_google_cloud(
                    audio_data,
                    credentials_json=credentials_file,
                    language=language_code
                )
            except sr.UnknownValueError:
                return "Google Cloud Speech could not understand audio"
            except sr.RequestError as e:
                return "Could not request results from Google Cloud Speech service; {0}".format(e)

        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results; {e}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('wavfile', help="WAV file")
    parser.add_argument(
        "--credentials", help="Path to credentials JSON file"
    )
    parser.add_argument(
        "--language", help="Language code for example en-EN"
    )
    args = parser.parse_args()

    result = convert_wav_to_text(args.wavfile, args.credentials, args.language)
    print(result, flush=True)
