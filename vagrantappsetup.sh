#!/usr/bin/env bash
set -e

# getting dotfiles
if [ ! -d /home/vagrant/dotfiles ]; then
    git clone https://github.com/paddycarey/dotfiles.git
    cd dotfiles
    ./dotfiles.sh
    cd ..
fi

# build the virtualenv
if [ ! -d /home/vagrant/venv ]; then
    echo "Building virtualenv"
    virtualenv /home/vagrant/venv
    source /home/vagrant/venv/bin/activate; easy_install -U distribute
fi

# install our app's requirements
source /home/vagrant/venv/bin/activate; pip install -r /vagrant/requirements.txt

if [ ! -d /home/vagrant/.byobu ]; then
    echo "Building byobu config"
    mkdir /home/vagrant/.byobu
    echo "BYOBU_BACKEND=screen" > /home/vagrant/.byobu/backend
fi

echo "Launching byobu session"
byobu-launcher-install
