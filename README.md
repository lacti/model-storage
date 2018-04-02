# Model Storage Module
- The aim of this project is to create a model storage to maintain machine learning models. Users can upload and download their models through python library or command lines.


# Install

## pip
```bash
$> wget https://raw.githubusercontent.com/hyunjong-lee/model-storage/master/CONFIGURATION.sample.json -O conf.json
$> vim conf.json # change to fit your environment
$> pip install git+https://github.com/hyunjong-lee/model-storage.git@master --install-option="--config-path=$(pwd)/conf.json"
```

## setup.py
```bash
$> git clone https://github.com/hyunjong-lee/model-storage.git
$> cd model-storage
$> vim CONFIGURATION.sample.json # change to fit your environment
$> python setup.py install --config-path="CONFIGURATION.sample.json"
```

# Usage

## bash

```bash
$> mstorage create-table # first time, you need to create table using create-table command
$> mstorage list SERVICE MODEL [LIMIT]
$> mstorage pull SERVICE MODEL OUT_FNAME [VERSION]
$> mstorage push SERVICE MODEL LOCAL_FNAME [ACTIVE]
```

## python

```python
$> python
Python 3.6.4 (default, Mar  9 2018, 23:15:03)
[GCC 4.2.1 Compatible Apple LLVM 9.0.0 (clang-900.0.39.2)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from mstorage import ModelStorage
>>> ms = ModelStorage()
>>> ms.list('svc1', 'test-model')
>>> ms.push('svc1', 'test-model', 'linear_test.model')
>>> ms.pull('svc1', 'test-model', 'linear_test.model.download')
```