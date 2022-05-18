from typing import Callable, Optional, Any, List, Sequence
import copy


class DArrayIterator(object):

    def __init__(self, lst: List[Optional[int]]):
        self.__index = -1
        self.__chunk: List[int] = []
        for i in lst:
            if i is not None:
                self.__chunk += [i]
        self.__size = self.__chunk.__len__()

    def hasNext(self) -> bool:
        """Determine whether the iterator still has elements"""
        return self.__index < self.__size - 1

    def __next__(self) -> Optional[int]:
        """
        Returns the current element of the iterator
        :return:current element
        """
        if self.__index > self.__size - 2:
            raise StopIteration
        self.__index += 1
        return self.__chunk[self.__index]

    def __iter__(self) -> 'DArrayIterator':
        return self


class DynamicArray(object):
    """Implementation of immutable dynamic array"""

    def __init__(self, capacity: int = 0, grow_factor: int = 2):
        """
        Dynamic array initialization
        :param capacity: size of elements that can be included
        :param grow_factor:  the capacity expansion ratio
        when the capacity of the dynamic array is insufficient each time
        """
        if capacity < 0:
            raise ImportError("Bad capacity: " +
                              str(capacity) + "<0,but should >0")
        self.__grow_factor = grow_factor
        self.__size = 0
        self.__capacity = capacity
        self.__chunk: List[Optional[int]] = [None] * self.__capacity

    def iterator(self) -> 'DArrayIterator':
        """
        According to the built-in list chunk convert a dynamic array to
        an iterator
        :return: an iterator
        """
        return DArrayIterator(self.__chunk)

    def to_list(self) -> List[Optional[int]]:
        """
        Transform the array to a list
        Transform object: __chunk
        Only value is not None will be use
        """
        lst: List[Optional[int]] = []
        for i in self.__chunk:
            lst.append(i)
        return lst

    def cons(self, element: Optional[int]) -> 'DynamicArray':
        """
        Add an element at the end of the array
        If the element is None, it means expand capacity:
            capacity+=1
        If the dynamic array in condition (size=capacity)
            Expand capacity
            Add element from tail
        """
        new_dynamic = copy.deepcopy(self)
        if new_dynamic.__size == new_dynamic.__capacity:
            if new_dynamic.__capacity > 0:
                new_dynamic.__capacity *= new_dynamic.__grow_factor
                new_dynamic.__chunk += [None] * (new_dynamic.__capacity -
                                                 self.__capacity)
            elif new_dynamic.__capacity == 0:
                new_dynamic.__capacity = 1
                new_dynamic.__chunk += [None] * (new_dynamic.__capacity -
                                                 self.__capacity)
            else:
                raise IndexError("Bad capacity: " +
                                 str(self.__capacity) + "<0")
        if element is None:
            pass
        else:
            new_dynamic.__chunk[new_dynamic.__size] = element
            new_dynamic.__size += 1
        return new_dynamic

    def remove(self, pos: int) -> 'DynamicArray':
        """
        Remove an element of array at specified position
        Starting from the position of the element to be deleted,
        it is overwritten with the value at POS + 1 in sequence
        :param pos: Index of the array
        """
        new_dynamic = copy.deepcopy(self)
        if pos < 0 or pos >= self.__size:
            raise Exception('Out of the index')
        while pos < self.__size - 1:
            new_dynamic.__chunk[pos] = new_dynamic.__chunk[pos + 1]
            pos += 1
        new_dynamic.__chunk[pos] = None
        new_dynamic.__size -= 1
        return new_dynamic

    def length(self) -> int:
        """ Return the capacity of array """
        return self.__capacity

    def size(self) -> int:
        """ Return the size of array """
        return self.__size

    def member(self, value: Optional[int]) -> bool:
        """
        Determines whether the given value is a member of the array
        :param value: The given value.
        :return: Value is member if return True, else not.
        """
        return self.__chunk.__contains__(value)

    def reverse(self) -> 'DynamicArray':
        """
        Reverse the elements in the array
        Only element in the array is not None will be reverse
        """
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

    def filter(self, predicate: Callable[[Optional[int]],
                                         bool]) -> 'DynamicArray':
        """
        Filter the array by specific predicate
        :param predicate: Screening conditions -> bool
        :return: A DynamicArray remove all element not fit predicate in order
        """
        res: List[Optional[int]] = []
        for i in self.iterator():
            if predicate(i):
                res.append(i)
        return from_list(res)

    def map(self, function: Callable[[Optional[int]], int]) -> 'DynamicArray':
        """
        Applies a function to each element in a dynamic array
        :param function: The function used to manipulate each element
        :return: A new DynamicArray
        """
        if self.size() == 0:
            return self
        new_dynamic = DynamicArray(self.__size)
        for i in self.iterator():
            new_dynamic = new_dynamic.cons(function(i))
        new_dynamic.__chunk += [None] * (self.__capacity - self.__size)
        new_dynamic.__capacity = self.__capacity
        return new_dynamic

    def reduce(self, function: Callable[[int, int], int],
               initial_state: int = 0) -> int:
        """
        Apply function of two arguments cumulatively to the items of the array,
        from left to right, to reduce the array to a single value
        """
        state = initial_state
        if self.size() == 0:
            return state
        for element in self.__chunk:
            if not isinstance(element, int):
                raise StopIteration("element must be int")
            state = function(state, element)
        return state

    def find(self, p: Callable[[int], bool]) -> Sequence:
        """
        find all element in the dynamic array in condition p
        :param p: Screening conditions
        :return: a list contain all element in condition p
        """
        lst: List[int] = []
        for k in self.__chunk:
            if not isinstance(k, int):
                raise StopIteration("element must be int")
            if p(k):
                lst.append(k)
        return lst

    def __eq__(self, other: object) -> bool:
        """
        Return True if those tow DynamicArray is equal
        All built-in properties should be equal
        """
        if not isinstance(other, DynamicArray):
            return NotImplemented
        if self.__size != other.size() or self.__capacity != other.__capacity:
            return False
        for a, b in zip(self.__chunk, other.__chunk):
            if a != b:
                return False
        return True

    def __str__(self):
        """Return description information"""
        return str(self.to_list())


def from_list(lst: Sequence) -> 'DynamicArray':
    """
    Convert list to dynamic array
    :param lst:
    :return: a DynamicArray
    """
    dynamic_array = DynamicArray(lst.__len__())
    for i in lst:
        dynamic_array = dynamic_array.cons(i)
    return dynamic_array


def concat(dynamic_array1: 'DynamicArray', dynamic_array2: 'DynamicArray') \
        -> 'DynamicArray':
    """ Merge two dynamic arrays """
    new_size = dynamic_array1.size() + dynamic_array2.size()
    new_dynamic = DynamicArray(new_size)
    for i in dynamic_array1.to_list():
        if i is not None:
            new_dynamic = new_dynamic.cons(i)
        else:
            break
    for k in dynamic_array2.to_list():
        if k is not None:
            new_dynamic = new_dynamic.cons(k)
        else:
            break
    return new_dynamic


def empty_() -> 'DynamicArray':
    """Get a monoid dynamic array"""
    return DynamicArray()


def iterator(self: 'DynamicArray') -> 'DArrayIterator':
    """
    External functions for iterator() use in unit testing
    """
    return self.iterator()


def to_list(self: 'DynamicArray') -> List[Optional[int]]:
    """
    External functions for to_list() use in unit testing
    """
    return self.to_list()


def cons(self: 'DynamicArray', element: Optional[int]) -> 'DynamicArray':
    """
    External functions for cons() use in unit testing
    """
    return self.cons(element)


def remove(self: 'DynamicArray', pos: int) -> 'DynamicArray':
    """
    External functions for remove() use in unit testing
    """
    return self.remove(pos)


def length(self: 'DynamicArray') -> int:
    """
    External functions for size() use in unit testing
    """
    return self.length()


def member(self: 'DynamicArray', value: Optional[int]) -> bool:
    """ Determines whether the given value is a member of the array"""
    return self.member(value)


def reverse(self: 'DynamicArray') -> 'DynamicArray':
    """
    External functions for reverse() use in unit testing
    """
    return self.reverse()


def filter(self: 'DynamicArray', predicate: Callable[[Optional[int]],
                                                     bool]) -> 'DynamicArray':
    """
    External functions for filter() use in unit testing
    """
    return self.filter(predicate)


def map(self: 'DynamicArray', function: Callable[[Any], int]) \
        -> 'DynamicArray':
    """
    External functions for map() use in unit testing
    """
    return self.map(function)


def reduce(self: 'DynamicArray', function: Callable[[int,
                                                     int], int],
           initial_state: int = 0) -> int:
    """
    External functions for reduce() use in unit testing
    """
    return self.reduce(function, initial_state)


def find(self: 'DynamicArray', p: Callable[[int], bool]) \
        -> Sequence:
    """
    External functions for find() use in unit testing
    """
    return self.find(p)


def next(self: 'DArrayIterator') -> Optional[int]:
    """
    External functions for __next__() in DArrayIterator use in unit testing
    """
    return self.__next__()
