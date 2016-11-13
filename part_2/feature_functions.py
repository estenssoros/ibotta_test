from __future__ import division
import re


def translate_data(data):
    if data == 'gap':
        return 0
    if 'session' in data:
        return data
    if 'engage' in data:
        return 1
    if 'verify' in data:
        return 2


def fix_columns(df):
    dont_fix = ['start_day', 'future_redemptions', 'customer_id']
    print 'fixing columns...'
    for col in df.columns:
        print '   {0}'.format(col)
        if col not in dont_fix:
            df[col] = df.apply(lambda x: translate_data(x[col]), axis=1)
    return df


def days_since_last(row):
    days_since = 0
    row = row[row.index.str.contains('day')]
    row = row.values.tolist()[1:]
    for day in row:
        if day == 0:
            days_since += 1
        else:
            days_since = 0
    return days_since


def engagement_ratio(row):
    return len(row[row.values == 1]) / len(row)


def verify_ratio(row):
    return len(row[row.values == 2]) / len(row)


def app_seconds(row):
    return sum([int(re.findall('[0-9]+', x)[0]) for x in row if type(x) == str])


def inactive_days(row):
    return len(row[row.values == 0])


def last_action(row):
    for i in row.values.tolist()[::-1]:
        if i != 0:
            if type(i) == str:
                return 3
            else:
                return i
    return 0


def utilization_ratio(row):
    return len(row[row != 0]) / len(row)


def remove_outliers(df, cols):
    index = []
    for col in cols:
        options = set(df[col])
        for option in options:
            s = df['future_redemptions'][df[col] == option]
            index.extend(s[(s - s.mean()).abs() > 3 * s.std()].index.values.tolist())
    index = set(index)
    df = df.loc[~df.index.isin(index)]
    return df

if __name__ == '__main__':
    pass
