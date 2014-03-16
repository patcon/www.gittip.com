#!/usr/bin/env bash

set -e

# Set login directory to root vagrant share
echo "cd /vagrant" > /etc/profile.d/login-directory.sh

# TODO: Pin apt-get packages to the same versions Heroku uses

# Install dependencies
echo 'deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main' > /etc/apt/sources.list.d/postgresql.list
wget -qO- https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
apt-get update
apt-get -y install make git build-essential python-software-properties postgresql-9.3 postgresql-contrib-9.3 libpq-dev python-dev

# Configure Postgres
sudo -u postgres psql -U postgres -qf /vagrant/create_db.sql
sudo -u postgres createuser --superuser root
sudo -u postgres createuser --superuser vagrant

cd /vagrant

# Warn if Windows newlines are detected and try to fix the problem
if grep --quiet --binary --binary-files=without-match $(printf '\r') README.md; then
    echo
    cat development/scripts/crlf-warning.txt
    echo

    echo 'Running "git config core.autocrlf false"'
    git config core.autocrlf false

    exit 1
fi

# Set up the environment, the database, and run Gittip
make env
sudo -u postgres make schema data

# Output helper text
cat <<EOF

Gittip installed! To run,
$ vagrant ssh --command "sudo -iu postgres make run"
EOF
