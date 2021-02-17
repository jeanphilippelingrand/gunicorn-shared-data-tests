#!/bin/sh

gunicorn \
	-b 0.0.0.0:5000 \
	--reload \
	--worker-class gthread \
	--threads 10 \
	--access-logfile - \
	app:app
