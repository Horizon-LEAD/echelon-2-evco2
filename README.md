# ECHELON-2-EVCO2

## Description

Translates the data retrieved from the Echelon model into the format accepted by the
[EVCO2] model.

## Installation

The `requirements.txt` and `Pipenv` files are provided for the setup of an environment where the module can be installed. The package includes a `setup.py` file and it can be therefore installed with a `pip install .` when we are at the same working directory as the `setup.py` file. For testing purposes, one can also install the package in editable mode `pip install -e .`.

After the install is completed, an executable `echelon-2-evco2` will be available to the user.

Furthermore, a `Dockerfile` is provided so that the user can package the model.

To build the image the following command must be issued from the project's root directory:
```
docker build -t echelon-2-evco2:latest .
```

## Usage
The executable's help message provides information on the parameters that are needed.
```

$ echelon-2-evco2 -h

usage: echelon-2-evco2 [-h] [-v] Echelon_Output_IN Vehicle_info_IN OUTDIR

Main module

positional arguments:
  Echelon_Output_IN  The Json output file from Echelon as input to the connector
  Vehicle_info_IN    Vehicle json containing information regarding vehicle type
  OUTDIR             The output directory

options:
  -h, --help         show this help message and exit
  -v, --verbosity    Increase output verbosity (default: 0)
```

If the package installation has been omitted, the model can of course also be run with
`python -m src.echelon2evco2.__main__ <args>`

### Examples
```
echelon-2-evco2 \
    sample-data/input/output-csv.csv \
    sample-data/input/vehicle_info.json \
    sample-data/output/
```

```
docker run --rm \
    -v ${PWD}/sample-data:/data \
    echelon-2-evco2:latest \
    /data/input/output-csv.csv \
    /data/input/vehicle_info.json \
    /data/output/
```



