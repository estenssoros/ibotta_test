import matplotlib.pyplot as plt
plt.style.use('ggplot')
import pandas as pd
import subprocess

def plot_scatter_matrix():
    df = pd.read_pickle('../data/df.pickle')
    cols = [x for x in df.columns if x != 'future_redemptions']
    fig, axs = plt.subplots(1, len(cols), figsize=(22, 4), sharey=True)
    for col, ax in zip(cols, axs):
        ax.scatter(df[col], df['future_redemptions'], alpha=0.8)
        ax.set_title(col, y=1.05)
        ax.set_xlim(-0.05, df[col].max() * 1.05)

    plt.ylim(0, df['future_redemptions'].max() * 1.05)
    plt.tight_layout()

    save_name = '../images/scatter_matrix.png'
    plt.savefig(save_name)
    plt.close()
    subprocess.Popen(['open', save_name])


def plot_feature_ranges():
    df = pd.read_pickle('../data/df.pickle')
    del df['redeemed']
    del df['future_redemptions']

    results = pd.read_pickle('../data/results.pickle')
    fig, axs = plt.subplots(2, 4, figsize=(20, 8))
    for col, ax in zip(df.columns, axs.flatten()):
        x = results['value'][results['feature'] == col]
        y = results['prediction'][results['feature'] == col]
        ax.scatter(x, y)
        ax.set_title(col)

    plt.tight_layout()
    save_name = '../images/feature_ranges.png'
    plt.savefig(save_name)
    plt.close()
    subprocess.Popen(['open', save_name])

if __name__ == '__main__':
    pass
