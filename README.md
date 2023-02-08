# easy-terminal

**A library that help you to debug the code in terminal**

## Getting started

1. [**Installation**](#installation)
2. [**Usages**](#usages)
3. [**Code example**](#code-example)
4. [**Documentation**](#documentation)

## Installation

#### `pip install easy-terminal`

##### Require easy-events>=2.2.0

GitHub : [Github](https://github.com/ThePhoenix78/easy-debug)


## Usages

Add the @debug() before the function you want to try in the terminal

## Code example

```py
from easy_terminal import terminal


@terminal()
def test1():
	do_action_here


@terminal()
async def test1(arg1, arg2, *, arg3):
	do_action_here

```

### This lib make you run python function in a terminal
