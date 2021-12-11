import pandas as pd

from operator import itemgetter
from random import randint, seed
from math import log10
from csv import writer as csv_writer

SEED = 10
NUM_CURVES = 20
config = {
    'spoons': { # high value, first 5 min = 400; next = 250; next = 100
        'scale': 25,
        'y_min': 10,
        'y_max': 20,
        'd_min':  6,
        'd_max': 12
    },
    'forks': {  # low volatility, constant cost 60
        'scale':  5,
        'y_min': 20,
        'y_max': 30,
        'd_min':  1,
        'd_max':  4
    },
    'knives': { # medium value, common item, first 20 = 50, next 10 = 100, end = 200
        'scale':  2,
        'y_min': 40,
        'y_max': 90,
        'd_min':  5,
        'd_max': 10
    },
}

if __name__ == '__main__':
    seed(SEED)

    dfs = []

    for name, curve in config.items():
        scale, y_min, y_max, d_min, d_max = itemgetter('scale', 'y_min', 'y_max', 'd_min', 'd_max')(curve)

        assert type(y_min) == int
        assert type(y_max) == int
        assert type(d_min) == int
        assert type(d_max) == int
        assert y_min <= y_max
        assert d_min <= d_max

        # TODO: enforce lucky vs unlucky people
        curves = pd.DataFrame(columns=[name])
        for i in range(NUM_CURVES):
            y, d, ypad, dpad = randint(y_min, y_max) * scale,  randint(d_min, d_max) * scale, int(log10(y_max * scale)) + 1, int(log10(d_max * scale)) + 1
            curves = curves.append({name : f"P = {y:{ypad}} - {d:{dpad}}Q" }, ignore_index=True)

        curves['idx'] = curves.index
        dfs.append(curves)

    curves = pd.DataFrame()
    curves['idx'] = dfs[0].index
    for commodity in dfs:
        curves = pd.merge(curves, commodity, how='outer', on=['idx'])

    curves = curves.drop(columns='idx')

    with open('output.tsv', 'w+') as wf:
        writer = csv_writer(wf, delimiter='	')
        for name, row in curves.iterrows():
            writer.writerow(curves.columns)
            writer.writerow(row.array)
            writer.writerow([])
            # print(row.array[1:])
        # writer.writerow([])
