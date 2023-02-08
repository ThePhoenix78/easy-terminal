from threading import Thread
from easy_events import *
import asyncio, time


class Debug():
    def __init__(self):
        self.sync = Events(first_parameter_object=False)
        self.asyn = AsyncEvents(first_parameter_object=False)
        Thread(target=self._inputs).start()

    def _inputs(self):
        while True:
            command = input("> ")

            if not command:
                continue

            command = Parameters(command)
            sync = self.sync.get_event(command._event)
            asyn = self.asyn.get_event(command._event)

            if asyn:
                Thread(target=self._execute_async, args=[command]).start()
            elif sync:
                Thread(target=self._execute, args=[command]).start()
            time.sleep(.1)

    def event(self, callback: callable):
        if asyncio.iscoroutinefunction(callback):
            self.asyn.event(callback=callback)
        else:
            self.sync.event(callback=callback)

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
    @terminal()
    async def test(a="a", b="b"):
        print("test", a, b)

    @terminal()
    def test1(b="b", c="c"):
        print("test1", b, c)
