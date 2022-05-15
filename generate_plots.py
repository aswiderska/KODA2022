from json import loads
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt


def main():
    results_path = 'results/results_rozklady.json'
    results_file = Path(results_path)
    results = loads(results_file.read_bytes())

    k_vals = list(results.keys())
    img_names = list(results[k_vals[0]])

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
        sizes_by_k['original_size'][k] = [results[k][img_name]['original_size'] for img_name in img_names]
        sizes_by_k['encoding_size'][k] = [results[k][img_name]['encoding_size'] for img_name in img_names]
        sizes_by_k['encoded_size'][k] = [results[k][img_name]['encoded_size'] for img_name in img_names]
        sizes_by_k['unencoded_size'][k] = [results[k][img_name]['unencoded_size'] for img_name in img_names]

    for img_name in img_names:
        sizes_by_name['original_size'][img_name] = [results[k][img_name]['original_size'] for k in k_vals]
        sizes_by_name['encoding_size'][img_name] = [results[k][img_name]['encoding_size'] for k in k_vals]
        sizes_by_name['encoded_size'][img_name] = [results[k][img_name]['encoded_size'] for k in k_vals]
        sizes_by_name['unencoded_size'][img_name] = [results[k][img_name]['unencoded_size'] for k in k_vals]

    # avg_bit_length plot
    plt.figure(1)
    for img in img_names:
        img_avg_bit_length = []
        for k in k_vals:
            img_avg_bit_length.append(results[k][img]['avg_bit_length'])
        plt.plot(k_vals, img_avg_bit_length, label=img)
    plt.title('Average bit length of symbols to be encoded, for different code lengths')
    plt.xlabel('code length')
    plt.ylabel('avg. symbol bit length')
    plt.legend()
    plt.savefig(f'plots/avg_bit_length_{results_file.stem}.svg')

    # encoding_size plot
    plt.figure(2)
    for img in img_names:
        img_encoding_size = []
        for k in k_vals:
            img_encoding_size.append(results[k][img]['encoding_size'])
        plt.plot(k_vals, img_encoding_size, label=img)
    plt.yscale('log')
    plt.title('Encoding dictionary size, for different code lengths')
    plt.xlabel('code length [bits]')
    plt.ylabel('encoding size [bytes]')
    plt.legend()
    plt.savefig(f'plots/encoding_size_{results_file.stem}.svg')

    # compression plot
    n = 3
    for part in range(n):
        plt.figure(3 + part, figsize=(16, 10))
        separation = 0.1  # separation between groups of bars
        spacing = 0.01  # separation between single bars
        width = (1 - separation) / (len(img_names) + 1)
        shift = width * (len(img_names)) / 2
        for i, img_name in enumerate(img_names):
            y1 = np.array(sizes_by_name['original_size'][img_name])
            y2 = np.array(sizes_by_name['encoded_size'][img_name])
            y3 = np.array(sizes_by_name['unencoded_size'][img_name])
            y4 = np.array(sizes_by_name['encoding_size'][img_name])
            y1 = np.array_split(y1, n)[part]
            y2 = np.array_split(y2, n)[part]
            y3 = np.array_split(y3, n)[part]
            y4 = np.array_split(y4, n)[part]
            _k_vals = np.array_split(k_vals, n)[part]
            x_axis = np.arange(len(_k_vals))
            if i < 1:
                plt.bar(x_axis + (i - 1) * width - shift, y1, width=width - spacing, color='y')
            plt.bar(x_axis + i * width - shift, y1, width=width - spacing, color='k')
            plt.bar(x_axis + i * width - shift, y2, width=width - spacing, color='g')
            plt.bar(x_axis + i * width - shift, y3, bottom=y2, width=width - spacing, color='r')
            plt.bar(x_axis + i * width - shift, y4, bottom=y2 + y3, width=width - spacing, color='b')
        plt.title(f'Original file size vs compressed file size part {part + 1}')
        images_str = ', '.join(img_names)
        plt.xticks([r for r in range(len(_k_vals))],
                   _k_vals)
        plt.xlabel('code length [bits]')
        plt.ylabel('compression size [bytes]')
        plt.legend(["Original", "Difference", "Encoded", "Unencoded", "Encoding"])
        plt.figtext(0.05, 0.05, f"Each bar represents different image in order:\n  {images_str}", size='small')
        plt.savefig(f'plots/compression_{results_file.stem}_{part}.svg')

    # avg_bit_len vs entropy plot
    plt.figure(6, figsize=(16, 10))
    separation = 0.1  # separation between groups of bars
    spacing = 0.01  # separation between single bars
    width = (1 - separation) / (len(img_names) + 1)
    shift = width * (len(img_names)) / 2
    x_axis = np.arange(len(k_vals))
    for i, img_name in enumerate(img_names):
        y1 = np.array([results[k][img_name]['avg_bit_length'] for k in k_vals])
        y2 = np.array([results[k][img_name]['entropy'] for k in k_vals])
        plt.bar(x_axis + i * width - shift, y1, width=width - spacing, color='g')
        plt.bar(x_axis + i * width - shift, y2, width=width - spacing, color='y')
    plt.title(f'Entropy vs Avg. bit length')
    images_str = ', '.join(img_names)
    plt.xticks([r for r in range(len(k_vals))],
               k_vals)
    plt.xlabel('code length [bits]')
    plt.ylabel('value [bits]')
    plt.legend(["Avg. bit length", "Entropy"])
    plt.figtext(0.05, 0.05, f"Each bar represents different image in order:\n  {images_str}", size='small')
    plt.savefig(f'plots/ent_vs_bit_len_{results_file.stem}.svg')


if __name__ == '__main__':
    main()
