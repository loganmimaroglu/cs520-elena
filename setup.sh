#!/bin/bash

echo "Checking for existing cs520-elena conda env"
conda init bash

if { conda env list | grep 'cs520-elena'; } >/dev/null 2>&1; then
  echo "Found existing cs520-elena conda env, activating"
  conda activate cs520-elena -q
  echo "Updating installed packages to match environment.yml file"
  conda env update --name cs520-elena --file environment.yml --prune -q
else
  echo "No existing cs520-elena conda env found, creating"
  conda env create -f environment.yml -q
  echo "Activating"
  conda activate cs520-elena -q
  exit
fi;

conda info --envs
echo "All set!"
