#!/bin/bash
export DJANGO_SETTINGS_MODULE="config.settings.production"
SCRIPT_PATH=$(dirname $(realpath $0))
pid_file=$SCRIPT_PATH"/tmp/note.pid"

source $SCRIPT_PATH/venv/bin/activate
uwsgi --stop $pid_file
$SCRIPT_PATH/venv/bin/python3 $SCRIPT_PATH/manage.py crontab remove
deactivate