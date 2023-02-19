<h1 align="center">
    <br>
    <img src="https://raw.githubusercontent.com/haxerzin/FFList/main/FFList.png" alt="FFList">
    <br>
    FFList
</h1>

<p align="center">
    A Fast Asynchronous System File Lister
</p>

## Features

- [x] Completely Asynchronous
- [x] Gather All System Files
- [x] Gather Files From Specified Directory
- [x] Gather Files From List Of Directories
- [x] Print Output
- [x] Cross Platform

## System Requirements

- [x] Windows / Linux / Mac
- [x] Python 3.11

## Installing FFList

```bash
git clone --depth=1 https://github.com/haxerzin/FFList
```

```bash
cd FFList
```

```bash
python -m pip install requirements.txt
```

```bash
python fflist.py --help
```

### Examples Use

#### Gather All System Files

```bash
python fflist.py -full
```

#### Gather files from specific directory recursive

```bash
python fflist.py -dir "C:/Program Files/"
```

#### Gather files from list of directories

- Add directory paths inside `dirs.txt`

```bash
python fflist.py -read dirs.txt
```

- Print output after gathering files from list of directories

```bash
python fflist.py -r dirs.txt -print
```

## License

<a href="https://github.com/haxerzin/FFList/blob/main/LICENSE" title="License">GPLv3</a>
