#!/bin/bash
set -ex
if [[ "$DATABASE_ENGINE" == django\.db\.backends\.mysql ]]; then
  mysql -e 'create database test_db;' -u root

  if [[ "$TRAVIS_PYTHON_VERSION" == 2\.7 ]]; then
    echo MySQL-python >> db_requirements.txt
  fi
  if [[ "$TRAVIS_PYTHON_VERSION" == 2\.6 ]]; then
    echo MySQL-python >> db_requirements.txt
  fi
fi

if [[ "$DATABASE_ENGINE" == django\.db\.backends\.postgresql_psycopg2 ]]; then
  psql -c 'create database test_db;' -U postgres
  echo psycopg2 >> db_requirements.txt
fi
