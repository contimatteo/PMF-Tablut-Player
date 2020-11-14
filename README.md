
# Client

<!-- TABLE OF CONTENTS -->
## Table of Contents
* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [License](#license)


<!-- ---------------------------------------------------------------------- -->
<br>
<!-- ---------------------------------------------------------------------- -->


## Prerequisites

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

## Installation

```sh
$ pip install wheel
$ pip install -r requirements.txt
$ pip install .
```

<!-- ---------------------------------------------------------------------- -->

## Usage

```sh
$ echo "TODO: ..."
```


<!-- ---------------------------------------------------------------------- -->
<br>
<!-- ---------------------------------------------------------------------- -->


# Server

## Prerequisites
```sh
$ git submodule update --init --recursive --remote
$ cd server/Tablut
```

Next, follow the instructions insde the [README.md](./server/README.md).


## Installation

```sh
$ ant clean
$ ant compile
```

## Usage

```sh
$ ant server
```