import unittest
from typing import List, Optional

from hypothesis import given
import hypothesis.strategies as st
from dynamic_array import empty_, cons, length, member, reduce
from dynamic_array import remove, to_list, concat, from_list, reverse, find
from dynamic_array import DynamicArray, filter_, map_


class TestDynamicArray(unittest.TestCase):

    def test_api(self) -> None:
        empty = empty_()
        l1 = cons(None, cons(1, empty))
        l2 = cons(1, cons(None, empty))
        # TODO: conj to add elements to the end
        self.assertEqual(str(empty), "[]")
        self.assertEqual(str(l1), "[1, None]")
        self.assertEqual(str(l2), "[None, 1]")
        self.assertNotEqual(empty, l1)
        self.assertNotEqual(empty, l2)
        self.assertNotEqual(l1, l2)
        self.assertEqual(l1, cons(None, cons(1, empty)))

        self.assertEqual(length(empty), 0)
        self.assertEqual(length(l1), 2)
        self.assertEqual(length(l2), 2)
        self.assertEqual(str(remove(l1, 0)), "[None]")
        self.assertEqual(str(remove(l1, 1)), "[1]")
        self.assertFalse(member(None, empty))
        self.assertTrue(member(None, l1))
        self.assertTrue(member(1, l1))
        self.assertFalse(member(2, l1))
        self.assertEqual(l1, reverse(l2))
        self.assertEqual(to_list(l1), [1, None])
        self.assertEqual(l1, from_list([1, None]))
        self.assertEqual(concat(l1, l2), from_list([1, None, None, 1]))
        buf = []
        for e in l1:
            buf.append(e)
        self.assertEqual(buf, [1, None])
        lst = to_list(l1) + to_list(l2)
        for e in l1:
            lst.remove(e)
        for e in l2:
            lst.remove(e)
        self.assertEqual(lst, [])

    @given(st.lists(st.integers()))
    def test_length(self, a: List[Optional[int]]) -> None:
        b = from_list(a)
        self.assertEqual(length(b), len(a))

    def test_reverse(self) -> None:
        a: List[Optional[int]] = [2, 4, 1, 4, 9]
        b = from_list(a)
        self.assertEqual(str(reverse(b)), '[9, 4, 1, 4, 2]')

    @given(st.lists(st.integers()))
    def test_from_list_to_list_equality(
            self, a: List[Optional[int]]) -> None:
        self.assertEqual(to_list(from_list(a)), a)

    def test_find(self) -> None:
        a: List[Optional[int]] = [2, 4, 4, 9, 5]
        arr = from_list(a)
        self.assertEqual(
            [9],
            find(arr, lambda x: (x % 3 == 0) if x is not None else False))
        self.assertEqual(
            [2, 4, 4, 5],
            find(arr, lambda x: (x % 3 != 0) if x is not None else False))
        self.assertEqual(
            [9],
            find(arr, lambda x: (x == 9) if x is not None else False))

    @given(st.lists(st.integers()))
    def test_filter(self, a: List[Optional[int]]) -> None:
        from builtins import filter as gt_filter
        arr = from_list(a)
        result = list(gt_filter(
            lambda x: x % 3 == 0 if x is not None else False, a))
        self.assertEqual(
            to_list(filter_(
                arr,
                lambda x: (x % 3 == 0) if x is not None else False)),
            result)
        result = list(gt_filter(
            lambda x: x % 3 != 0 if x is not None else False, a))
        self.assertEqual(
            to_list(filter_(
                arr,
                lambda x: (x % 3 != 0) if x is not None else False)),
            result)

    @given(st.lists(st.integers()))
    def test_map(self, a: List[Optional[int]]) -> None:
        from builtins import map as gt_map
        arr1: 'DynamicArray' = from_list(a)
        result = list(gt_map(lambda x: x ** 3 if x is not None else x, a))
        self.assertEqual(
            to_list(map_(
                arr1, lambda x: x ** 3 if x is not None else x)), result)

    @given(st.lists(st.integers()), st.integers())
    def test_reduce(self, a: List[Optional[int]], b: int) -> None:
        arr = from_list(a)
        if length(arr) == 0:
            self.assertEqual(
                b, reduce(
                    arr, lambda x, y: (x + y) if y is not None else 1, b))
        else:
            from functools import reduce as gt_reduce
            result = gt_reduce(
                lambda x, y: x + y if y is not None else x + 1, a, b)
            self.assertEqual(reduce(
                arr,
                lambda x, y: (x + y) if y is not None else x + 1, b), result)
            result = gt_reduce(
                lambda x, y: x + y if y is not None else x + 1, a, b)
            self.assertEqual(reduce(
                arr,
                lambda x, y: (x + y) if y is not None else x + 1, b), result)

    def test_empty(self) -> None:
        a = empty_()
        k: List[Optional[int]] = []
        b = from_list(k)
        self.assertEqual(a, b)

    @given(st.lists(st.integers()),
           st.lists(st.integers()),
           st.lists(st.integers()))
    def test_monoid(self, a: List[Optional[int]], b: List[Optional[int]],
                    c: List[Optional[int]]) -> None:
        arr1 = from_list(a)
        arr2 = from_list(b)
        arr3 = from_list(c)
        self.assertEqual(to_list(concat(concat(arr1, arr2), arr3)),
                         to_list(concat(arr1, concat(arr2, arr3))))

    @given(st.lists(st.integers()))
    def test_monoid_identity(self, lst: List[Optional[int]]) -> None:
        a = from_list(lst)
        self.assertEqual(concat(empty_(), a), a)
        self.assertEqual(concat(a, empty_()), a)

    @given(st.lists(st.integers()))
    def test_immutability(self, lst: List[Optional[int]]) -> None:
        a = from_list(lst)
        # do some operations
        cons(22, a)
        reverse(a)
        self.assertEqual(str(a), str(lst))


if __name__ == '__main__':
    unittest.main()
