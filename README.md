# Elevation Navigation System

A Python-based implementation for elevation aware navigation.

Please see docs/build/index.html for complete documentation.

## Setup for Development

### Requirements

Miniconda or Anaconda

### Steps

Load conda environment
```shell
conda env create -f environment.yml
conda activate cs520-elena
# Or if it already exists
conda env update --prefix ./env --file environment.yml  --prune
```

Populate Google API secret
```shell
echo 'google_elevation_api_key=ASK_LOGAN_FOR_SECRET' > .env
```

Now you're all set

## Authors

Logan Mimaroglu  
Jiachang Situ  
Saiyyam Kochar  
Rishab Maheshwari

## Documentation

run `./document.sh` and then open docs/build/index.html in your web browser.

## Testing

run `python -m unittest test/backend_test.py`

## Backend Server

run `./run_server.sh`

## Front end

start a live server using such as with this [extension for vscode](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) and boom the front end is running

if you also start the backend the complete product will be functional
