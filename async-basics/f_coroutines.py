
def coroutine(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g
    return inner


def subgen():
    x = 'Ready to accept message'
    message = yield x
    print('Subgen received: ', message)


class BlaBlaException(Exception):
    pass


@coroutine
def average():
    count = 0
    sum_num = 0
    avg = None

    while True:
        try:
            x = yield avg

        except StopIteration:
            print('Done')
            break

        except BlaBlaException:
            print('...............................')
            break

        else:
            count += 1
            sum_num += x
            avg = round(sum_num / count)

    return avg
