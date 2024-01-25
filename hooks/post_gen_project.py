#!/usr/bin/env python
import json
import os
import shutil
import subprocess

from pathlib import Path

import requests

LICENSES_DICT = {
    "Proprietary": None,
    "Apache-2.0": "Apache-2.0",
    "MIT": "MIT",
    "BSD-4-Clause": "BSD-4-Clause",
    "BSD-3-Clause": "BSD-3-Clause",
    "BSD-2-Clause": "BSD-2-Clause",
    "GPL-2.0-only": "GPL-2.0",
    "GPL-2.0-or-later": "GPL-2.0",
    "GPL-3.0-only": "GPL-3.0",
    "GPL-3.0-or-later": "GPL-3.0",
    "LGPL-2.1-only": "LGPL-2.1",
    "LGPL-2.1-or-later": "LGPL-2.1",
    "LGPL-3.0-only": "LGPL-3.0",
    "LGPL-3.0-or-later": "LGPL-3.0",
    "ISC": "ISC",
}

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

username = '{{ cookiecutter.author_name }}' if '{{ cookiecutter.author_name }}' else os.popen('git config user.name').read().strip()
email = '{{ cookiecutter.author_email }}' if '{{ cookiecutter.author_email }}' else os.popen('git config user.email').read().strip()


def download_license_from_github(license_name):
    """Download the license file from GitHub"""
    license_name = LICENSES_DICT[license_name]
    if license_name:
        url = 'https://api.github.com/licenses/{}'.format(license_name)
        response = requests.get(url)
        if response.status_code == 200:
            license_content = json.loads(response.content.decode('utf-8'))['body']
            return license_content
    return None


def format_license(license_content):
    """Format the license file"""
    license_content = license_content.replace("[year]", "{% now 'local', '%Y' %}")
    license_content = license_content.replace("[fullname]", username)
    license_content = license_content.replace("[email]", email)
    license_content = license_content.replace("[project]", "{{ cookiecutter.project_name }}")

    # GPL 3-Clause License
    license_content = license_content.replace("<year>", "{% now 'local', '%Y' %}")
    license_content = license_content.replace("<name of author>", username)
    license_content = license_content.replace(
        "<one line to give the program's name and a brief idea of what it does.>",
        "{{ cookiecutter.project_short_description }}"
    )

    return license_content


def write_license_file(license_name):
    """Write the license file to the project directory"""
    license_content = download_license_from_github(license_name)
    if license_content:
        with open(os.path.join(PROJECT_DIRECTORY, 'LICENSE'), 'w') as f:
            f.write(license_content)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def poetry_update():
    os.system("poetry update")


def modify_pyproject_toml():
    with open(os.path.join(PROJECT_DIRECTORY, 'pyproject.toml'), 'r') as f:
        content = f.read()

    content = content.replace('authors = []', 'authors = ["{} <{}>"]'.format(username, email))

    with open('pyproject.toml', 'w') as f:
        f.write(content)


def init_repo():
    subprocess.run(["poetry", "install", "-n"])
    subprocess.run(["poetry", "update"])
    subprocess.run(["poetry", "run", "pre-commit", "install"])
    subprocess.run(["poetry", "run", "pre-commit", "run", "-a"])


if __name__ == '__main__':
    if "{{ cookiecutter.open_source_license }}" != "Proprietary(Not Open Source)":
        write_license_file("{{ cookiecutter.open_source_license }}")

    modify_pyproject_toml()

    # init_repo()
