import unittest
from typing import Sequence

from hypothesis import given
import hypothesis.strategies as st
from dynamic_array import iterator, empty_, cons, length, member, reduce
from dynamic_array import remove, to_list, concat, from_list, reverse, find
from dynamic_array import filter, map, DynamicArray


class TestDynamicArray(unittest.TestCase):

    def test_api(self):
        empty = empty_()
        l1 = cons(cons(empty, 1), None)
        l2 = cons(cons(empty, None), 1)

        self.assertEqual(str(empty), "[]")
        self.assertEqual(str(l1), "[1, None]")
        self.assertEqual(str(l2), "[1]")
        self.assertNotEqual(empty, l1)
        self.assertNotEqual(empty, l2)
        self.assertNotEqual(l1, l2)
        self.assertEqual(l1, cons(cons(empty, 1), None))
        self.assertEqual(length(empty), 0)
        self.assertEqual(length(l1), 2)

        self.assertEqual(length(l2), 1)
        self.assertEqual(str(remove(l1, 0)), "[None, None]")
        self.assertRaises(Exception, remove, l2, 1)
        self.assertFalse(member(empty, None))
        self.assertTrue(member(l1, None))
        self.assertTrue(member(l1, 1))
        self.assertFalse(member(l1, 2))
        self.assertEqual(str(l1), "[1, None]")
        self.assertEqual(to_list(l1), [1, None])
        self.assertEqual(to_list(l1), to_list(from_list([1, None])))
        self.assertEqual(to_list(concat(l1, l2)), to_list(from_list([1, 1])))
        buf = []
        for e in l1.iterator():
            buf.append(e)
        self.assertEqual(buf, [1])
        lst = to_list(l2) + to_list(l1)
        for e in l1.iterator():
            lst.remove(e)
        for e in l2.iterator():
            lst.remove(e)
        self.assertEqual(lst, [None])

    @given(st.lists(st.integers()))
    def test_length(self, a):
        b = from_list(a)
        self.assertEqual(length(b), len(a))

    def test_reverse(self):
        a = [2, 4, 1, 4, 9]
        b = from_list(a)
        self.assertEqual(str(reverse(b)), '[9, 4, 1, 4, 2]')

    @given(st.lists(st.integers()))
    def test_from_list_to_list_equality(self, a) -> None:
        self.assertEqual(to_list(from_list(a)), a)

    def test_find(self) -> None:
        a: Sequence = [2, 4, 4, 9, 5]
        arr = from_list(a)
        self.assertEqual([], find(arr, lambda x: x is None))
        self.assertEqual([9], find(arr, lambda x: x % 3 == 0))
        self.assertEqual([2, 4, 4, 5], find(arr, lambda x: x % 3 != 0))
        self.assertEqual([9], find(arr, lambda x: x == 9))

    @given(st.lists(st.integers()))
    def test_filter(self, a: Sequence) -> None:
        from builtins import filter as gt_filter
        arr = from_list(a)
        result = list(gt_filter(lambda x: x % 3 == 0, a))
        self.assertEqual(to_list(filter(arr, lambda x: x % 3 == 0)), result)
        result = list(gt_filter(lambda x: x % 3 != 0, a))
        self.assertEqual(to_list(filter(arr, lambda x: x % 3 != 0)), result)

    @given(st.lists(st.integers()))
    def test_map(self, a: Sequence):
        from builtins import map as gt_map
        arr1: 'DynamicArray' = from_list(a)
        result = list(gt_map(lambda x: x ** 3, a))
        self.assertEqual(to_list(map(arr1, lambda x: x ** 3)), result)

    @given(st.lists(st.integers()), st.integers())
    def test_reduce(self, a: Sequence, b: int):
        arr = from_list(a)
        if arr.length() == 0:
            self.assertEqual(b, reduce(arr, lambda x, y: x + y, b))
        else:
            from functools import reduce as gt_reduce
            result = gt_reduce(lambda x, y: x + y, a, b)
            self.assertEqual(reduce(arr, lambda x, y: x + y, b), result)
            result = gt_reduce(lambda x, y: x + y, a, b)
            self.assertEqual(reduce(arr, lambda x, y: x + y, b), result)

    def test_iterator(self):
        x: Sequence = [2, 4, 6]
        arr = from_list(x)
        t = []
        try:
            i = iterator(arr)
            while i.hasNext():
                t.append(i.__next__())
        except StopIteration:
            pass
        self.assertEqual(x, t)
        self.assertEqual(to_list(arr), t)
        i = empty_().iterator()
        self.assertRaises(StopIteration, lambda: next(i))

    def test_empty(self) -> None:
        a = empty_()
        b = from_list([])
        self.assertEqual(a, b)

    @given(st.lists(st.integers()),
           st.lists(st.integers()),
           st.lists(st.integers()))
    def test_monoid(self, a: Sequence, b: Sequence, c: Sequence):
        arr1 = from_list(a)
        arr2 = from_list(b)
        arr3 = from_list(c)
        self.assertEqual(to_list(concat(concat(arr1, arr2), arr3)),
                         to_list(concat(arr1, concat(arr2, arr3))))

    @given(st.lists(st.integers()))
    def test_monoid_identity(self, lst: Sequence):
        a = from_list(lst)
        self.assertEqual(concat(empty_(), a), a)
        self.assertEqual(concat(a, empty_()), a)


if __name__ == '__main__':
    unittest.main()
