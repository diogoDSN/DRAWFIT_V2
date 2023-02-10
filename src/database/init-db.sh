#!/bin/bash

psql -U $POSTGRES_USER -v drawfit_bot_pass=\'$BOT_PASSWORD\' -f /initial_database.sql
