#!/bin/sh

export $(cat /.env | xargs)

exec "$@"