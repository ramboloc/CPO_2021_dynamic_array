import unittest
from hypothesis import given
import hypothesis.strategies as st
from typing import Any, List
from dynamic_array import *


class TestDynamicArray(unittest.TestCase):

    def test_api(self):
        empty = DynamicArray(0)

        l1 = empty.cons(1).cons(None)
        l2 = empty.cons(None)
        self.assertEqual(str(empty), "[]")
        self.assertEqual(str(l1), "[1, None]")
        self.assertEqual(str(l2), "[None, 1]")
        self.assertNotEqual(empty, l1)
        self.assertNotEqual(empty, l2)
        self.assertNotEqual(l1, l2)
        self.assertEqual(l1, cons(cons(empty, 1), None))
        self.assertEqual(length(empty), 0)
        self.assertEqual(length(l1), 2)

        self.assertEqual(length(l2), 2)
        self.assertEqual(str(remove(l1, 0)), "[None]")
        self.assertEqual(str(remove(l1, 1)), "[1]")
        self.assertFalse(member(empty, None))
        self.assertTrue(member(l1, None))
        self.assertTrue(member(l1, 1))
        self.assertFalse(member(l1, 2))
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

    def test_intersection(self):
        empty = DynamicArray()

        l1 = cons(cons(empty, 1), None)
        l2 = cons(cons(empty, 2), 1)

        self.assertEqual(str(intersection(l1, 0, None)), '[None, None]')
        self.assertEqual(str(intersection(l2, 1, 3)), '[2, 3]')

    @given(st.lists(st.integers()))
    def test_length(self, a):
        b = from_list(a)
        self.assertEqual(length(b), len(a))

    def test_reverse(self):
        a = [2, 4, None, 4, 9]
        b = from_list(a)
        self.assertEqual(str(reverse(b)), '[9, 4, None, 4, 2]')

    @given(st.lists(st.integers()))
    def test_from_list_to_list_equality(self, a):
        self.assertEqual(to_list(from_list(a)), a)

    def test_find(self):
        a = [2, 4, None, 4, 9]
        self.assertTrue(find(a, lambda x: x is None))
        self.assertTrue(find(a, lambda x: x % 3 == 0))
        self.assertTrue(find(a, lambda x: x % 3 != 0))
        self.assertFalse(find(a, lambda x: x == 9))

    @given(st.lists(st.integers()))
    def test_filter(self, a):
        from builtins import filter as gt_filter
        arr = from_list(a)
        result = list(gt_filter(lambda x: x % 3 == 0, a))
        self.assertEqual(to_list(filter(lambda x: x % 3 == 0, arr)), result)
        result = list(gt_filter(lambda x: x % 3 != 0, a))
        self.assertEqual(to_list(filter(lambda x: x % 3 != 0, arr)), result)

    @given(st.lists(st.integers()),
           st.lists(st.integers()),
           st.lists(st.integers()))
    def test_map(self, a, b, c):
        from builtins import map as gt_map
        arr1 = from_list(a)
        result = list(gt_map(lambda x: x ** 3, a))
        self.assertEqual(to_list(map(lambda x: x ** 3, arr1)), result)
        result = list(gt_map(lambda x, y: x * y, a, b))
        arr2 = from_list(b)
        self.assertEqual(to_list(map(lambda x, y: x * y, arr1, arr2)), result)
        arr3 = from_list(c)
        result = list(gt_map(lambda x, y, z: x * y - z, a, b, c))
        self.assertEqual(to_list(map(lambda x, y, z: x * y - z, arr1,
                                     arr2, arr3)), result)
        a = [2, 4, 6]
        arr4 = from_list(a)
        b = [0, None, 3]
        arr5 = from_list(b)
        with self.assertRaises(TypeError):
            map(lambda x, y: x + y, arr4, arr5)

    @given(st.lists(st.integers()), st.integers())
    def test_reduce(self, a, b):
        arr = from_list(a)
        if arr.length() == 0:
            self.assertEqual(b, reduce(lambda x, y: x + y, arr, b))
            with self.assertRaises(TypeError):
                reduce(lambda x, y: x + y, arr)
        else:
            from functools import reduce as gt_reduce
            result = gt_reduce(lambda x, y: x + y, a)
            self.assertEqual(reduce(lambda x, y: x + y, arr), result)
            result = gt_reduce(lambda x, y: x + y, a, b)
            self.assertEqual(reduce(lambda x, y: x + y, arr, b), result)

    def test_iterator(self):
        x = [2, 4, 6]
        l = from_list(x)
        t = []
        try:
            i = iterator(l)
            while hasNext(i):
                t.append(next(i))
        except StopIteration:
            pass
        self.assertEqual(x, t)
        self.assertEqual(to_list(l), t)
        i = iterator(empty())
        self.assertRaises(StopIteration, lambda: next(i))

    def test_empty(self):
        a = empty()
        b = from_list([])
        self.assertEqual(a, b)

    @given(st.lists(st.integers()),
           st.lists(st.integers()),
           st.lists(st.integers()))
    def test_monoid(self, a, b, c):
        aa = from_list(a)
        bb = from_list(b)
        cc = from_list(c)
        self.assertEqual(concat(concat(aa, bb), cc),
                         concat(aa, concat(bb, cc)))

    @given(st.lists(st.integers()))
    def test_monoid_identity(self, lst):
        a = from_list(lst)
        self.assertEqual(concat(empty(), a), a)
        self.assertEqual(concat(a, empty()), a)
