import matplotlib.pyplot as plt
plt.style.use('ggplot')
import pandas as pd
from list_dicts import day_dict
from ibotta_ml import get_data
import subprocess
import os


def main():
    df = get_data()
    subprocess.Popen(['say', 'data processed'])
    df.to_pickle('data/df.pickle')
    df = pd.read_pickle('data/df.pickle')
    cols = df.columns.values.tolist()
    cols.remove('future_redemptions')
    fig, axs = plt.subplots(1, len(cols), figsize=(22, 4), sharey=True)
    for col, ax in zip(cols, axs):
        ax.scatter(df[col], df['future_redemptions'], alpha=0.8)
        ax.set_title(col, y=1.05)
        ax.set_xlim(-0.05, df[col].max() * 1.05)

    plt.ylim(0, df['future_redemptions'].max() * 1.05)
    plt.tight_layout()

    save_name = 'images/scatter_matrix.png'
    plt.savefig(save_name)
    plt.close()
    subprocess.Popen(['open', save_name])
    subprocess.Popen(['say', 'chart saved'])

if __name__ == '__main__':
    main()
