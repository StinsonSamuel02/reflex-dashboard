#!/usr/bin/env bash
# Exit on error
set -o errexit

/root/.local/bin/poetry run gunicorn --workers 3 --bind unix:/home/orgsi-web-app/core.sock core.wsgi:application
