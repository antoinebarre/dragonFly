import os

print(os.getcwd())

from flake8.api import legacy as flake8


style_guide = flake8.get_style_guide(ignore=['E24', 'W503'])
report = style_guide.check_files("dragonfly/__init__.py")