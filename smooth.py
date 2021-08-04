from sys import argv
from configparser import ConfigParser
import numpy as np
import pandas as pd


def smooth(input_file, numerator, denominator, output_file):
    df = pd.read_csv(input_file)
    df[numerator] = np.where(df[denominator] >= df[numerator], df[numerator], df[denominator])
    denominators, numerators = df[denominator].values.tolist(), df[numerator].values.tolist()
    cfg = ConfigParser()
    cfg.read('smooth.ini')
    a, b = float(cfg.get('COMMON','a')),float(cfg.get('COMMON','b'))
    print(a, b)
    df.loc[:, 'smooth_fraction'] = (df[numerator] + a) / (df[denominator] + b)
    df.to_csv(output_file, index=0)


def main():
    if len(argv) < 5:
        print('Invalid parameter， please enter the correct parameters')
        print('python smooth.py <Input> <a> <b> <Output>')
    input_file, numerator, denominator, output_file = argv[1], argv[2], argv[3], argv[4]
    smooth(input_file, numerator, denominator, output_file)


if __name__ == '__main__':
    main()
