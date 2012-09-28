SHELL := /usr/bin/env bash

all:
	echo "please make love"

install:
	pip install -r requirements.txt

run: love
web: love
love:
	python manage.py runserver 0.0.0.0:8964

.PHONY : install love all run web

