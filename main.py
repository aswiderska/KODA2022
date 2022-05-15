from functools import partial
from json import loads, JSONDecodeError, dumps
from logging import info
from multiprocessing import Pool
from pathlib import Path

from numpy.random import default_rng

from tunstall import Tunstall
from utils import setup_logger

logger = setup_logger()


class Simulation:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self.load_json(config_path)
        self.results = None

    @staticmethod
    def load_json(path):
        """Parse json file to dict."""

        config_file = Path(path)
        try:
            return loads(config_file.read_text(encoding='utf8'))
        except JSONDecodeError:
            return {}

    def run(self):
        multithreaded = self.config.get('multithreaded', False)
        k_values = self.config.get('k_values', [4])
        data_path = self.config.get('data_path')
        results_path = self.config.get('results_path', 'results.json')

        if not data_path:
            return None

        data_dir = Path(data_path)

        if not data_dir.exists():
            return None

        info('Processing config loaded')

        info(f'Running processing for each image for all k = {k_values} parameters')
        _process = partial(self.process, data_dir=data_dir)
        if multithreaded:
            with Pool() as pool:
                self.results = pool.map(_process, k_values)
        else:
            self.results = map(_process, k_values)

        results_file = Path(results_path)
        results_file.parent.mkdir(parents=True, exist_ok=True)
        results_file.write_text(dumps(list(self.results)))

    def process(self, k, data_dir):

        info(f'k = {k}')

        processing_results = {
            'data_dir': str(data_dir),
            'k': k
        }

        simulator_results = []

        for image in data_dir.iterdir():
            info(f'Running processing for {image.name}')
            tun = Tunstall(k=k)

            content = image.read_bytes()
            _ = tun.encode(content)
            sim_res = tun.get_result()

            sim_res['image'] = image.name

            simulator_results.append(sim_res)

        # Convert the list of dicts, to a dict of lists
        result_keys = list(simulator_results[0].keys())
        aggregated_dict = {k: [] for k in result_keys}
        for res in simulator_results:
            for k, v in res.items():
                aggregated_dict[k].append(v)

        processing_results.update(aggregated_dict)
        return processing_results

    def get_rng(self):
        seed = self.config.get('seed', 123)
        return default_rng(seed)

    def get_results(self):
        return self.results


def main():
    """Running processing on all the data and receiving stats."""
    config_path = 'config/config.json'

    logger.info('Starting processing')

    sim = Simulation(config_path)
    sim.run()

    logger.info('Processing ended')


if __name__ == '__main__':
    main()
