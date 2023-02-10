from easy_terminal import terminal


help_msg = """
pc processor ram    : will print the informations of the pc
hello               : will print world
help                : will show this message
"""

@terminal(aliases=["help"])
def h():
    print(help_msg)


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


@main()
def principal(car: str = "mercedes"):
    print(f"Your car is a {car}")

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

>help

pc processor ram    : will print the informations of the pc
hello               : will print world
help                : will show this message
"""
