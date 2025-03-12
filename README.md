# Infix to Prefix Converter

This repository contains the **Infix to Prefix Converter**, a GUI-based application designed to convert infix expressions to prefix notation and evaluate them. It supports arithmetic operations, trigonometric functions, and variable handling.

## Features

- **Expression Conversion**: Converts infix expressions to prefix notation.
- **Mathematical Operations**: Supports `+`, `-`, `*`, `/`, `%`, `^`, `sin`, `cos`, and `sqrt`.
- **Parentheses Validation**: Ensures expressions are properly balanced.
- **Variable Assignment**: Allows users to assign values dynamically.
- **User-Friendly GUI**: Built with `tkinter` for easy interaction.

## Prerequisites

To run this project, ensure you have the following installed:

- **Python 3.x** or higher
- Required libraries: `tkinter`, `pythonds`

## Installation

Clone this repository to your local machine:

```bash
git clone https://github.com/mahmoud375/Prefix-project.git
cd Prefix-project
```

Navigate to the project directory and install dependencies:

```bash
pip install -r requirements.txt
```

Run the script:

```bash
python Prefix.py
```

## Usage

1. Enter an infix expression in the input field.
2. Click the "Evaluate" button to convert and compute the result.
3. If variables exist, input their values when prompted.
4. View the prefix notation and result in the GUI.
5. Click "Reset" to clear the fields.

## Example Expressions

- `(3 + 5) * 2`
- `a + b * c`, where `a`, `b`, and `c` require user-defined values.
- `sin(30) + sqrt(9)`

## Author

Developed by [Mahmoud Elgendy]

## License

This project is licensed under the MIT License.
