Provisioning a new site
=======================

## Required packages:

- nginx
- Python 3
- Git
- pip
- virtualenv

e.g., on Ubuntu:

    sudo apt-get install nginx git python3 python3-pip
    sudo pip3 install virtualenv

## Nginx Virtual Host config

 - See `nginx.template.conf`
 - Replace `SITENAME` with, e.g., `staging.my-domain.com`

## Upstart Job

 - See `gunicorn-upstart.template.conf`
 - Replace `SITENAME` with, e.g., `staging.my-domain.com`

## Folder structure:

Assume we have a user account at `/home/username`

    /home/username
    |__ sites
        |__ SITENAME
            |-- database
            |-- source
            |-- static
            |__ virtualenv