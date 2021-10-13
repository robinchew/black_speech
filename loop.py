from functools import partial
from itertools import tee, chain, islice, zip_longest

def num_items_per_loop(num, some_iterable):
    return zip_longest(
        *[chain(islice(new_iter, i, None)) for i, new_iter in enumerate(tee(some_iterable, num))])

END = 'END'
NONE_TYPE = {
    'type': 'ignore',
}

def chunk_at_a_time(chunk_size, iterable, three_items = tuple(), new_iterable = tuple(), count = 0):
    new_three = tuple(item for i, item in zip(range(chunk_size), three_items))

    #new_three = new_three + tuple(nxt(iterable)
    for i in range(chunk_size - len(new_three)):
        try:
            got = next(iterable)
        except StopIteration:
            yield new_three + (NONE_TYPE,)
            yield new_three[1:] + (NONE_TYPE, NONE_TYPE)
            return
        new_three += (got,)

    yield new_three

    first, *rest = new_three

    yield from chunk_at_a_time(chunk_size, iterable, tuple(rest), new_iterable + (first,), count + 1)

two_at_a_time = partial(chunk_at_a_time, 2)
three_at_a_time = partial(chunk_at_a_time, 3)
four_at_a_time = partial(chunk_at_a_time, 4)

"""
for item in three_at_a_time(iter(range(20))):
    print('it', item)
"""
