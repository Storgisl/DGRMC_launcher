#!/bin/bash

pyinstaller --onefile \
--distpath "$PWD" \
launcher.py
