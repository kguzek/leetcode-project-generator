# LeetCode Project Generator

A CLI tool created using [Click](https://click.palletsprojects.com/en/8.1.x/).
This utility creates a barebones project template from the URL of a LeetCode problem.

## Installation

### From PyPI

```sh
pip install leetcode-project-generator
```

### From source

```sh
python -m pip install setuptools, build
python -m build
python -m pip install ./dist/lpg-*-py3-none-any.whl
```

## Usage

### Installed package

```sh
lpg (--title_slug <problem title> | --url <problem url>) [--directory <project directory>] [--lang <language>] [--force] [--git-init] [--git-commit] [--git-commit-message <message>]
```

### Local package

```sh
python -m lpg (--title_slug <problem title> | --url <problem url>) [--directory <project directory>] [--lang <language>] [--force] [--git-init] [--git-commit] [--git-commit-message <message>]
```

### Explanation

"Title slug" refers to the dashed title of the LeetCode problem which can be found in the URL of the problem.
E.g. for <https://leetcode.com/problems/two-sum/description/>, the title slug is `two-sum`.

The default language is C. Other languages are currently unsupported.
If using Bash, you must surround the URL with quotes, since the `&` symbol would be interpreted as an asynchronous command.

The project directory defaults to `~/Documents/Coding/{language_name}/`. You may use use the template `{language_name}` when specifying the directory, and this will automatically be translated into the name of the language specified using `--lang`. E.g.: `cpp -> C++`.
The project will be created in its own directory with the name of the title slug within this directory. This is unchangeable.

### Example

If you want to initialise a project for <https://leetcode.com/problems/two-sum/description/>, then you might type:

```sh
lpg -d /path/to/project -l c 'https://leetcode.com/problems/two-sum/description/'
```

This will create a directory called `/path/to/project/two-sum` and fill it with C language skeleton files. In this case, specifying `-l c` is redundant since C is the default language.

For more syntax help, use the `help` option.

```sh
lpg --help
```

or

```sh
python -m lpg --help
```

## Roadmap

Planned available languages:

- [x] python
- [x] python3 (thanks [@dancikmad](https://github.com/dancikmad))
- [ ] javascript
- [ ] typescript
- [x] c
- [ ] cpp
- [ ] csharp
- [ ] java
- [ ] php
- [ ] swift
- [ ] kotlin
- [ ] dart
- [ ] golang
- [ ] ruby
- [ ] scala
- [ ] rust
- [ ] racket
- [ ] erlang
- [ ] elixir

## Contributing

Know any of the above langauges and want to help out? Your contributions will be greatly appreciated!

For more information on how to implement the language interface, refer to [this issue](https://github.com/kguzek/leetcode-project-generator/issues/1).
Then, fork this repository, make your changes and [submit them as a pull request](https://github.com/kguzek/leetcode-project-generator/compare).

### Testing

You can test all registered language interfaces (including your implementation) by running the test file found at [src/lpg/interfaces/lang_test.py](src/lpg/interfaces/lang_test.py):

```sh
python -m unittest src.lpg.interfaces.lang_test
```

This uses the builtin `unittest` module and executes project generation for each language against an arbitrary list of LeetCode problems in a temporary directory, which is then cleaned up.

Thanks for reading!
