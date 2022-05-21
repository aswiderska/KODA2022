from json import loads
from pathlib import Path
from zipfile import ZipFile

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

from main import Simulation


def compare():
    config_path = 'config/config.json'
    sim = Simulation(config_path)
    input_dir = Path(sim.config.get('data_path'))
    file_exts = ['.png', '.jpg', '.webp']
    files = list(input_dir.iterdir())
    results = {
        ext: [] for ext in file_exts
    }
    results['.pgm'] = []
    results['.zip'] = []
    results['order'] = [file.stem for file in files]
    for file in files:
        with ZipFile(file.with_suffix('.zip'), 'w') as zipp:
            zipp.write(file)

        img = cv.imread(str(file.resolve()), cv.IMREAD_GRAYSCALE)
        results['.pgm'].append(len(file.read_bytes()))
        results['.zip'].append(len(file.with_suffix('.zip').read_bytes()))
        file.with_suffix('.zip').unlink()
        for ext in file_exts:
            _, im_buf_arr = cv.imencode(ext, img)
            results[ext].append(len(im_buf_arr.tobytes()))

    results_path = 'results/results_obrazy.json'
    results_file = Path(results_path)
    results2 = loads(results_file.read_bytes())

    k_vals = list(results2.keys())
    img_names = list(results2[k_vals[0]])

    sizes_by_k = {
        'original_size': {},
        'encoding_size': {},
        'encoded_size': {},
        'unencoded_size': {}
    }

    sizes_by_name = {
        'original_size': {},
        'encoding_size': {},
        'encoded_size': {},
        'unencoded_size': {}
    }

    for k in k_vals:
        sizes_by_k['original_size'][k] = [results2[k][img_name]['original_size'] for img_name in img_names]
        sizes_by_k['encoding_size'][k] = [results2[k][img_name]['encoding_size'] for img_name in img_names]
        sizes_by_k['encoded_size'][k] = [results2[k][img_name]['encoded_size'] for img_name in img_names]
        sizes_by_k['unencoded_size'][k] = [results2[k][img_name]['unencoded_size'] for img_name in img_names]

    for img_name in img_names:
        sizes_by_name['original_size'][img_name] = [results2[k][img_name]['original_size'] for k in k_vals]
        sizes_by_name['encoding_size'][img_name] = [results2[k][img_name]['encoding_size'] for k in k_vals]
        sizes_by_name['encoded_size'][img_name] = [results2[k][img_name]['encoded_size'] for k in k_vals]
        sizes_by_name['unencoded_size'][img_name] = [results2[k][img_name]['unencoded_size'] for k in k_vals]

    # avg_bit_len vs entropy plot
    img_names = results['order']
    file_exts.append('.zip')
    file_exts.append('.pgm')
    file_exts.append('Tunstall')
    colors = ['y', 'b', 'g', 'c', 'k', 'm']
    plt.figure(1, figsize=(14, 8))
    separation = 0.1  # separation between groups of bars
    spacing = 0.01  # separation between single bars
    width = (1 - separation) / (len(file_exts) + 1)
    shift = width * (len(file_exts)) / 2
    x_axis = np.arange(len(img_names))
    results['Tunstall'] = [sizes_by_k['encoding_size']['13'][i] +
                           sizes_by_k['encoded_size']['13'][i] +
                           sizes_by_k['unencoded_size']['13'][i] for i in range(len(sizes_by_k['encoding_size']['13']))]
    for i, (ext, color) in enumerate(zip(file_exts, colors)):
        y1 = np.array(results[ext])
        plt.bar(x_axis + i * width - shift, y1, width=width - spacing, color=color)

    plt.title(f'Different compression methods')
    images_str = '.pgm, '.join(img_names)
    plt.xticks([r for r in range(len(img_names))],
               img_names)
    plt.xlabel('image')
    plt.ylabel('size [bytes]')
    plt.legend(file_exts)
    plt.savefig('plots/comparison_obrazy_k_13.svg')

    print('xd')


def main():
    compare()


if __name__ == '__main__':
    main()
