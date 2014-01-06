#!/usr/bin/env bash
set -e

update-locale LANG=en_GB.UTF-8

# upgrade the system
apt-get -q update

# install some python libs
apt-get -qq -y --force-yes install git python-pip python-virtualenv screen byobu
apt-get -qq -y --force-yes build-dep python-imaging python-mysqldb

if [ ! -f /usr/local/bin/flaskrun ]; then

    echo "Building flaskrun script"
    echo "#!/bin/bash" > /usr/local/bin/flaskrun
    echo "set -e" >> /usr/local/bin/flaskrun
    echo "" >> /usr/local/bin/flaskrun
    echo "source /home/vagrant/venv/bin/activate" >> /usr/local/bin/flaskrun
    echo "python /vagrant/manage.py runserver -t 0.0.0.0 -p 8000" >> /usr/local/bin/flaskrun
    chmod a+x /usr/local/bin/flaskrun

fi

if [ ! -f /usr/local/bin/bashrun ]; then

    echo "Building bashrun script"
    echo "#!/bin/bash" > /usr/local/bin/bashrun
    echo "set -e" >> /usr/local/bin/bashrun
    echo "" >> /usr/local/bin/bashrun
    echo "cd /vagrant/" >> /usr/local/bin/bashrun
    echo "bash" >> /usr/local/bin/bashrun
    chmod a+x /usr/local/bin/bashrun

fi

echo "copying vagrantappsetup.sh in the VM"
tr -d '\015' </vagrant/vagrantappsetup.sh >/home/vagrant/vagrantappsetup.sh
echo "run setup"
sudo -H -u vagrant bash /home/vagrant/vagrantappsetup.sh
