# SA Spade A - lab 2 - variant 2

## Laboratory work description

* Design algorithms and data structures in immutable styles
* Usage of recursion
* Develop unit and property-based tests

## Project structure

- `dynamic_array.py` -- includes class `DynamicArray` and class `DArrayIterator`
- `dynamic_array_test.py` -- unit and PBT tests for classes and functions in `dynamic_array.py`.

## Features

- `cons(self, element)`:Add an element at the end of the array.
- `remove(self, pos)`: Remove an element of array at specified position.
- `length(self)`: Return the length of array.
- `member(self, value)`: Determines whether the given value is a
  member of the array.
- `reverse(self)`:  Reverse the array.
- `intersection(self, pos, value)`: Add an element into the array
  at specified position.
- `to_list(self)`: Transform the array to a list.
- `from_list(lst)`: Convert list to dynamic array.
- `find(self, p)`: find element by specific predicate, return a boolean value.
- `filter(self, predicate)`: Filter the array by specific predicate.
- `map(self,function)`: Applies a function to each element in a dynamic array.
- `reduce(self,function)`: Apply function of two arguments cumulatively to
  the items of the array,from left to right, to reduce the array to a single value.
- `iterator(self)`: Convert a dynamic array to an iterator.
- `empty(self)`: return an empty instance of `DynamicArray`.
- `concat(dynamic_array1, dynamic_array2)`: Merge two dynamic arrays.

## Contribution

- Wu Bin
  * GitHub repository created
  * write `dynamic_array.py`
  * solve bugs
- Li Jingwen -- writing README.md
  * write `dynamic_array_test.py`
  * write `README.md`

## Changelog

- 15.5.2022 -3
  - Li Jingwen commits codes.
- 13.5.2022 -2
  - Wu Bin commits codes.
- 12.5.2022 -1
  - Build the project framework.

## Design notes

### Compare mutable and immutable implementation

* A mutable collection can be updated or extended in place. This means you can change,
  add, or remove elements of a collection as a side effect. *Immutable* collections,
  by contrast, never change. You have still operations that simulate additions,
  removals, or updates, but those operations will in each case return a new
  collection and leave the old collection unchanged.
* The immutable data structure allows a developer to work with data safely from many places and
  processes without any surprises with broken states or unexpected data changes. It is all about a
  place where a programmer manages the state. It is a data structure internals for mutable data, and
  all changes are implicit (you can recognize them only by method name). For immutable data – is
  a variable inside your code. If you need to update a state, you should reassign the variable in your
  source code to the immutable version. It may be verbose but explicit and controllable.

