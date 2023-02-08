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


"""
>hello
world

>A.hello
world 1

>a.hello
world 6
"""
