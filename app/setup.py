from setuptools import setup, find_packages
import os, sys

# read requirements from requirements.txt file
with open(os.path.join(os.path.dirname(__file__), 'requirements.txt'), 'r') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

# read version from VERSION file
with open(os.path.join(os.path.dirname(__file__), '../VERSION'), 'r') as f:
    version = f.read().strip()

APP_NAME = "pirag"

setup(
    name = APP_NAME,
    version = version,
    packages = ["app", "app.rag", "rag"],
    package_dir = {"app": ".", "rag": "rag"},
    include_package_data = True,
    install_requires = requirements,
    entry_points = {
        "console_scripts": [
            f"{APP_NAME}=app.main:main",
        ],
    },
)
