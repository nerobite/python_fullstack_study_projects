"""
Написать итератор, аналогичный итератору из задания 1, но обрабатывающий списки с любым уровнем вложенности.
"""

class FlatIterator:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        self.index = 0

    def __iter__(self):
        self.list_ = self.get_files_list(self.list_of_list)
        return self

    def __next__(self):
        if self.index < len(self.list_):
            item = self.list_[self.index]
            self.index += 1
            return item
        else:
            raise StopIteration

    def get_files_list(self, lst = None):
        result = []
        if lst is None:
            lst = self.list_of_list
        for item in lst:
            if isinstance(item, list):
                result.extend(self.get_files_list(item))
            else:
                result.append(item)
        return result


def test_3():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']


if __name__ == '__main__':
    test_3()
