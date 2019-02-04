# Maturity Review Automation Tools

## Motivation
This is a PoC tool for generating Maturity Review charts / data

Before this tool existed a manual process was undertaken after every maturity review. This PoC is a direct representation of that manual process.

## Tool Chain
- python3
- pip3
- virtualenv
- Docker

## Running locally

**It is reccomended that you use pythons `virtualenv` to avoid breaking globally installed packages**

1. Setup virtualenv
```bash
pip3 install virtualenv
virtualenv venv && source venv/bin/activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
python application.py
```

This will start a locally running instane of the app at `http://localhost` -> note this has not been tested on Windows.

## Running inside the docker container locally

This is as simple as building the docker image locally and running it:

```bash
docker build -t maturity-review-tool .
docker run -p 80:80 -n maturity-review-tool maturity-review-tool:latest
```

This will start the docker container and bind it to your local port 80, making the instance accesible at `http://localhost`. If you environment does not allow for binding on port 80 then adjust the local port in the docker run command: `-p 8080:80` this example will allow you to access at `http://localhost:8080`

## Testing

Some very awful tests do exist for the data logic but they are only happy path tests. These can be found in `./test_data_handler.py` They can be run as:

```bash
python -m unittest
```
