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

Add the @terminal() before the function you want to try in the terminal

## Code example

```py
from easy_terminal import terminal


class A:
    nb = 1

    def __init__(self, nb=5):
        self.nb = nb

    @terminal()
    def hello(self):
        print("world", self.nb, "\n")

a = A(6)

@terminal()
def hello():
    print("world\n")
    
    
@terminal()
def pc(processor: str = "intel", ram: str = "8go"):
    print(f"processor: {processor}\nram : {ram}\n")


"""
>hello
world

>A.hello
world 1

>a.hello
world 6

>pc
processor: intel
ram : 8go

>pc amd
processor: amd
ram : 8go

>pc amd 16go
processor: amd
ram : 16go
"""

```

### This lib make you run python function in a terminal
