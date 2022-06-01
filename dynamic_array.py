from typing import Callable, Optional, List
from typing import Union

UnionList = Union[List[Optional[int]], List[int]]


class DArrayIterator(object):

    def __init__(self, lst: List[Optional[int]], array_size: int):
        self.__index = -1
        self.__chunk: List[Optional[int]] = lst
        self.__size = array_size

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

    def __init__(self, lst: List[Optional[int]] = None, capacity: int = -1,
                 grow_factor: int = 2):
        """
        Dynamic array initialization
        :param capacity: size of elements that can be included
        :param grow_factor:  the capacity expansion ratio
        when the capacity of the dynamic array is insufficient each time
        """
        self.__grow_factor = grow_factor
        self.__size = 0
        self.__capacity = 0
        self.__chunk: List[Optional[int]] = []
        if lst is not None:
            self.__size = lst.__len__()
            if capacity == -1:
                capacity = lst.__len__()
            self.__capacity = capacity
            self.__chunk = lst

    def __eq__(self, other: object) -> bool:
        """
        Return True if those tow DynamicArray is equal
        All built-in properties should be equal
        """
        if not isinstance(other, DynamicArray):
            return NotImplemented
        if self.size() != size(other) or self.__capacity != other.__capacity:
            return False
        for a, b in zip(self.__chunk, other.__chunk):
            if a != b:
                return False
        return True

    def __str__(self) -> str:
        """Return description information"""
        return str(to_list(self))

    def __iter__(self):
        """
        According to the built-in list chunk convert a dynamic array to
        an iterator
        """
        return DArrayIterator(self.__chunk, self.__size)

    def grow_factor(self) -> int:
        """ return grow_factor of DynamicArray """
        return self.__grow_factor

    def size(self) -> int:
        """ return the size of DynamicArray """
        return self.__size

    def capacity(self) -> int:
        """ return the capacity of DynamicArray """
        return self.__capacity

    def getByIndex(self, pos: int) -> Optional[int]:
        """ get element by index """
        return self.__chunk[pos]

    def member(self, element) -> bool:
        """ return ture if DynamicArray contain element """
        return self.__chunk.__contains__(element)


def to_list(self, index: int = 0) -> List[Optional[int]]:
    """
    Transform the array to a list
    Transform object: __chunk
    """
    lst: List[Optional[int]] = []
    while index < self.size():
        lst.append(self.getByIndex(index))
        index += 1
    return lst


def from_list(lst: Optional[List[Optional[int]]]) -> 'DynamicArray':
    """
    Convert list to dynamic array
    :param lst:
    :return: a DynamicArray
    """
    return DynamicArray(lst)


def cons(element: Optional[int], self: 'DynamicArray') -> 'DynamicArray':
    """
    Add an element at the end of the array
    If the dynamic array in condition (size=capacity)
        Expand capacity
        Add element from tail
    """
    res: List[Optional[int]] = []
    for i in self:
        res.append(i)
    res.append(element)
    new_capacity: int = self.capacity()
    if self.size() == self.capacity():
        new_capacity = new_capacity * self.grow_factor() \
            if self.size() > 0 else 1
    new_dynamic = DynamicArray(res, new_capacity, self.grow_factor())
    return new_dynamic


def concat(dynamic_array1: 'DynamicArray', dynamic_array2: 'DynamicArray') \
        -> 'DynamicArray':
    """ Merge two dynamic arrays """
    res: List[Optional[int]] = []
    for i in dynamic_array1:
        res.append(i)
    for i in dynamic_array2:
        res.append(i)
    new_capacity: int = dynamic_array1.size() + dynamic_array2.size()
    new_dynamic = DynamicArray(res, new_capacity, dynamic_array1.grow_factor())
    return new_dynamic


def remove(self: 'DynamicArray', pos: int) -> 'DynamicArray':
    """
    Remove an element of array at specified position
    Starting from the position of the element to be deleted,
    it is overwritten with the value at POS + 1 in sequence
    :param self:
    :param pos: Index of the array
    """
    res: List[Optional[int]] = []
    if pos < 0 or pos >= self.size():
        raise Exception('Out of the index')
    for i in self:
        res.append(i)
    res.pop(pos)
    return DynamicArray(res, self.capacity(), self.grow_factor())


def length(self: 'DynamicArray') -> int:
    """ Return the capacity of array """
    return self.capacity()


def size(self) -> int:
    """ Return the size of array """
    return self.size()


def member(value: Optional[int], self: 'DynamicArray') -> bool:
    """
    Determines whether the given value is a member of the array
    :param self:
    :param value: The given value.
    :return: Value is member if return True, else not.
    """
    return self.member(value)


def reverse(self: 'DynamicArray') -> 'DynamicArray':
    """
    Reverse the elements in the array
    Only element in the array is not None will be reverse
    """
    res: List[Optional[int]] = []
    index = self.size() - 1
    while index > -1:
        res.append(self.getByIndex(index))
        index -= 1
    return DynamicArray(res, self.capacity(), self.grow_factor())


def filter_(self: 'DynamicArray', predicate: Callable[[Optional[int]],
                                                      bool]) -> 'DynamicArray':
    """
    Filter the array by specific predicate
    :param self:
    :param predicate: Screening conditions -> bool
    :return: A DynamicArray remove all element not fit predicate in order
    """
    res: List[Optional[int]] = []
    for i in self:
        if predicate(i):
            res.append(i)
    return DynamicArray(res, self.capacity(), self.grow_factor())


def map_(self: 'DynamicArray', function: Callable[[Optional[int]],
                                                  int]) -> 'DynamicArray':
    """
    Applies a function to each element in a dynamic array
    :param self: DynamicArray
    :param function: The function used to manipulate each element
    :return: A new DynamicArray
    """
    res: List[Optional[int]] = []
    for i in self:
        res.append(function(i))
    return DynamicArray(res, self.capacity(), self.grow_factor())


def reduce(self, function: Callable[[int, Optional[int]], int],
           initial_state: int = 0) -> int:
    """
    Apply function of two arguments cumulatively to the items of the array,
    from left to right, to reduce the array to a single value
    """
    state = initial_state
    if self.size() == 0:
        return state
    for element in self:
        state = function(state, element)
    return state


def find(self: 'DynamicArray', p: Callable[[Optional[int]], bool]) \
        -> List[int]:
    """
    find all element in the dynamic array in condition p
    :param self:
    :param p: Screening conditions
    :return: a list contain all element in condition p
    """
    lst: List[int] = []
    for k in self:
        if p(k):
            lst.append(k)
    return lst


def empty_() -> 'DynamicArray':
    """Get a monoid dynamic array"""
    return DynamicArray()


def next(self: 'DArrayIterator') -> Optional[int]:
    """
    External functions for __next__() in DArrayIterator use in unit testing
    """
    return self.__next__()
