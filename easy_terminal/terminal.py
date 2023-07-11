from threading import Thread
from easy_events import Events, AsyncEvents, Parameters
import asyncio, time, gc, copy

print("DEBUG")

class Debug():
    def __init__(self):
        self.sync = Events(first_parameter_object=False)
        self.asyn = AsyncEvents(first_parameter_object=False)
        self.run = True
        self.main_function = None
        Thread(target=self._inputs).start()

    def get_object_old(self, object: str):
        for elem in gc.get_objects():
            if isinstance(elem, dict) and f"__main__.{object}" in str(elem):
                return elem.get(object)

    def get_object(self, object: str):
        for elem in gc.get_objects():
            if isinstance(elem, dict) and object in str(elem):
                val = elem.get(object)
                if not val:
                    continue

                if "<class __main__." in str(val):
                    return val, "__main__."

                elif "<class " in str(val):
                    return val, str(val)[8:-str(val)[::-1].index(".")]


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
        while self.run:
            command = input("> ")

            if not command:
                continue

            is_class = self.analyse_input(command)
            command = Parameters(command)

            if is_class:
                event_type = str(is_class[0][0]).split(is_class[0][1])[1]

                if " " in event_type:
                    event_type = event_type.split(" ")[0]

                event_type = event_type.replace("'>", "")

                print(event_type)

                sync = self.sync.grab_event(is_class[-1], event_type)
                asyn = self.asyn.grab_event(is_class[-1], event_type)

            else:
                sync = self.sync.grab_event(command._event, None)
                asyn = self.asyn.grab_event(command._event, None)

            if (sync or asyn) and is_class:
                event = getattr(is_class[0][0], is_class[1])

                command._parameters = command._parameters.split()
                command._parameters.insert(0, is_class[0][0])
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

            elif self.main_function:
                command._parameters = command._parameters.split()
                command._parameters.insert(0, command._event)

                if self.main_function == "sync":
                    event = self.sync.get_events_type("__main")[0].event
                    dico = self.sync.build_arguments(event, command._parameters)
                    Thread(target=self._execute_class, args=[event, dico]).start()

                elif self.main_function == "async":
                    event = self.asyn.get_events_type("__main")[0].event
                    dico = self.sync.build_arguments(event, command._parameters)
                    Thread(target=self._execute_async_class, args=[event, dico]).start()

            time.sleep(.1)

    def _execute_async_class(self, event: callable, parameters: dict):
        try:
            asyncio.run(event(**parameters))
        except Exception:
            asyncio.run(event())
            
    def _execute_class(self, event: callable, parameters: dict):
        try:
            event(**parameters)
        except Exception:
            event()

    def _execute_async(self, command):
        asyncio.run(self.asyn.trigger(command, None))

    def _execute(self, command):
        self.sync.trigger(command, None)

    def stop(self):
        self.run = False

    def event(self, callback: callable, aliases: list = []):
        event_type = None

        if isinstance(aliases, str):
            aliases = [aliases]

        if "." in str(callback):
            event_type = str(callback).split(".")[0].replace("<function ", "")

        if asyncio.iscoroutinefunction(callback):
            self.asyn.event(callback=callback, aliases=aliases, type=event_type)
        else:
            self.sync.event(callback=callback, aliases=aliases, type=event_type)

        aliases.clear()

    def main(self, callback: callable):
        if asyncio.iscoroutinefunction(callback):
            self.asyn.event(callback=callback, type="__main")
            self.main_function = "async"
        else:
            self.sync.event(callback=callback, type="__main")
            self.main_function = "sync"


_cmd = Debug()


def terminal(aliases: list = [], callback: callable = None):
    def add_debug(func):
        _cmd.event(callback=func, aliases=aliases)
        return func

    if callback:
        return add_debug(callback)

    return add_debug

def main():
    def add_main(func):
        _cmd.main(callback=func)
        return func

    return add_main


if __name__ == "__main__":

    class A:
        def __init__(self, name="Test"):
            self.name = name

        @terminal()
        async def yo(self, a="a", b="b", c="c"):
            print("plait", a, b, c)

    a = A("a")

    @terminal("test2")
    async def test(a="a", b="b"):
        print("test", a, b)

    @terminal()
    def test1(b="b", c="c"):
        print("test1", b, c)


    def yo():
        print("gourt")

    terminal(callback=yo)

    @main()
    def magic(magic):
        print(f"Hello {magic}\n")
