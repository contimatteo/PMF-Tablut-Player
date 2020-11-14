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
  - [Installation](#server-installation)
  - [Usage](#server-usage)
- [Authors](#authors)
- [Contributions](#contributions)
- [License](#license)

<!-- ---------------------------------------------------------------------- -->
<!-- ---------------------------------------------------------------------- -->

## About The Project

...

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
$ pip install -r requirements.txt
$ pip install .
```

<!-- ---------------------------------------------------------------------- -->

### Client Usage

```sh
$ fpm_tablut_player
```

<!-- ---------------------------------------------------------------------- -->
<!-- ---------------------------------------------------------------------- -->

## Server

### Server Prerequisites

```sh
$ git submodule update --init --recursive --remote
$ cd server/Tablut
```

Next, follow the instructions insde the [README.md](https://github.com/AGalassi/TablutCompetition/blob/master/README.md).

### Server Installation

```sh
$ ant clean
$ ant compile
```

### Server Usage

```sh
$ ant server
```

<!-- ---------------------------------------------------------------------- -->
<!-- ---------------------------------------------------------------------- -->

## Authors

...

## Contributions

...

## License

...
