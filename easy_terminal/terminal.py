from threading import Thread
from easy_events import *
import asyncio, time, gc


class Debug():
    def __init__(self):
        self.sync = Events(first_parameter_object=False)
        self.asyn = AsyncEvents(first_parameter_object=False)
        Thread(target=self._inputs).start()

    def get_object(self, object: str):
        for elem in gc.get_objects():
            if isinstance(elem, dict) and f"__main__.{object}" in str(elem):
                return elem.get(object)

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

            base = self.get_object(base)

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
                event_type = str(is_class[0]).split("__main__.")[1]

                if " " in event_type:
                    event_type = event_type.split(" ")[0]
                event_type = event_type.replace("'>", "")

                sync = self.sync.grab_event(is_class[-1], event_type)
                asyn = self.asyn.grab_event(is_class[-1], event_type)
            else:
                sync = self.sync.grab_event(command._event, None)
                asyn = self.asyn.grab_event(command._event, None)

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

    def _execute_async_class(self, event: callable, parameters: dict):
        asyncio.run(event(**parameters))

    def _execute_class(self, event: callable, parameters: dict):
        event(**parameters)

    def _execute_async(self, command):
        asyncio.run(self.asyn.trigger_run(command, None))

    def _execute(self, command):
        self.sync.trigger(command, None)

    def event(self, callback: callable):
        event_type = None

        if "." in str(callback):
            event_type = str(callback).split(".")[0].replace("<function ", "")

        if asyncio.iscoroutinefunction(callback):
            self.asyn.event(callback=callback, aliases=[], type=event_type)
        else:
            self.sync.event(callback=callback, aliases=[], type=event_type)


_cmd = Debug()


def terminal():
    def add_debug(func):
        _cmd.event(callback=func)
        return func

    return add_debug


if __name__ == "__main__":

    class A:
        def __init__(self, name="Test"):
            self.name = name

        @terminal()
        async def yo(self, a="a", b="b", c="c"):
            print("plait", a, b, c)

    a = A("a")

    @terminal()
    async def test(a="a", b="b"):
        print("test", a, b)

    @terminal()
    def test1(b="b", c="c"):
        print("test1", b, c)


    @terminal()
    def yo():
        print("gourt")
