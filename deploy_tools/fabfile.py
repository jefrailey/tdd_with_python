# Standard Library
import os
import random

# Third party
from fabric.contrib.files import (
    append,
    exists,
    sed,
)
from fabric.api import (
    env,
    local,
    run,
)

REPO_URL = os.getenv('REPO_URL')
# env.use_ssh_config = True


def deploy():
    site_folder = '/home/{env.user}/sites/{env.host}'.format(env=env)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    for folder in ('database', 'static', 'virtualenv', 'source'):
        absolute_path = site_folder + '/' + folder
        run('mkdir -p {absolute_path}'.format(absolute_path=absolute_path))


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd {source_folder} && git fetch'.format(
            source_folder=source_folder))
    else:
        run('git clone {REPO_URL} {source_folder}'.format(
            REPO_URL=REPO_URL,
            source_folder=source_folder))
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run('cd {source_folder} && git reset --hard {current_commit}'.format(
        source_folder=source_folder, current_commit=current_commit))


def _update_settings(source_folder, site_name):
    superlists_folder = source_folder + '/superlists'
    settings_path = superlists_folder + '/settings.py'
    sed(settings_path, 'DEBUG = True', 'DEBUG = False')
    sed(
        settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["{site_name}"]'.format(site_name=site_name)
    )
    secret_key_file = superlists_folder + '/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '{key}'".format(key=key))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    pip_path = virtualenv_folder + '/bin/pip'
    requirements_path = source_folder + '/requirements.txt'
    if not exists(pip_path):
        run('virtualenv --python=python3 {virtualenv_folder}'.format(
            virtualenv_folder=virtualenv_folder))
    run('{pip_path} install -r {requirements_path}'.format(
        pip_path=pip_path, requirements_path=requirements_path))


def _update_static_files(source_folder):
    _manage(source_folder, 'collectstatic')


def _update_database(source_folder):
    _manage(source_folder, 'migrate', options='--noinput')


def _manage(source_folder, command, options='--noinput'):
    python3 = '../virtualenv/bin/python3'
    run(
        'cd {source_folder} && {python3} manage.py {command} {options}'.format(
            source_folder=source_folder, python3=python3, command=command,
            options=options)
    )
