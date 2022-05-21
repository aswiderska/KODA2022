from pathlib import Path

import cv2
import matplotlib.pyplot as plt
from matplotlib.image import imread


def plot_histogram(img_path, out_path=None, fig=None, subplot=(1, 1, 1)):
    img_file = Path(img_path)

    img = imread(str(img_file.resolve()), cv2.IMREAD_GRAYSCALE)

    if not fig:
        fig = plt.figure()
        plt.xlabel('pixel value')
        plt.ylabel('pixel frequency')

    fig.add_subplot(*subplot)
    plt.hist(img.ravel(), bins=256, density=True)
    plt.title(img_file.name)

    if not out_path:
        return

    out_dir = Path(out_path)
    out_file = img_file.with_name(f'histogram_{img_file.stem}.svg')
    plt.savefig(out_dir.joinpath(out_file.name))


def main():
    output_dir_path = '/home/darkroom2/DEV/KODA/KODA2022/plots'
    img_dir_path = '/home/darkroom2/DEV/KODA/KODA2022/data/rozklady'
    img_dir = Path(img_dir_path)
    fig = plt.figure(figsize=(14, 10), tight_layout=True)
    plt.suptitle('Histograms')
    plt.xlabel('pixel value')
    plt.ylabel('pixel frequency')
    plt.axis('off')
    for i, img_file in enumerate(img_dir.iterdir()):
        plot_histogram(img_file, fig=fig, subplot=(2, 5, i + 1))

    out_dir = Path(output_dir_path)
    plt.savefig(out_dir.joinpath(f'histogram_{img_dir.stem}.svg'))


if __name__ == '__main__':
    main()
