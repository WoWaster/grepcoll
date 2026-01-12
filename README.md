# GrepColl

GrepColl: grep, but with recoll underneath, usefull to search with stemming and lemmatization

## Installation

Recoll and python bindings must be installed in the system.

```bash
sudo apt-get install recoll python3-recoll # Ubuntu
sudo pacman -S recoll                      # Arch
```

After that, you need to clone this repository and install all the dependencies.

```bash
git clone git@github.com:WoWaster/grepcoll.git
cd grepcoll
uv sync
```

## Usage

```bash
uv run grepcoll <pattern> <path/to/dir>
```

By default `<path>` is the root of the project.

## Credits

This package was created with [Cookiecutter](https://github.com/audreyfeldroy/cookiecutter) and the [audreyfeldroy/cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) project template.
