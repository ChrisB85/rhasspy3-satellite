.PHONY: config
config:
	./script/run bin/config_print.py

server-install:
	./script/setup_http_server
	./script/run ./config/programs/asr/google-asr/script/setup
	./script/run ./config/programs/tts/google-tts/script/setup
	./script/run ./config/programs/vad/silero/script/setup

server-start:
	./script/http_server --debug
