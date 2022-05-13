from typing import Callable, Optional, Any, List
import copy


def from_list(lst: List[Optional[int]]) -> Any:
    """
    Convert list to dynamic array
    :param lst:
    :return: a DynamicArray
    """
    dynamic_array = DynamicArray(lst.__len__())
    for i in lst:
        dynamic_array.add(i)
    return dynamic_array


def concat(dynamic_array1: 'DynamicArray', dynamic_array2: 'DynamicArray') -> 'DynamicArray':
    """ Merge two dynamic arrays """
    new_dynamic = DynamicArray(dynamic_array1.size() + dynamic_array2.size())
    for i in dynamic_array1.to_list():
        new_dynamic.add(i)
    for k in dynamic_array2.to_list():
        dynamic_array1.add(k)
    return new_dynamic


class DArrayIterator:

    def __init__(self, lst: List[int]):
        self.__index = -1
        self.__chunk = lst
        self.__size = lst.__len__()

    def hasNext(self) -> bool:
        """Determine whether the iterator still has elements"""
        return self.__index < self.__size - 1

    def next(self) -> Optional[int]:
        """
        Returns the current element of the iterator
        :return:current element
        """
        if self.__index > self.__size - 2:
            return None
        self.__index += 1
        return self.__chunk[self.__index]


class DynamicArray(object):

    def __init__(self, capacity: int, grow_factor: int = 2):
        """
        Dynamic array initialization
        :param capacity: size of elements that can be included
        :param grow_factor:  the capacity expansion ratio
        when the capacity of the dynamic array is insufficient each time
        """
        self.__grow_factor = grow_factor
        self.__size = 0
        self.__capacity = capacity
        self.__chunk: List[Optional[int]] = [None] * self.__capacity

    def to_iterator(self) -> 'DArrayIterator':
        """
        Convert a dynamic array to an iterator
        :return: an iterator
        """
        return DArrayIterator(self.__chunk)

    def copy(self) -> 'DynamicArray':
        """
        Make a copy of self
        :return:
        """
        new_dynamic = copy.deepcopy(self)
        return new_dynamic

    def to_list(self) -> List[int]:
        """ Transform the array to a list """
        lst: List[int] = []
        for i in self.__chunk:
            if i is not None:
                lst.append(i)
            else:
                break
        return lst

    def add(self, element: Optional[int]) -> 'DynamicArray':
        """ Add an element at the end of the array"""
        new_dynamic = self.copy()
        if new_dynamic.__size == new_dynamic.__capacity:
            new_dynamic.__capacity = new_dynamic.__capacity * new_dynamic.__grow_factor
            new_dynamic.__chunk += [None] * (new_dynamic.__capacity - self.__capacity)
        if element is None:
            pass
        else:
            new_dynamic.__chunk[new_dynamic.__size] = element
        new_dynamic.__size += 1
        return new_dynamic

    def set(self, pos: int, value: Optional[int]) -> 'DynamicArray':
        """ Add an element into the array at specified position
        :param pos: Index of the array
        :param value: The value of element, int or None
        """
        if pos < 0 or pos >= self.__size:
            raise Exception('Out of the index')
        new_dynamic = self.copy()
        new_dynamic.__chunk[pos] = value
        return new_dynamic

    def remove(self, pos: int) -> 'DynamicArray':
        """ Remove an element of array at specified position
        :param pos: Index of the array
        """
        new_dynamic = self.copy()
        if pos < 0 or pos >= self.__size:
            raise Exception('Out of the index')
        while pos < self.__size - 1:
            new_dynamic.__chunk[pos] = new_dynamic.__chunk[pos + 1]
            pos += 1
        new_dynamic.__chunk[pos] = None
        new_dynamic.__size -= 1
        return new_dynamic

    def size(self) -> int:
        """ Return the length of array. """
        return self.__size

    def member(self, value: int) -> bool:
        """ Determines whether the given value is a member of the array.

        :param value: The given value.
        :return: Value is member if return True, else not.
        """
        return self.__chunk.__contains__(value)

    def reverse(self) -> 'DynamicArray':
        """ Reverse the array. """
        new_dynamic = copy.deepcopy(self)
        left = 0
        right = self.__size - 1
        while left < right:
            t = new_dynamic.__chunk[right]
            new_dynamic.__chunk[right] = new_dynamic.__chunk[left]
            new_dynamic.__chunk[left] = t
            right -= 1
            left += 1
        return new_dynamic

    def filter(self, predicate: Callable[[Optional[int]], bool]) -> 'DynamicArray':
        """ Filter the array by specific predicate. """
        new_dynamic = copy.deepcopy(self)
        for i in range(new_dynamic.__size - 1, -1, -1):
            if not predicate(new_dynamic.__chunk[i]):
                new_dynamic.remove(i)
        return new_dynamic

    def map(self, function: Callable[[Any], int]) -> 'DynamicArray':
        """ Applies a function to each element in a dynamic array"""
        new_dynamic = copy.deepcopy(self)
        i = 0
        while i < new_dynamic.size():
            new_dynamic.__chunk[i] = function(new_dynamic.__chunk[i])
        return new_dynamic

    def reduce(self, function: Callable[[Optional[int], Optional[int]], int],
               initial_state: Optional[int] = None) -> Optional[int]:
        """ Apply function of two arguments cumulatively to the items of the array,
            from left to right, to reduce the array to a single value.
        """
        if self.size() == 0:
            return None
        state = initial_state
        for element in self.__chunk:
            if element is not None:
                state = function(state, element)
            else:
                break
        return state


ls = [1, 1, 1, None, 5, 8, 7, 1]
print(ls.__sizeof__())
