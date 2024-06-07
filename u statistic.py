import pandas as pd
from functools import reduce

real = pd.read_csv('real_data.csv', sep=';')
df = pd.read_csv('forecast.csv', sep=';')
df.set_index('time', inplace=True)
real.set_index('time', inplace=True)

real = real[df.iloc[0].name:df.iloc[-1].name]


def U_statistics(listf, listy):
    e = (sum((y - x) ** 2 for y, x in zip(listy, listf)) / len(listf))** 0.5
    f = (reduce(lambda x, y: x + y ** 2, listf) / len(listf)) ** 0.5
    y = (reduce(lambda x, y: x + y ** 2, listy) / len(listy)) ** 0.5


    return e / (y + f)


# for name, values in df.items():
# print(sum(list(map(lambda x: x ** 2, values))))


for column in df.columns:
    print(column, U_statistics(df[column].tolist(), real[column].tolist()))
