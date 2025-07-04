#!/usr/bin/env bash

# Определите переменные для базы данных и файла скрипта
DATABASE_NAME=hexlet
SQL_FILE=init.sql

# Выполните psql без явного указания имени пользователя и пароля
psql -a -d $DATABASE_NAME -f $SQL_FILE