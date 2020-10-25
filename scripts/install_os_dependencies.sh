#!/usr/bin/env bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.8.6
#sudo apt-get install -y python-psycopg2 postgresql libncurses5-dev libffi libffi-devel libxml2-devel libxslt-devel libxslt1-dev
#sudo apt-get install -y postgresql-libs postgresql-devel python-lxml python-devel gcc patch python-setuptools
#sudo apt-get install -y gcc-c++ flex epel-release nginx supervisor
#/etc/init.d/nginx stop