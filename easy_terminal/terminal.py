from threading import Thread
from easy_events import *
import asyncio, time


class Debug():
    def __init__(self):
        self.sync = Events(first_parameter_object=False)
        self.asyn = AsyncEvents(first_parameter_object=False)
        Thread(target=self._inputs).start()

    def analyse_input(self, command: str):
        result = []
        base = None
        method = None
        mid = None

        func = command.split(" ", 1)[0]

        if "." in func:
            func2 = func.split(".")
            base = func2[0]
            method = func2[-1]
            mid = method
            if len(func2) > 2:
                mid = func.split(".", 1)[-1]

            base = globals().get(base)

        if not base:
            return

        return [base, mid, method]

    def _inputs(self):
        while True:
            command = input("> ")

            if not command:
                continue

            is_class = self.analyse_input(command)
            command = Parameters(command)

            if is_class:
                sync = self.sync.get_event(is_class[-1])
                asyn = self.asyn.get_event(is_class[-1])
            else:
                sync = self.sync.get_event(command._event)
                asyn = self.asyn.get_event(command._event)

            if (sync or asyn) and is_class:
                event = getattr(is_class[0], is_class[1])

                command._parameters = command._parameters.split()
                command._parameters.insert(0, is_class[0])
                dico = self.sync.build_arguments(event, command._parameters)

                if "__main__" in str(event):
                    del(dico["self"])

                if asyn:
                    Thread(target=self._execute_async_class, args=[event, dico]).start()
                elif sync:
                    Thread(target=self._execute_class, args=[event, dico]).start()

            elif asyn:
                Thread(target=self._execute_async, args=[command]).start()
            elif sync:
                Thread(target=self._execute, args=[command]).start()

            time.sleep(.1)

    def event(self, callback: callable):
        if asyncio.iscoroutinefunction(callback):
            self.asyn.event(callback=callback, aliases=[])
        else:
            self.sync.event(callback=callback, aliases=[])

    def _execute_async_class(self, event: callable, parameters: dict):
        asyncio.run(event(**parameters))

    def _execute_class(self, event: callable, parameters: dict):
        print(parameters)
        event(**parameters)

    def _execute_async(self, command):
        asyncio.run(self.asyn.trigger_run(command))

    def _execute(self, command):
        self.sync.trigger(command)


_cmd = Debug()


def terminal():
    def add_debug(func):
        _cmd.event(callback=func)
        return func

    return add_debug


if __name__ == "__main__":
    class Test:
        def __init__(self, name="Test"):
            self.name = name

        @terminal()
        def yo(self, a, b, c):
            print("plait", a, b, c)

    a = Test("a")

    @terminal()
    async def test(a="a", b="b"):
        print("test", a, b)

    @terminal()
    def test1(b="b", c="c"):
        print("test1", b, c)
