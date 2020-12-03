# FPM PLAYER

<!-- TABLE OF CONTENTS -->

## Table of Contents

- [About the Project](#about-the-project)
- [Challenge](#challenge)
- [Game](#game)
- [Client](#client)
  - [Prerequisites](#client-prerequisites)
  - [Installation](#client-installation)
  - [Usage](#client-usage)
- [Server](#server)
  - [Prerequisites](#server-prerequisites)
  - [Usage](#server-usage)
- [Authors](#authors)
- [Contributions](#contributions)
- [License](#license)

<!-- ---------------------------------------------------------------------- -->
<!-- ---------------------------------------------------------------------- -->

## About The Project

The presentation pitch is available at [this link](./FPM-project-pitch.pdf).

## Challenge

...

## Game

...

<!-- ---------------------------------------------------------------------- -->
<!-- ---------------------------------------------------------------------- -->

## Client

### Client Prerequisites

```sh
$ chmod +x scripts/*
```

Install a virtualenv:

```sh
$ python -m venv venv
```

Activate the virtualenv:

```sh
$ source venv/bin/activate
```

<!-- ---------------------------------------------------------------------- -->

### Client Installation

```sh
$ pip install wheel
$ pip install .
$ pip install -r requirements.txt
```

Now you have:

```sh
$ fpm_tablut_player

  usage: fpm_tablut_player [-h] [--role {black,white}] [--timeout TIMEOUT] [--server SERVER]

  optional arguments:
  -h, --help            show this help message and exit
  --role {black,white}  player role
  --timeout TIMEOUT     move timeout
  --server SERVER       server ip address
```

### Client Usage

Black Player

```sh
$ source venv/bin/activate && fpm_tablut_player --role 'black' --timeout 60 --server '127.0.0.1'
```

White Player

```sh
$ source venv/bin/activate && fpm_tablut_player --role 'white' --timeout 60 --server '127.0.0.1'
```

<!-- ---------------------------------------------------------------------- -->
<!-- ---------------------------------------------------------------------- -->

## Server

### Server Prerequisites

```sh
$ git submodule update --init --recursive --remote
$ cd server/Tablut
```

### Server Usage

Follow the instructions insde the [README.md](https://github.com/AGalassi/TablutCompetition/blob/master/README.md) file.

<!-- ---------------------------------------------------------------------- -->
<!-- ---------------------------------------------------------------------- -->

## Authors

 - [Matteo Conti](https://github.com/contimatteo)
 - [Francesco Palmisano](https://github.com/Frankgamer97)
 - [Primiano Armino Cristino](https://github.com/primiarmi)

## License

...
