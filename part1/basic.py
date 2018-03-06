# -*- coding: utf-8 -*-

"""
    NOTE:
    There are many ways of solving these problems, but what we
    are looking from you is to specifically use idiomatic Python.
    Please answer each of these problems below using Python 2.7.

    If you enjoy a challenge, you can provide multiple solutions to
    these basic questions. :)
"""

"""
**Exercise 1:**
    Transform these lists (left side is INPUT, right side is OUTPUT):
    [1,2,3,1,5] → [15,11,13,12,11]
    [‘a’,’b’,’c’,’d’,’e’]    →   [‘e’,’d’,’c’,’b’,’a’]
    [‘a’,’b’,’c’,’d’,’e’]    →   [‘a’,’c’,’e’]
    [‘a’,’b’,’c’,’d’,’e’]    →   [‘b’,’d’]
    [11,6,10] → [11,10,6,[27]]
"""
# Exercise 1 solution

numeric_arr1 = [1,2,3,1,5]
output_arr1 = [15,11,13,12,11]


def reverse_add_ten(input):
    return [x+10 for x in input][::-1]

assert reverse_add_ten(numeric_arr1) == output_arr1


alpha_array = ['a','b','c','d','e']
output_arr2 = ['e','d','c','b','a']
output_arr3 =  ['a','c','e']
output_arr4 = ['b','d']

def reverse_array(input):
    return input[::-1]

assert reverse_array(alpha_array) == output_arr2

def odd_elements_array(input):
    return input[::2]

assert odd_elements_array(alpha_array) == output_arr3

def even_elements_array(input):
    return input[1::2]

assert even_elements_array(alpha_array) == output_arr4


numeric_arr2= [11,6,10]
output_arr5 = [11,10,6,[27]]

def sort_append_sum_aslist(input):
    result = sorted(input,reverse=True)
    result.append([sum(result)])
    return result

assert sort_append_sum_aslist(numeric_arr2) == output_arr5

"""
    **Exercise 2:**
    We have a function `complex_function` to compute certain data, printing out
    the result after the computation. This is great, but we want to add some
    functionality. We want to push to a log:
    - the time used by the function to run
    - the name of the function
    - the input values of the function.

    Note: We cannot modify the body of the original `complex_function` function.
"""
# Exercise 2 solution
import time

def logger(input_function):
    def wrapper_function(input):
        start = time.time()
        input_function(input)
        print "This function took this many seconds to run -",time.time()-start
        print "Its name is -",input_function.__name__
        print "It had the following inputs -", input
    return wrapper_function


@logger
def complex_function(num):
    time.sleep(1)
    return num**2
    
complex_function(23)


"""
**Exercise 3:**
    Define a custom `MyDict` class that allows the following operations:
    - set/read values using both the dot notation (e.g. `mydict.name`) and
      item access notation used for dictionaries (e.g. `mydict[name]`).
      In case the mapped value is not present, returns `None`.
    - A + B addition operation:
      `MyDict` + `dict` = `MyDict`;
      `MyDict` + `MyDict` = `MyDict`;
      the result of this operation is a `MyDict` object, having all the fields
      of both dictionaries. In case of common keys between the dictionaries,
      their values need to be added/appended together (according to their type.
      For the sake of the exercise, admissible types are only
      `int` and `string`).

      Example:
      ```
      m = MyDict()
      m.a = 10
      m['b'] = 20
      print m['c']  # prints `None`
      n = {'a': 10, 'c': 15}
      print m + n  # prints `{'a': 20, 'b':20, 'c': 15}
      ```
"""
# Exercise 3 solution

class MyDict(dict):
    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        try:
            return self.__dict__[key]
        except KeyError:
            return None

    # There is something here I don't quite understand.
    # This function is hit only when the attribute is not present in the instance of MyDict.
    # Honestly not sure what is happening here, but it works as we'd like it.
    def __getattr__(self,key):
        print "hello from __getattr__"
        return None

    def as_dict(self):
        return self.__dict__

    def iteritems(self):
        return self.__dict__.iteritems()

    def __add__(self,addend):
        result = self.__dict__.copy()
        for key, value in addend.iteritems():
            try:
                result[key] += value
            except KeyError:
                result[key] = value
        return result

first_dict = MyDict()
first_dict.a = 10
first_dict['b'] = 20
assert first_dict['c'] == None
second_dict = {'a': 10, 'c': 15}
assert (first_dict + second_dict) == {'a': 20, 'b':20, 'c': 15}
