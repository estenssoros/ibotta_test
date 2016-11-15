from __future__ import division
import pandas as pd
import numpy as np
from time import time
import os
from multiprocessing import Pool, cpu_count
# -----------------------------------------
from list_dicts import day_columns, day_dict
from eda import plot_feature_ranges
from feature_functions import *
# -----------------------------------------
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report, r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.grid_search import GridSearchCV
# -----------------------------------------
import statsmodels.api as sm


def multi_apply(arg):
    t1 = time()
    df_cols, func = arg
    series = df_cols.apply(lambda x: func(x), axis=1), func.__name__
    print '   {0} - {1:.2f} seconds'.format(func.__name__, time() - t1)
    return series


def get_data():
    fname = "../data/Ibotta_Marketing_Analyst_Dataset_daily.csv"
    df = pd.read_csv(fname)
    df.pop('customer_id')

    df['start_day'] = df.apply(lambda x: day_dict[x['start_day']], axis=1)
    df = fix_columns(df)

    # from feature_functions.py
    functions = [days_since_last,
                 engagement_ratio,
                 verify_ratio,
                 app_seconds,
                 inactive_days,
                 last_action,
                 utilization_ratio]

    cores = cpu_count()
    print 'feature engineering... using {}/{} cores'.format(cores - 1, cores)
    pool = Pool(processes=cores - 1)
    df_cols = df[day_columns]
    function_list = [(df_cols, func) for func in functions]
    results = pool.map(multi_apply, function_list)
    pool.close()
    pool.join()

    for series, f_name in results:
        df[f_name] = series

    print 'trimming_outliers'
    cols = [func.__name__ for func in functions]
    cols.remove('app_seconds')

    df = remove_outliers(df, cols)

    # redeemed classification/regression column
    df['redeemed'] = df.apply(lambda x: x['future_redemptions'] > 0, axis=1)

    print '   - upsampling data'
    df_redeemed = df[df['redeemed'] == True]
    k = len(df) - len(df_redeemed)
    up_sample = df_redeemed.iloc[
        np.random.randint(0, len(df_redeemed), size=k)]
    df = df.append(up_sample, ignore_index=True)

    print '   - removing columns'
    cols = [x for x in df.columns if x not in day_columns]
    df = df[cols]
    pickle_name = '../data/df.pickle'
    df.to_pickle(pickle_name)
    print 'data saved to {0}'.format(pickle_name)
    return df


def split_data(df):
    split_df = df.copy()
    y = split_df.pop('redeemed').values
    X = split_df.values
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    return X_train, X_test, y_train, y_test


def initialize_models():
    estimators = dict()
    estimators['RandomForestClassifier'] = RandomForestClassifier(
        n_jobs=-1, random_state=1)
    estimators['GradientBoostingClassifier'] = GradientBoostingClassifier(
        random_state=1)
    estimators['AdaBoostClassifier'] = AdaBoostClassifier(random_state=1)
    estimators['KNeighbors'] = KNeighborsClassifier(n_jobs=-1)
    return estimators


def train_models():
    df = pd.read_pickle('../data/df.pickle')
    if 'future_redemptions' in df.columns:
        del df['future_redemptions']
    estimators = initialize_models()
    X_train, X_test, y_train, y_test = split_data(df)
    for name, model in estimators.iteritems():
        t1 = time()
        print 'Training: {}'.format(name)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        print 'operation took: {} seconds'.format(time() - t1)
        print 'classification_report:'
        print classification_report(y_test, y_pred)
        print 'x' * 60


def grid_search(df, model, grid):
    print 'gridsearching {}....'.format(model.__class__.__name__)
    X_train, X_test, y_train, y_test = split_data(df)

    gridsearch = GridSearchCV(model(),
                              grid,
                              n_jobs=-1,
                              verbose=True,)
    gridsearch.fit(X_train, y_train)
    print 'best parameters:', gridsearch.best_params_
    best_model = gridsearch.best_estimator_
    print 'classification report:'
    print classification_report(y_test, best_model.predict(X_test))
    return gridsearch


def grid_search_models():
    df = pd.read_pickle('../data/df.pickle')
    random_forest_grid = {'max_depth': [3, 5, None],
                          'max_features': ['sqrt'],
                          'min_samples_split': [1],
                          'min_samples_leaf': [1],
                          'bootstrap': [True],
                          'n_estimators': [40, 50],
                          'random_state': [1]}

    gradient_boost_grid = {'loss': ['deviance', 'exponential'],
                           'learning_rate': [0.1, 0.01],
                           'n_estimators': [100, 200],
                           'subsample': [0.8, 1.0],
                           'min_samples_split': [2, 5],
                           'min_samples_leaf': [1, 3],
                           'max_depth': [3, None],
                           'random_state': [1]}

    ada_boost_grid = {'n_estimators': [50, 100],
                      'learning_rate': [1, 0.1],
                      'algorithm': ['SAMME', 'SAMME.R'],
                      'random_state': [1]}

    grid_search(df, RandomForestClassifier, random_forest_grid)
    grid_search(df, GradientBoostingClassifier, gradient_boost_grid)
    grid_search(df, AdaBoostClassifier, ada_boost_grid)


def train_rfc_model():
    df = pd.read_pickle('../data/df.pickle')
    if 'future_redemptions' in df.columns:
        del df['future_redemptions']
    y = df.pop('redeemed').values
    X = df.values
    rf = RandomForestClassifier(n_jobs=-1, random_state=1)
    rf.fit(X, y)
    for col, imp in zip(df.columns, rf.feature_importances_):
        print '{0} - {1:.2f}'.format(col, imp * 100)
    return rf


def train_rfr_model():
    df = pd.read_pickle('../data/df.pickle')
    if 'redeemed' in df.columns:
        del df['redeemed']
    y = df.pop('future_redemptions').values
    X = df.values
    print X.shape
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    rf = RandomForestRegressor(n_jobs=-1, random_state=1)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)
    print 'r^2 score: {}'.format(r2_score(y_pred, y_test))
    return rf


def train_ols():
    df = pd.read_pickle('../data/df.pickle')
    y_final = df.pop('future_redemptions')
    rf = train_rfc_model()
    del df['redeemed']
    df['rf_classification'] = rf.predict(df.values)
    X = sm.add_constant(df)
    model = sm.OLS(y_final, X.astype(float)).fit()
    print model.summary()


def test_feature_ranges():
    df = pd.read_pickle('../data/df.pickle')
    del df['redeemed']
    rf = train_rfr_model(df)
    del df['future_redemptions']
    results = pd.DataFrame(columns=['feature', 'value', 'prediction'])
    for i, col in enumerate(df.columns):
        col_means = [df[x].mean() for x in df.columns]
        col_range = np.linspace(df[col].min(), df[col].max(), 100)
        for item in col_range:
            col_means[i] = item
            pred = rf.predict(np.array(col_means).reshape(1, 8))[0]
            results = results.append({'feature': col,
                                      'value': item,
                                      'prediction': pred}, ignore_index=True)
    results.to_pickle('../data/results.pickle')


def main_ml():
    if not os.path.isfile('../data/df.pickle'):
        get_data()
    train_models()
    train_rfc_model()
    train_ols()
    plot_feature_ranges()

if __name__ == '__main__':
    main_ml()
