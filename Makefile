SHELL := /usr/bin/env bash

all:
	echo "please make love"

install:
	pip install -r requirements.txt
db:
	python manage.py syncdb
run: love
web: love
love: love_zhy
love_zhy:
	python manage.py runserver 0.0.0.0:8964
love_syc:
	python manage.py runserver 0.0.0.0:8965
love_jly:
	python manage.py runserver 0.0.0.0:8966
love_zs:
	python manage.py runserver 0.0.0.0:8967

.PHONY : install love all run web

