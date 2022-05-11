# DRAWFIT_V2
Upgraded DRAWFIT robot using HTTP requests

Still developing the backbone, don't judge


## Virtual Environment [recomended]

Create a virtual environment the first time running the project.
Use this command in the project's root directory:

```
python3 -m venv .venv
```

To enter the created virtual environment use command:

```
source .venv/bin/activate
```

Next install the project's dependencies you need with:

```
pip -r install Requirements.txt
or
pip -r install DevRequirements.txt
```



## Running

To run the bot just use the command in the project's root directory:

```
python src/main/Drawfit.py
```

## Unit Tests

To run the full unit test package use the following command in the project's root directory:

```
pytest --rootdir=src/test
```