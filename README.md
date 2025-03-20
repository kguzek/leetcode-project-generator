# LeetCode Project Generator

A CLI tool created using [Click](https://click.palletsprojects.com/en/8.1.x/).
This utility creates a barebones project template from the URL of a LeetCode problem.

## Installation

```sh
python -m pip install setuptools, build
python -m build
python -m pip install ./dist/lpg-*-py3-none-any.whl
```

## Usage

```sh
python -m lpg (--title_slug <problem title> | --url <problem url>) [--directory <project directory>] [--lang <language>] [--force] [--git-init]
```

"Title slug" refers to the dashed title of the LeetCode problem which can be found in the URL of the problem.
E.g. for [https://leetcode.com/problems/two-sum/](https://leetcode.com/problems/two-sum/), the title slug is `two-sum`.

The default language is C. Other languages are currently unsupported.
If using Bash, you must surround the URL with quotes, since the `&` symbol would be interpreted as an asynchronous command.

The project directory defaults to `~/Documents/Coding/{language_name}/`. You may use use the template `{language_name}` when specifying the directory, and this will automatically be translated into the name of the language specified using `--lang`. E.g.: `cpp -> C++`.
The project will be created in its own directory with the name of the title slug within this directory. This is unchangeable.

For more syntax help, use the `help` option.

```sh
python -m lpg --help
```

## Roadmap

Planned available languages:

- python
- python3
- javascript
- typescript
- c
- cpp
- csharp
- java
- php
- swift
- kotlin
- dart
- golang
- ruby
- scala
- rust
- racket
- erlang
- elixir

Thanks for reading!
