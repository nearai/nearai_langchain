#!/bin/sh
echo "This script will run:"
echo "\tpython3.11 -m venv .venv"
echo "\t. .venv/bin/activate"
echo "\tpython3 -m pip install --upgrade pip"
echo "\tpython3 -m pip install -e ."
read -p "Continue? (y/n) " -n 1 -r

if [[ $REPLY =~ ^[Yy]$ ]]
then
  python3.11 -m venv .venv
  . .venv/bin/activate
  python3 -m pip install --upgrade pip
  pip install poetry
  python3 -m pip install -e .
fi