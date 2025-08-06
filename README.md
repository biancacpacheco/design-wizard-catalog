# Design Tests Catalog
The Design Tests Catalog is a repository of design assessments for introductory programming courses. Each test includes a description, the rationale behind its creation, and examples of both accepted and rejected code submissions.

# Methodology
This repository contains a collection of design tests for Python code, designed to be used with the Python Design Wizard tool. These tests were created based on a manual review of introductory programming courses from 22 different courses across 5 Brazilian universities. While most of the courses belong to Computer Science programs, we also included equivalent courses from various engineering programs in our analysis.

The test scripts included in this catalog can be found in the /Catalog directory of this repository, organized into subdirectories that correspond to the section titles of the catalog outlined below.

# How to Execute
Place the /Catalog directory in the root of your python-dw clone
```
.
|_api
|_Catalog
```

You can then execute any test with the command:
```bash
python3 -m catalog.topic_name.test_name path/to/file.py
```
for example, to run the bubble sort test:
```bash
python3 -m catalog.sorting_algorithms.bubblesort_test tests/data/bubblesort.py
```
# Table of Tests
- [Sorting Algorithms](#sorting-algorithms)
    - [Bubble Sort](#bubble-sort)
    - [Insertion Sort](#insertion-sort)
    - [Merge Sort](#merge-sort)
    - [Quick Sort](#quick-sort)
    - [Selection Sort](#selection-sort)
    - [Counting Sort](#counting-sort)
- [Search Algorithms](#search-algorithms)
    - [Linear Search](#linear-search)
    - [Binary Search](#binary-search)
- [Prohibited Structures and Functions](#prohibited-structures-and-functions)
    - [Prohibited Function Calls](#prohibited-function-calls)
    - [Prohibited Data Structures](#prohibited-data-structures)
- [Usage of Specific Elements](#usage-of-specific-elements)
    - [Exclusive Use of Finite Loops (For)](#exclusive-use-of-finite-loops-for)
    - [Exclusive Use of Infinite Loops (While)](#exclusive-use-of-infinite-loops-while)
    - [Usage of Conditionals](#usage-of-conditionals)
    - [Usage and Manipulation of Lists](#usage-and-manipulation-of-lists)
    - [Declaration of Functions](#declaration-of-functions)
    - [Auxiliary functions](#auxiliary-functions)
    - [Auxiliary lists](#auxiliary-lists)
    - [Auxiliary variables](#auxiliary-variables)
    - [Usage of Pre-Estabilished Functions](#usage-of-pre-estabilished-functions)
- [Code Smells](#code-smells)
    - [Excessive Number of Arguments](#excessive-number-of-arguments)
    - [Excessive Number of Returns](#excessive-number-of-returns)

# Sorting Algorthims

This section contains scripts to statically analyze sorting algorithm implementations by students. The main focus is to see if the student is following the expected structure of each classic sorting algorithm (i.e a bubblesort should be composed of two nestled fors and no auxiliary variables).

## Bubble Sort

Description: This is the script that tests if an implementation of a bubblesort is following it's expected structure with two nestled 'for' loops and no auxiliary variables:

``` python
import sys
from api.design_wizard import PythonDW

if len(sys.argv) != 2:
    print("Usage: python3 script.py path/to/file.py")
    sys.exit(1)

script_path = sys.argv[1]

python_dw = PythonDW()
python_dw.parse(script_path)
python_dw.design_populate_all_entities()

function_names = python_dw.get_all_functions()

args = function_names[0].args.args
args_names = [i.arg for i in args]

for_entities = python_dw.get_entities_by_type("for")

nestled_fors = False
aux_variable = False

if len(for_entities) == 2:
    relations = python_dw.design_get_callees_from_entity_relation('for1', 'HASLOOP')
    if len(relations) > 0:
        if relations[0].get_name() == for_entities[1].get_name():
            nestled_fors = True
        
    
    if (nestled_fors):
        body = for_entities[0].get_ast_node().body
        for node in body:
            if python_dw.verify_instance(node, "assign"):
                for t in node.targets:
                    if python_dw.verify_instance(t, "name"):
                        if t.id not in args_names:
                            aux_variable = True

bubble_sort_structure = nestled_fors and not aux_variable

print(bubble_sort_structure)
```

As seen above, the code first checks whether there are indeed two nested 'for' loops in the function. If so, it then inspects the 'Assign' nodes in the syntax tree to see if any of them involve the creation of a new variable. This check helps determine whether the student likely implemented bubble sort rather than selection sort, which also features nested 'for' loops but typically uses an auxiliary variable. Therefore, the following code passes the test:

```python
def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr) - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
```

whereas the following one does not:

```python
def selection_sort(array, size):  
    for ind in range(size):
        min_index = ind

        for j in range(ind + 1, size):
            if array[j] < array[min_index]:
                min_index = j
        (array[ind], array[min_index]) = (array[min_index], array[ind])
    return array
```

## Insertion Sort

Description: This is the script that tests if an implementation of a insertion sort is following it's expected structure with a 'while' loop nestled within a 'for' loop:

```python
import sys
from api.design_wizard import PythonDW

if len(sys.argv) != 2:
    print("Usage: python3 script.py path/to/file.py")
    sys.exit(1)

script_path = sys.argv[1]

python_dw = PythonDW()
python_dw.parse(script_path)
python_dw.design_populate_all_entities()

for_entities = python_dw.get_entities_by_type('for')
while_entities = python_dw.get_entities_by_type('while')

insertion = False

if len(for_entities) == 1 and len(while_entities) == 1:
    relations = python_dw.design_get_callees_from_entity_relation('for1', 'HASLOOP')
    if len(relations) > 0:
        if relations[0].get_name() == while_entities[0].get_name():
            insertion = True

print(insertion)
```

the following code is an example that passes this test:

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
```

while the following one, that contains two nestled loops, but not a 'while' loop inside of a 'for', does not:

```python
def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr) - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
```

## Merge Sort

Description: The following script tests if an implementation of a Merge Sort algorithm follows it's expected structure: with the creation of an auxiliary function, use of auxiliary lists and also usage of two or three 'while' loops:  

```python
import sys
from api.design_wizard import PythonDW

if len(sys.argv) != 2:
    print("Usage: python3 script.py path/to/file.py")
    sys.exit(1)

script_path = sys.argv[1]

python_dw = PythonDW()
python_dw.parse(script_path)
python_dw.design_populate_all_entities()

merge_sort = True
while_entities = python_dw.get_entities_by_type("while")


if (not len(while_entities) == 2 and not len(while_entities) == 3):
    merge_sort = False

if merge_sort:
    functions = python_dw.get_all_functions()
    if len(functions) < 2:
        merge_sort = False

if merge_sort:
    arguments = functions[0].args.args
    args_names = [a.arg for a in arguments]

    assign_entities = python_dw.get_entities_by_type("assign")

    aux_structure = False

    for e in assign_entities:
        body = e.get_body()
        if python_dw.verify_instance(body, "list"):
            aux_structure = True
            break

        elif python_dw.verify_instance(body, "binop"):
            targets = e.ast_node.targets 
            if python_dw.verify_instance(body.left,"list") or (python_dw.verify_instance(body.right,"list")):
                for t in targets:
                    if t.id not in args_names:
                        aux_structure = True
                        break

if not aux_structure:
    merge_sort = False 

print(merge_sort)
```

The following code passes the test, as a classic merge sort implementation:

```python
def merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m

    L = [0] * (n1)
    R = [0] * (n2)
    
    for i in range(0, n1):
        L[i] = arr[l + i]
    
    for j in range(0, n2):
        R[j] = arr[m + 1 + j]
    
    i = 0    
    j = 0    
    k = l  
    
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def mergeSort(arr, l, r):
    if l < r:
        m = l+(r-l)//2
        mergeSort(arr, l, m)
        mergeSort(arr, m+1, r)
        merge(arr, l, m, r)
```
Whereas the next one does not, as it does have a auxiliary function, but the sorting happens in place within the given array:

```python
def partition(array, low, high):
    pivot = array[high]
    i = low - 1
    for j in range(low, high):
        if array[j] <= pivot:
            i = i + 1
            (array[i], array[j]) = (array[j], array[i])
    (array[i + 1], array[high]) = (array[high], array[i + 1])
    return i + 1

def quickSort(array, low, high):
    if low < high:
        pi = partition(array, low, high)
        quickSort(array, low, pi - 1)
        quickSort(array, pi + 1, high)
```

## Quick Sort

Description: This test verifies if an implementation of a Quick Sort algorithm follows the structure expected: using one 'for' loop, implementing an auxiliary function, and not using any auxiliary lists.

```python
import sys
from api.design_wizard import PythonDW

if len(sys.argv) != 2:
    print("Usage: python3 script.py path/to/file.py")
    sys.exit(1)

script_path = sys.argv[1]

python_dw = PythonDW()
python_dw.parse(script_path)
python_dw.design_populate_all_entities()

quick_sort = True
for_entities = python_dw.get_entities_by_type("for")


if (not len(for_entities) == 1):
    quick_sort = False


if quick_sort:
    functions = python_dw.get_all_functions()
    if len(functions) < 2:
        quick_sort = False

if quick_sort:
    arguments = functions[0].args.args
    args_names = [a.arg for a in arguments]

    assign_entities = python_dw.get_entities_by_type("assign")

    aux_structure = False

    for e in assign_entities:
        body = e.get_body()
        if python_dw.verify_instance(body, "list"):
            aux_structure = True
            break

        elif python_dw.verify_instance(body, "binop"):
            targets = e.ast_node.targets 
            if python_dw.verify_instance(body.left,"list"):
                for t in targets:
                    if t.id not in args_names:
                        aux_structure = True
                        break
            if ((not aux_structure) and (python_dw.verify_instance(body.left,"list"))):
                for t in targets:
                    if t.id not in args_names:
                        aux_structure = True
                        break

if aux_structure:
    quick_sort = False 

print(quick_sort)
```

As expected, the following implementation of a quick sort does pass the test: 

```python
def partition(array, low, high):
    pivot = array[high]
    i = low - 1
    for j in range(low, high):
        if array[j] <= pivot:
            i = i + 1
            (array[i], array[j]) = (array[j], array[i])
    (array[i + 1], array[high]) = (array[high], array[i + 1])
    return i + 1

def quickSort(array, low, high):
    if low < high:
        pi = partition(array, low, high)
        quickSort(array, low, pi - 1)
        quickSort(array, pi + 1, high)
```

while the implementation of a merge sort, despite having an auxiliary function, does not: 

```python
def merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m

    L = [0] * (n1)
    R = [0] * (n2)
    
    for i in range(0, n1):
        L[i] = arr[l + i]
    
    for j in range(0, n2):
        R[j] = arr[m + 1 + j]
    
    i = 0    
    j = 0    
    k = l  
    
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def mergeSort(arr, l, r):
    if l < r:
        m = l+(r-l)//2
        mergeSort(arr, l, m)
        mergeSort(arr, m+1, r)
        merge(arr, l, m, r)
```

## Selection Sort

Description: This test checks if the implementation of the Selection Sort algorithm fits the expected two nestled 'for' loops along with the usage of an auxiliary variable.

```python
import sys
from api.design_wizard import PythonDW

if len(sys.argv) != 2:
    print("Usage: python3 script.py path/to/file.py")
    sys.exit(1)

script_path = sys.argv[1]

python_dw = PythonDW()
python_dw.parse(script_path)
python_dw.design_populate_all_entities()

function_names = python_dw.get_all_functions()

args = function_names[0].args.args
args_names = [i.arg for i in args]

for_entities = python_dw.get_entities_by_type("for")

nestled_fors = False
aux_variable = False

if len(for_entities) == 2:
    relations = python_dw.design_get_callees_from_entity_relation('for1', 'HASLOOP')
    if len(relations) > 0:
        if relations[0].get_name() == for_entities[1].get_name():
            nestled_fors = True
        
    
    if (nestled_fors):
        body = for_entities[0].get_ast_node().body
        for node in body:
            if python_dw.verify_instance(node, "assign"):
                for t in node.targets:
                    if python_dw.verify_instance(t, "name"):
                        if t.id not in args_names:
                            aux_variable = True

print(nestled_fors and aux_variable)
```

The implementation of the selection sort below passes the test:

```python
def selection_sort(array, size):  
    for ind in range(size):
        min_index = ind

        for j in range(ind + 1, size):
            if array[j] < array[min_index]:
                min_index = j
        (array[ind], array[min_index]) = (array[min_index], array[ind])

    return array
```

A bubblesort implementation, on the other hand, does not pass the test, as despite having two nestled 'for'loops, it does not use an auxiliary variable:

```python
def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr) - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
````

## Counting Sort

Description: The following test checks the implementation of the Counting Sort algorithm, ensuring it uses three non-nestled 'for' loops and two auxiliary arrays

```python
import sys
from api.design_wizard import PythonDW

if len(sys.argv) != 2:
    print("Usage: python3 script.py path/to/file.py")
    sys.exit(1)

script_path = sys.argv[1]

python_dw = PythonDW()
python_dw.parse(script_path)
python_dw.design_populate_all_entities()

for_entities = python_dw.get_entities_by_type("for")

check_fors = False

if len(for_entities) == 3:
    for f in for_entities:
        if not python_dw.design_get_callees_from_entity_relation(f.get_name(), 'HASLOOP'):
            check_fors = True

check_aux_arrays = False

if check_fors:
    
    aux_arrays = 0
    verified_arrays = []

    function_names = python_dw.get_all_functions()

    args = function_names[0].args.args
    args_names = [i.arg for i in args]

    assign_entities = python_dw.get_entities_by_type("assign")

    for e in assign_entities:
        body = e.get_body()
        if python_dw.verify_instance(body, "list"):
            if body not in verified_arrays:
                aux_arrays += 1
                verified_arrays.append(body)
        elif python_dw.verify_instance(body, "binop"):
            targets = e.ast_node.targets 
            if python_dw.verify_instance(body.left,"list") or (python_dw.verify_instance(body.right,"list")):
                for t in targets:
                    if (t.id not in args_names) and (body not in verified_arrays):
                        verified_arrays.append(body)
                        aux_arrays += 1
    if aux_arrays == 2:
        check_aux_arrays = True


print(check_aux_arrays and check_fors)
```

The implementation of the counting sort algorithm below passes the test: 

```python
def counting_sort(A, k):
    
        C = [0] * k

        for i in range(len(A)):
            C[A[i] - 1] += 1;
        
        for i in range(1, len(C)):
            C[i] += C[i-1];
        
        B = [0] * len(A)

        for i in range(len(A) - 1, -1, -1):
            B[C[A[i] - 1] - 1] = A[i]
            C[A[i] - 1] -= 1

        return B;
    
```
A mergesort implementation, however, does not, as it does not meet the requirements in the test:

```python
def merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m

    L = [0] * (n1)
    R = [0] * (n2)
    
    for i in range(0, n1):
        L[i] = arr[l + i]
    
    for j in range(0, n2):
        R[j] = arr[m + 1 + j]
    
    i = 0    
    j = 0    
    k = l  
    
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def mergeSort(arr, l, r):
    if l < r:
        m = l+(r-l)//2
        mergeSort(arr, l, m)
        mergeSort(arr, m+1, r)
        merge(arr, l, m, r)
```

# Search Algorithms

This section contains scripts to statically analyze search algorithms

## Linear Search

Description: The following test checks if a linear search algorithm was implemented using a 'for' loop and no auxiliary variables

```python
import sys
from api.design_wizard import PythonDW

if len(sys.argv) != 2:
    print("Usage: python3 script.py path/to/file.py")
    sys.exit(1)

script_path = sys.argv[1]

python_dw = PythonDW()
python_dw.parse(script_path)
python_dw.design_populate_all_entities()

for_usage = len(python_dw.get_entities_by_type("for")) == 1

assign_entities = python_dw.get_entities_by_type("assign")
function_names = python_dw.get_all_functions()

aux_var_usage = False

if for_usage:
    args = function_names[0].args.args
    args_names = [i.arg for i in args]

    for e in assign_entities:
        for t in e.ast_node.targets:
            if python_dw.verify_instance(t, "name"):
                if t.id not in args_names:
                    body = e.get_body()
                    if not python_dw.verify_instance(body, "list"):
                        aux_var_usage = True
                        break
                    if python_dw.verify_instance(body, "binop"):
                        if (not python_dw.verify_instance(body.left, "list")) and (not python_dw.verify_instance(body.right, "list")):
                            aux_var_usage = True
                            break
                
linear_search = for_usage and not aux_var_usage
print(linear_search)
```

the following implementation passes the verification:

```python
def linear_search(list, target):
    for i in range(len(list)):
        if list[i] == target:
            return i  
    return -1 
```
 the following code, on the other hand, does not:

```python
def binary_search(list, target):
    start = 0
    end = len(list) - 1

    while start <= end:
        middle = (start + end) // 2

        if list[middle] == target:
            return middle
        elif list[middle] < target:
            start = middle + 1
        else:
            end = middle - 1
    return -1 
```

## Binary Search

Description: This test verifies if the implementation of a binary search follows the expected structure, using one 'while' loop and three auxiliary variables representing the start, middle and end index of the list being verified.

```python
import sys
from api.design_wizard import PythonDW

if len(sys.argv) != 2:
    print("Usage: python3 script.py path/to/file.py")
    sys.exit(1)

script_path = sys.argv[1]

python_dw = PythonDW()
python_dw.parse(script_path)
python_dw.design_populate_all_entities()

while_usage = len(python_dw.get_entities_by_type("while")) == 1

aux_var = []

if while_usage:
    
    assign_entities = python_dw.get_entities_by_type("assign")
    function_names = python_dw.get_all_functions()
    
    args = function_names[0].args.args
    args_names = [i.arg for i in args]

    for e in assign_entities:
        for t in e.ast_node.targets:
            if python_dw.verify_instance(t, "name"):
                if t.id not in args_names:
                    body = e.get_body()
                    if not python_dw.verify_instance(body, "list"):
                        if t.id not in aux_var:
                            aux_var.append(t.id)
                    if python_dw.verify_instance(body, "binop"):
                        if (not python_dw.verify_instance(body.left, "list")) and (not python_dw.verify_instance(body.right, "list")):
                            if t.id not in aux_var:
                                aux_var.append(t.id)


binary_search = while_usage and len(aux_var) == 3

print(binary_search)
```

Below, there is an example of accepted implementation

```python
def binary_search(list, target):
    start = 0
    end = len(list) - 1

    while start <= end:
        middle = (start + end) // 2

        if list[middle] == target:
            return middle
        elif list[middle] < target:
            start = middle + 1
        else:
            end = middle - 1
    return -1 
```

And an implementation that fails the check:

```python
def linear_search(list, target):
    for i in range(len(list)):
        if list[i] == target:
            return i  
    return -1 
```

# Prohibited Structures and Functions

This section contains tests to verify if a student is not using prohibited functions (such as ```sort()```, instead of actual implementation of a sorting algorithm) and data structures (such as a 'set', or a 'dict')

## Prohibited Function Calls

Description: The following script checks if an implementation does not use any prohibited functions (i.e: ```sort()```, ```split()```, ```union()```, ```intersection()```, etc.). It can be personalized according to a course's needs.

```python
import sys
from api.design_wizard import PythonDW

if len(sys.argv) != 2:
    print("Usage: python3 script.py path/to/file.py")
    sys.exit(1)

script_path = sys.argv[1]

python_dw = PythonDW()
python_dw.parse(script_path)
python_dw.design_populate_all_entities()

prohibited_functions = ["sort", "split", "issubset", "issuperset", "union", "intersection", "difference", "join", "symmetric_difference"] 
allowed_function = True

for function in prohibited_functions:
    if python_dw.get_entities_by_type(function) != []:
        allowed_function = False

print(allowed_function)
```

The following code is an example of accepted implementation:

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        return arr
```

The next one fails this test, as it uses the prohibited function ```sort()```:

```python
def insertion_sort(arr):
    arr.sort()
    return arr
```

## Prohibited Data Structures

Description: The following script checks if there is no usage of prohibited data structures (such as a 'dictionary' ou a 'set')

```python
import sys
from api.design_wizard import PythonDW

if len(sys.argv) != 2:
    print("Usage: python3 script.py path/to/file.py")
    sys.exit(1)

script_path = sys.argv[1]

python_dw = PythonDW()
python_dw.parse(script_path)
python_dw.design_populate_all_entities()

prohibited_structures = ["dict", "set"]

assign_entities = python_dw.get_entities_by_type('assign')

allowed_structures = True

for s in prohibited_structures:
    if s in python_dw.entities:
        allowed_structures = False
        break


if allowed_structures:
    for node in assign_entities:
        for struct in prohibited_structures:
            if python_dw.verify_instance(node.get_body(), struct):
                allowed_structures = False
                break
            else:
                for t in node.ast_node.targets:
                    if python_dw.verify_instance(t, struct):
                        allowed_structures = False
                        break

print(allowed_structures)
```

The following code is an accepted implementation, as it does not instance any of the prohibited structures in the example:

```python
def union(list_a, list_b):
    union = []
    for item in list_a + list_b:
        if item not in union:
            union.append(item)
    return union
```
the next one uses the prohibited structure "set", and therefore fails:

```python
def union(list_a, list_b):
    set1 = set(list_a)
    set2 = (list_b)
    union_set = set1 | set2 
    return list(union_set)
```

# Usage of Specific Elements

In this section, we gathered tests that ensure an student is using pre-determined elements (i.e. when learning about 'for' loops, it is important that the student exclusively uses that type of loop in order to learn it).

## Exclusive Use of Finite Loops (for)
Description: This test verifies that a code exclusively uses 'for' loops

```python
import sys
from api.design_wizard import PythonDW

if len(sys.argv) != 2:
    print("Usage: python3 script.py path/to/file.py")
    sys.exit(1)

script_path = sys.argv[1]

python_dw = PythonDW()
python_dw.parse(script_path)
python_dw.design_populate_all_entities()

for_usage = len(python_dw.get_entities_by_type("for")) > 0 
while_usage = len(python_dw.get_entities_by_type("while")) > 0

exclusively_for = for_usage and not while_usage

print(exclusively_for)
```

the script bellow is an example of accepted implementation:

```python
def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr) - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
```

whereas the next one does not, as it uses both 'for' and 'while' loops

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
```

## Exclusive Use of Infinite Loops (while)
 
Description: This test verifies that a code exclusively uses 'while' loops

```python
import sys
from api.design_wizard import PythonDW

if len(sys.argv) != 2:
    print("Usage: python3 script.py path/to/file.py")
    sys.exit(1)

script_path = sys.argv[1]

python_dw = PythonDW()
python_dw.parse(script_path)
python_dw.design_populate_all_entities()

for_usage = len(python_dw.get_entities_by_type("for")) > 0 
while_usage = len(python_dw.get_entities_by_type("while")) > 0

exclusively_while = not for_usage and while_usage

print(exclusively_while)
```
the script bellow is accepted, as it only uses 'while' loops:

```python
def binary_search(list, target):
    start = 0
    end = len(list) - 1

    while start <= end:
        middle = (start + end) // 2

        if list[middle] == target:
            return middle
        elif list[middle] < target:
            start = middle + 1
        else:
            end = middle - 1
    return -1 
```

whereas the next one does not, as it uses both 'for' and 'while' loops

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
```

## Usage of Conditionals

Description: This test ensures that a code uses conditionals ('if' statements)

```python
import sys
from api.design_wizard import PythonDW

if len(sys.argv) != 2:
    print("Usage: python3 script.py path/to/file.py")
    sys.exit(1)

script_path = sys.argv[1]

python_dw = PythonDW()
python_dw.parse(script_path)
python_dw.design_populate_all_entities()

conditionals = len(python_dw.get_entities_by_type("if")) > 0 

print(conditionals)
```

the following code passes the test:

```python
def func(a,b):
    if a > b:
        return a
    else:
        return b
```
whereas the next one does not:

```python
def func(a,b):
    return max(a,b)
```

## Usage and Manipulation of Lists

Description: This test verifies that an implementation uses and/or manipulates lists.

```python
import sys
from api.design_wizard import PythonDW

if len(sys.argv) != 2:
    print("Usage: python3 script.py path/to/file.py")
    sys.exit(1)

script_path = sys.argv[1]

python_dw = PythonDW()
python_dw.parse(script_path)
python_dw.design_populate_all_entities()

list_usage = False

list_usage = len(python_dw.get_entities_by_type("list")) != 0

if not list_usage:
    assign_entities = python_dw.get_entities_by_type("assign")

    for e in assign_entities:
        body = e.get_body()
        if python_dw.verify_instance(body, "list"):
            list_usage = True
            break

        elif python_dw.verify_instance(body, "binop"):
            targets = e.ast_node.targets 
            if python_dw.verify_instance(body.left,"list") or (python_dw.verify_instance(body.right,"list")):
                for t in targets:
                    list_usage = True
                    break
        elif python_dw.verify_instance(body, "tuple"):
            for v in body.elts:
                if python_dw.verify_instance(v, "subscript") or python_dw.verify_instance(v,"list"):
                    list_usage = True
                    break
            if list_usage:
                break
        else:
            targets = e.ast_node.targets
            for t in targets:
                if python_dw.verify_instance(t, "subscript") or python_dw.verify_instance(t, "list"):
                    list_usage = True
                    break
                                
print(list_usage)
```

The test looks at all the assign nodes in the code to see if there are subscript (slice of a list) nodes , list nodes or binary operation (with lists as at least one of the values) nodes

The following code passes this test: 

```python
def func(input_str)
    l = list(input_str)
    for i in l:
        print(l)
```
and the following one does not:

```python
def func(input_str):
    for i in input_str:
        print(i)
```

## Declaration of Functions

Description: This test ensures that the student defines (self made) functions in the implementation

```python
import sys
from api.design_wizard import PythonDW

if len(sys.argv) != 2:
    print("Usage: python3 script.py path/to/file.py")
    sys.exit(1)

script_path = sys.argv[1]

python_dw = PythonDW()
python_dw.parse(script_path)
python_dw.design_populate_all_entities()

defined_functions = len(python_dw.get_all_functions()) > 0

print(defined_functions)
```

The test passes for the following implementation:

```python
def func(a,b):
    if a > b:
        return a
    else:
        return b 
```

and fails for ones with no function definition:

```python
a = int(input())
b = int(input())

if a > b:
    print(a)
else:
    print(b)
```

## Auxiliary Functions
Description: The following code verifies if a script implements more than one function for solving the problem.

```python
import sys
from api.design_wizard import PythonDW

if len(sys.argv) != 2:
    print("Usage: python3 script.py path/to/file.py")
    sys.exit(1)

script_path = sys.argv[1]

python_dw = PythonDW()
python_dw.parse(script_path)
python_dw.design_populate_all_entities()

aux_function = len(python_dw.get_all_functions()) >= 2

print(aux_function)
```

The test looks at the number of functions created to determine if there is indeed more than one function being defined, therefore, it accepts the following code:

```python
def partition(array, low, high):
    pivot = array[high]
    i = low - 1
    for j in range(low, high):
        if array[j] <= pivot:
            i = i + 1
            (array[i], array[j]) = (array[j], array[i])

    (array[i + 1], array[high]) = (array[high], array[i + 1])
    return i + 1


def quickSort(array, low, high):
    if low < high:
        pi = partition(array, low, high)
        quickSort(array, low, pi - 1)
        quickSort(array, pi + 1, high)
```

and declines the one below:

```python
def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr) - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
```
## Auxiliary Lists
Description: Similarly to the previous one, this test verifies the existence of auxiliary lists in an implementation. It checks for assign nodes that include a list or operation using lists with a different name from the ones listed as arguments of the function.

```python
import sys
from api.design_wizard import PythonDW

if len(sys.argv) != 2:
    print("Usage: python3 script.py path/to/file.py")
    sys.exit(1)

script_path = sys.argv[1]

python_dw = PythonDW()
python_dw.parse(script_path)
python_dw.design_populate_all_entities()

assign_entities = python_dw.get_entities_by_type("assign")

function_names = python_dw.get_all_functions()

#function.args: returns ast.arguments object
#function.args.args: list of arguments
#function.args.args[i].arg: name of the argument 

args = function_names[0].args.args
args_names = [i.arg for i in args]

aux_structure = False

for e in assign_entities:
    body = e.get_body()
    if python_dw.verify_instance(body, "list"):
        aux_structure = True
        break

    elif python_dw.verify_instance(body, "binop"):
        targets = e.ast_node.targets 
        if python_dw.verify_instance(body.left,"list") or (python_dw.verify_instance(body.right,"list")):
            for t in targets:
                if t.id not in args_names:
                    aux_structure = True
                    break
                              
    
print(aux_structure)
```

It returns ```True``` for the following code:

```python
def counting_sort(A, k):
    
        C = [0] * k

        for i in range(len(A)):
            C[A[i] - 1] += 1;
        
        for i in range(1, len(C)):
            C[i] += C[i-1];
        
        B = [0] * len(A)

        for i in range(len(A) - 1, -1, -1):
            B[C[A[i] - 1] - 1] = A[i]
            C[A[i] - 1] -= 1

        return B;
```

And ```False``` for the next one, as the manipulated list is received as an argument:

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
```

## Auxiliary Variables

Description: Like the last two tests, this one verifies if an implementation uses or not auxiliary variables by checking the assign nodes and verifying variables not listed in the arguments of the function

```python
import sys
from api.design_wizard import PythonDW

if len(sys.argv) != 2:
    print("Usage: python3 script.py path/to/file.py")
    sys.exit(1)

script_path = sys.argv[1]

python_dw = PythonDW()
python_dw.parse(script_path)
python_dw.design_populate_all_entities()

assign_entities = python_dw.get_entities_by_type("assign")
function_names = python_dw.get_all_functions()

aux_vars = False

args = function_names[0].args.args
args_names = [i.arg for i in args]

for e in assign_entities:
    for t in e.ast_node.targets:
        if python_dw.verify_instance(t, "name"):
            if t.id not in args_names:
                body = e.get_body()
                if not python_dw.verify_instance(body, "list"):
                    aux_vars = True
                    break
                if python_dw.verify_instance(body, "binop"):
                    if (not python_dw.verify_instance(body.left, "list")) and (not python_dw.verify_instance(body.right, "list")):
                        aux_vars = True
                        break
                

print(aux_vars)            
```

An example of accepted code:

```python
def selection_sort(array, size):  
    for ind in range(size):
        min_index = ind

        for j in range(ind + 1, size):
            if array[j] < array[min_index]:
                min_index = j
        (array[ind], array[min_index]) = (array[min_index], array[ind])

    return array
```

And an example of rejected code:

```python
def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr) - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
```

## Usage of Pre-Estabilished Functions

Description: This test ensures that the student uses pre-estabilished functions (i.e: ```range()```)

```python
import sys
from api.design_wizard import PythonDW

if len(sys.argv) != 2:
    print("Usage: python3 script.py path/to/file.py")
    sys.exit(1)

script_path = sys.argv[1]

python_dw = PythonDW()
python_dw.parse(script_path)
python_dw.design_populate_all_entities()

necessary_elements = ["range", "for"]
usage_of_necessary_elements = True

entities = python_dw.entities

for element in necessary_elements:
    if element not in entities:
        usage_of_necessary_elements = False
        break

print(usage_of_necessary_elements)
```

It passes the following implementation:

```python
def func(list_of_ints):
    for i in range(len(list_of_ints)):
        print(list_of_ints[i])
```
yet, it fails in the following one, as it cannot spot the usage of ```range()```:

```python
def func(list_of_ints):
    for i in list_of_ints:
        print(i)
```

# Code Smells

The main goal of the tests in this section is to verify bad smells that could be avoided by students, such as a long list of arguments or an excessive number of `return`'s in a function.

## Excessive Number of Arguments

Description: This test verifies if the number of arguments in each function declared does not exceed a number - which can be adapted to it's context.

```python
import sys
from api.design_wizard import PythonDW

if len(sys.argv) != 2:
    print("Usage: python3 script.py path/to/file.py")
    sys.exit(1)

script_path = sys.argv[1]

python_dw = PythonDW()
python_dw.parse(script_path)
python_dw.design_populate_all_entities()

functions= python_dw.get_all_functions()

#function.args: returns ast.arguments object
#function.args.args: list of arguments
#function.args.args[i].arg: name of the argument 

arg_limit = 5
accepted_number_of_args = True

for f in range(len(functions)):
    args = functions[f].args.args
    
    if len(args) > arg_limit:
        accepted_number_of_args = False
        break

print(accepted_number_of_args)
```

In this specific test, the limit of arguments for every single function is 5. As an example, the following code passes this test:  

```python
def sum_of_five(arr):
    v = 0
    for i in range(5):
        v += arr[i]
    return v
```

And it fails the next one

```python
def sum_of_five(a,b,c,d,e):
    return a+b+c+d+e
```

## Excessive Number of Returns

Description: This tests ensures that the student is not overusing 'return' statements in the implementation 

```python
import sys
from api.design_wizard import PythonDW

if len(sys.argv) != 2:
    print("Usage: python3 script.py path/to/file.py")
    sys.exit(1)

script_path = sys.argv[1]

python_dw = PythonDW()
python_dw.parse(script_path)
python_dw.design_populate_all_entities()

acceptable_number_of_returns = len(python_dw.get_entities_by_type("return")) <= 3

print(acceptable_number_of_returns)
```

In this case, the test ensures that a code uses no more than three ```return```statements. It accepts the following code:

```python
def student_status(grade):
    if grade < 0:
        status = 'Invalid grade value''
    elif grade < 5:
        status = 'Failed'
    elif grade >= 5 and grade < 7:
        status = 'Must take final exam''
    else:
        status = 'Passed'
    
    return status
```

but not the following one:

```python
def student_status(grade):
    if grade < 0:
        return 'Invalid grade value''
    elif grade < 5:
        return 'Failed'
    elif grade >= 5 and grade < 7:
        return 'Must take final exam''
    else:
        return 'Passed'
```
