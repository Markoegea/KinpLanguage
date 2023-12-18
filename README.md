# Kinp Language

This project aims to create a new programming lenguage open source, with a syntaxis in spanish.

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [Credits](#credits)
- [License](#license)
- [Contact Information](#contact-information)
- [FAQs](#faqs)
- [Examples/Demo](#examplesdemo)
- [Roadmap](#roadmap)
- [Security](#security)
- [Dependencies](#dependencies)

## Description

This project is a programming lenguage open source, based in Python with inspiration in JavaScript and C#.

Use Python to read the given text letter by letter, to transform them in tokens that are parsed to generate an abstact syntax tree, next is evaluated node by node, to give the desirable output.

Have a syntaxis in spanish because is aimed to help spanish speakers students to understand the very basics of programming languages and how to program.

## Installation

For the moment the installation procces is very easy:
1. Go to the code button
2. Select if you want to clone the project with Github or Download the ZIP folder.
3. Open the project with your favorite code editor or IDE (In my case I use Visual Studio Code)
4. Import the necessary libraries
5. To open it you have to write in the console:

In linux
``` console
python3 main.py (the path of your file .kp)
```

In Windows
``` console
py main.py (the path of your file .kp)
```

## Usage

When you want to run your file written in Kinp code, use: 

``` console
python3 main.py (path to Kinp file)
```

For example
``` console
python3 main.py examples/factorial_2.kp
```

or leave the file path empty to run the loop evaluator, to run code in your command console.

For example
``` console
python3 main.py
```

## Features

- Programming language
- Open source
- Functional programming
- Spanish Syntax
- Interpreter
- Educational

## Documentation

COMING SOON!

## Contributing

COMING SOON!

## Credits

- https://platzi.com/cursos/interpretes-software/ To teach how to create a programming language from zero.

## License

Project under the Apache License 2.0.

## Contact Information

Gmail: thekingmarco03@gmail.com
LinkedIn: https://www.linkedin.com/in/markoegea/

## FAQs

Make your question and they will be posted here.

## Examples/Demo

COMING SOON!

## Roadmap

The future plans for the Kinp Language are:

- Improve the error handling.
- Create the Lists objects.
- Create the Conditions statement (Switch).
- Create the loops statement (For, While, Do-While).
- Support the Object-oriented paradigm (Classes).

## Security

Any information regarding security vulnerabilities, please write to the email: thekingmarco03@gmail.com.

## Dependencies

- [mypy] Is a static type checker for Python. It helps catch errors and bugs
by analyzing and inferring types, allowing for a more robust and reliable codebase.

- [mypy-extensions] Is a package that provides additional functionality and type hints for use with mypy. It includes various extensions and annotations to enhance type checking capabilities beyond what's available in the standard Python typing module.

- [nose] Is a testing framework for Python. It extends Python's built-in unittest module, making it easier to write and execute tests by providing additional features and a more user-friendly interface.

- [tomli] Is a library for parsing and manipulating TOML (Tom's Obvious, Minimal Language) files in Python. TOML is a configuration file format that aims to be easy to read and write due to its simplicity and human-friendly syntax.

- [typing-extensions] Provides backports and additions to the typing module in Python. It includes extra utilities and type hints that are not available in earlier Python versions, enabling to write more expressive and precise type annotations.