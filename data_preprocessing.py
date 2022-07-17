import pandas as pd
import numpy as np
from functools import reduce

from scipy.signal import argrelextrema
from sklearn.preprocessing import normalize
from sklearn.linear_model import LinearRegression


def max_diff_with_val(lst, mean):
    mx = 0
    for item in lst:
        mx = max(mx, abs(item - mean))
    return mx


def max_diff(lst):
    max_diff = 0
    for x, y in zip(lst[0::], lst[1::]):
        max_diff = max(max_diff, abs(y - x))
    return max_diff


def freq(x):
    return len(argrelextrema(np.array(x), np.less)[0]) / 12 * 60


def calc_coef_angle(y):
    X = np.linspace(0, 240, 240)
    X = X.reshape(-1, 1)

    try:
        return LinearRegression().fit(X, y).coef_[0]
    except:
        return 0


def average(lst):
    return reduce(lambda a, b: a + b, lst) / len(lst)


def preprocess(data):
    # Кодирование идентификатора порядковым номером
    data['Filename'] = data['Filename'].astype('category')
    data['Filename'] = data['Filename'].cat.codes

    # Преобразуем строки данных в списки
    data['Data'] = data['Data'].apply(eval)
    data['Data_2'] = data['Data_2'].apply(eval)

    # Выведем длины списков в отдельные столбцы
    data['len'] = data['Data'].apply(len)
    data['len2'] = data['Data_2'].apply(len)

    # Удалим поврежденные/неполные данных
    data = data.dropna()
    data = data[(data.len != 0) & (data.len2 != 0)]

    # Нормализация
    data['Data'] = data['Data'].apply(lambda data: [x for xs in normalize([np.array(data)]) for x in xs])
    data['Data_2'] = data['Data_2'].apply(lambda data: [x for xs in normalize([np.array(data)]) for x in xs])

    # Найдем стандартное отклонение
    data.insert(5, 'Data_STD', data.apply(lambda row: np.std(row.Data), axis=1))
    data.insert(7, 'Data_2_STD', data.apply(lambda row: np.std(row.Data_2), axis=1))

    # Cреднее значение показателей человека на протяжении всего исследования
    concat_lists = data.groupby(['Filename', 'Presentation']).agg({'Data': 'sum', 'Data_2': 'sum'})
    concat_lists.insert(1, 'Mean', concat_lists['Data'].apply(lambda x: average(x)))
    concat_lists.insert(3, 'Mean_2', concat_lists['Data_2'].apply(lambda x: average(x)))
    concat_lists = concat_lists.drop('Data', axis=1)
    concat_lists = concat_lists.drop('Data_2', axis=1)

    data = pd.merge(left=data, left_on=['Filename', 'Presentation'],
                    right=concat_lists, right_on=['Filename', 'Presentation'],
                    how='inner')

    # Расчет линии тренда
    data['Angle'] = data.Data.apply(calc_coef_angle)
    data['Angle_2'] = data.Data_2.apply(calc_coef_angle)

    # Добавим частоту колебаний
    data['Freq'] = data.Data.apply(freq)
    data = data[(data.Freq > 50) & (data.Freq < 220)]

    # Приблизительный расчет амплитуды
    data.insert(5, 'Amplitude', data['Data'].apply(max_diff))
    data.insert(8, 'Amplitude_2', data['Data_2'].apply(max_diff))

    # Удалим длины списков с датчиков, они нам больше не понадобятся
    data = data.drop('len', axis=1)
    data = data.drop('len2', axis=1)

    # Максимум производной
    data['Data_max_grad'] = data['Data'].apply(lambda x: max(np.abs(np.gradient(x))))
    data['Data_2_max_grad'] = data['Data'].apply(lambda x: max(np.abs(np.gradient(x))))

    # Отклонение от нормы повторения
    data.insert(8, 'Diff', data.apply(lambda row: max_diff_with_val(row.Data, row.Mean), axis=1))
    data.insert(8, 'Diff_2', data.apply(lambda row: max_diff_with_val(row.Data_2, row.Mean_2), axis=1))

    features = [
        'Test_index',
        'Presentation',
        'Question',
        'Amplitude',
        'Data_STD',
        'Amplitude_2',
        'Data_2_STD',
        'Mean',
        'Mean_2',
        'Angle',
        'Angle_2',
        'Freq',
        'Data_max_grad',
        'Data_2_max_grad'
    ]

    return data[features]
