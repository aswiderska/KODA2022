# KODA2022

### Kodowanie Tunstalla

* [ ] Opracować koder i dekoder Tunstalla (np. pozycja [2] literatury uzupełniającej do wykładu).
* [ ] Przetestować algorytm na sztucznie wygenerowanych ciągach danych o rozkładzie równomiernym,
  normalnym, geometrycznym oraz obrazach testowych.
* [ ] Wyznaczyć histogram i entropię danych wejściowych. Porównać entropię ze średnią długością bitową
  kodu wyjściowego.
* [ ] Ocenić efektywność algorytmu do kodowania obrazów naturalnych.
* [ ] Porównanie z innymi metodami kompresji.
* [ ] Zbadanie wpływu "parametrów kodu T." na efektywność kompresji. Parametrem jest długość słowa
  kodowego - sprawdzić, jak zmiana tego parametru wpływa na średnią bitową, a nie ograniczać się
  tylko do jednej, arbitralnie przyjętej wartości.


## Requirements

`python >= 3.6`
`pip`
`numpy`
`scipy`
`pandas`
`matplotlib`

## Setup

### Install system requirements

* _Linux (eg. Ubuntu):_

```commandline
sudo apt update
sudo apt install python3 python3-pip
```

* _Windows_

https://www.python.org/downloads/

This will install Python as well as `pip`.

### Install Python requirements

1. Make sure Python and `pip` are installed and added to `PATH` system variable.
2. Open terminal or command prompt and in the project directory type:

```commandline
pip3 install -r requirements.txt
```

---

### Usage

First, change the parameters in the [config/config.json](config/config.json)
file.

You can also create your own json file with all needed parameters, for example:

```json
{
  "data_path": "data/obrazy/",
  "results_path": "results/results_obrazy.json",
  "multithreaded": true,
  "k_values": [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
}
```

* `data_path` - path to a directory containing files (or file) to encode
* `results_path` - path to a file where the results should be stored
* `multithreaded` - use thread pool for computation. If false all computations
  are carried out in the main thread
* `k_values` - a list of values for k parameter (bit length of encoded symbol)

To run the program, use `main.py` script:

```commandline
python3 main.py
```