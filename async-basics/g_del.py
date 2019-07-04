
def coroutine(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g
    return inner


class BlaBlaException(Exception):
    pass


@coroutine
def subgen():
    while True:
        try:
            message = yield
        except BlaBlaException:
            break
        else:
            print("...........", message)


@coroutine
def delegator(g):
    while True:
        try:
            data = yield
            g.send(data)
        except BlaBlaException as e:
            g.throw(e)


"""
$ python -i g_del.py
>>> sg = subgen()
>>> g = delegator(sg)
>>> g.send('Ok')
........... Ok
>>> g.throw(BlaBlaException)
Ku-ku!!!
>>>

"""


@coroutine
def delegator1(g):
    # while True:
    #     try:
    #         data = yield
    #         g.send(data)
    #     except BlaBlaException as e:
    #         g.throw(e)
    yield from g


"""
$ python -i g_del.py
>>> sg = subgen()
>>> g = delegator1(sg)
>>> g.send('ok')
........... ok
>>> g.send(234)
........... 234
>>> g.throw(BlaBlaException)
Ku-ku!!!
>>>

"""


@coroutine
def subgen1():
    while True:
        try:
            message = yield
        except StopIteration:
            break
        else:
            print("...........", message)

    return "Returned from subgen()"


@coroutine
def delegator2(g):
    # while True:
    #     try:
    #         data = yield
    #         g.send(data)
    #     except BlaBlaException as e:
    #         g.throw(e)
    result = yield from g
    print(result)


"""
$ python -i g_del.py
>>> g = delegator2(subgen1())
........... None
>>> g.throw(StopIteration)
Returned from subgen()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration

"""
