from typing import Callable, Optional, Any
import copy


def from_list(lst: list[Optional[int]]) -> Any:
    """
    Convert list to dynamic array
    :param lst:
    :return: a DynamicArray
    """
    dynamic_array = DynamicArray(lst.__len__())
    for i in lst:
        dynamic_array.add(i)
    return dynamic_array


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
        self.__chunk: list[Optional[int]] = [None] * self.__capacity
        self.__index = -1

    def copy(self) -> 'DynamicArray':
        """
        Make a copy of self
        :return:
        """
        new_dynamic = copy.deepcopy(self)
        return new_dynamic

    def to_list(self) -> list[Optional[int]]:
        """ Transform the array to a list """
        return [self.__chunk[i] for i in range(self.__size)]

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

    def map(self, function: Callable[..., int], *iters: tuple['DynamicArray', ...]) -> None:
        """ Applied function to every item of instances of DynamicArray,
         yielding the results. If additional instance arguments are passed,
         function must take that many arguments and is applied to the items
         from all instances in parallel. With multiple instances, the map
         stops when the shortest instance is exhausted.
         """
        if self.__size == 0:
            pass
        if len(iters) > 0:
            i = 0
            for args in zip(*iters):
                if i < self.__size:
                    self.__chunk[i] = function(self.__chunk[i], *args)
                    i += 1
            if i < self.__size:
                for j in range(self.__size - 1, i - 1, -1):
                    self.remove(j)
        else:
            for i in range(self.__size):
                self.__chunk[i] = function(self.__chunk[i])

    def reduce(self, function: Callable[[Optional[int], Optional[int]], int],
               initial: Optional[int] = None) -> Optional[int]:
        """ Apply function of two arguments cumulatively to the items of the array,
            from left to right, to reduce the array to a single value.

        :param function: Callable.
        :param initial: If the optional initializer is present, it is placed before
            the items of the array in the calculation, and serves as a default
            when the array is empty. If initializer is not given and array
            contains only one item, the first item is returned.
        """
        it = iter(self)
        if initial is None:
            try:
                value = next(it)
            except StopIteration:
                raise TypeError("reduce() of empty sequence with no "
                                "initial value") from None
        else:
            value = initial

        for element in it:
            value = function(value, element)
        return value

    def __add__(self, other: 'DynamicArray') -> 'DynamicArray':
        """ Operator '+' overloading, concat self with other instance of DynamicArray. """
        if type(other) != DynamicArray:
            raise Exception('The type of concatenation is not DynamicArray!')
        for k in other:
            self.add(k)
        return self


ls = [1, 1, 1, None]
