"""Main module
"""

import logging
from os.path import isfile, isdir
import pandas as pd
import numpy as np
from sys import argv
from os.path import join
from argparse import (ArgumentParser, RawTextHelpFormatter,
                      ArgumentDefaultsHelpFormatter, ArgumentTypeError)

LOG_FILE_MAX_BYTES = 50e6
LOG_MSG_FMT = "%(asctime)s %(levelname)-8s %(name)s \
%(filename)s#L%(lineno)d %(message)s"
LOG_DT_FMT = "%Y-%m-%d %H:%M:%S"

DESC = '''
Echelon to EVCO2 Connector
'''

logger = logging.getLogger("echelon_evco2_connector")

class RawDefaultsHelpFormatter(ArgumentDefaultsHelpFormatter, RawTextHelpFormatter):
    """Argparse formatter class"""


def strfile(path):
    """Argparse type checking method
    string path for file should exist"""
    if isfile(path):
        return path
    raise ArgumentTypeError("Input file does not exist")


def strdir(path):
    """Argparse type checking method
    string path for file should exist"""
    if isdir(path):
        return path
    raise ArgumentTypeError("Input directory does not exist")


def main():
    """ echelon2copert interface main
    """
    parser = ArgumentParser(description=DESC,
                            formatter_class=RawDefaultsHelpFormatter)

    parser.add_argument('-v', '--verbosity', action='count',
                        default=0, help='Increase output verbosity')
    parser.add_argument('Echelon_Output_IN', type=strfile, default=None,
                        help='The csv output file from Echelon as input to the connector')
    parser.add_argument('Vehicle_info_IN', type=strfile, default=None,
                        help='Vehicle json file containing information regarding vehicle')

    parser.add_argument('OUTDIR', type=strdir, help='The output directory')

    args = parser.parse_args(argv[1:])

    df_echelon = pd.read_csv(args.Echelon_Output_IN, sep=';')
    df_echelon = df_echelon[['totalDistance', 'numberOfVehicles']].iloc[:1]
    df_vehicle_info = pd.read_json(args.Vehicle_info_IN).iloc[:1]
    df = pd.concat([df_echelon, df_vehicle_info], axis=1)
    df.rename(columns = {'totalDistance':'MeanActivity', 'numberOfVehicles':'Stock'}, inplace = True)
    df['ResponsePlanId'] = np.random.randint(1, 1000, df.shape[0])
    df['energykwh'] = df.apply(lambda row: (row.VehicleConsumption/100) * row.MeanActivity, axis = 1)
    df['energyTJ'] = df.apply(lambda row: row.energykwh * 3.6 * 1e-6, axis = 1)
    df.drop('VehicleConsumption', axis=1, inplace=True)
    df.to_excel(join(args.OUTDIR, "energy_consumption.xlsx"), index=False)


if __name__ == '__main__':
    main()
