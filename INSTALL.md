## Installation

We recommend installation in a virtual environment, either `conda` or `pyenv`.

### Create a `conda` environment

```
$> conda create -n libpyvinyl
```

### Common users

```
$> pip install libpyvinyl
```

### Developers of libpyvinyl

We provide a requirements file for developers in _requirements/dev.txt_.

```
$> conda install --file requirements/dev.txt --file requirements/prod.txt
```

**or**

```
$> pip install -r requirements/prod.txt -r requirements/dev.txt 
```


Then, install `libpyvinyl` into the same environment. The `-e` flag links the installed library to
the source code in the local path, such that changes in the latter are immediately effective in the installed version.

```
$> pip install -e .
```
