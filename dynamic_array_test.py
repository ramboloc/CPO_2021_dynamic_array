import unittest
from hypothesis import given
import hypothesis.strategies as st
from typing import Any, List
from dynamic_array import DynamicArray,DArrayIterator


class TestDynamicArray(unittest.TestCase):

    def test_api(self) -> None:
        test_array=DynamicArray(10)




