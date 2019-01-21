# Phase
Phase is a dynamically typed programming language with prefix notation. Much of its syntax takes inspiration from Python and Scheme. 
You can run Phase files using the Python interpreter, with the command `$python3 phase_main.py FILENAME.phs`, where FILENAME.phs is your Phase file. 

You can also use the read-eval-print-loop (REPL) by omitting the filename: 
`$python3 phase_main.py`. 


The example file `example.phs` is a tutorial composed of examples to help you get started with writing short programs. Once you've skimmed through the documentation below, it should be your next resource. Run `$python3 phase_main.py example.phs` to get started.


Phase is a simple language with a small core of keywords and few primitive data types. It uses prefix notation, like Lisps, and is whitespace separated like Python (4-spaces or tabs). It is best learned by reading the documentation, playing with `example.phs`, and testing out simple programs by using the REPL or runnning your own scripts. 


One can assume choices not explicitly outlined in the documentation below are made in the most Pythonic way possible.


To report bugs, ask questions, or give feedback, send an email to sambhav@berkeley.edu

# Documentation

## Prefix Notation

Functions are called using prefix notation. This means that a function call is a function name followed by its arguments.
For example, to add two numbers, one would write `+ 10 20`. No parenthesis are needed if only one function is being called in the line. If multiple functions are being called, all nested function calls must have parenthesis. 

For example, `prn (+ (+ 1 2) 3)` would print the sum of 1, 2, and 3.

## Data Types

Phase supports integers, booleans, strings, lists, user-defined functions and the None object.

**Integers**

Integers are represented literally in the conventional way. `1`, `-12`, and `30` are all examples of valid integers

**Booleans**

Booleans can be represented literally as `T` (for true) and `F` (for false). 

**Strings**

Strings must be represented with one quote to begin them and one quote to end them. For example, `'Hello'` is a valid string. Parenthesis and single quotes must be escaped with the backslash. The load function automatically escapes all single quotes and parenthesis in the file it is given.

**Lists**

Lists can hold data of different types. When instantiating a list literal, elements should be separated by spaces. For example, `[1 2 3]` is a valid list.

**User-defined Functions**

Users can define their own functions use the `def` keyword (see details below). User-defined functions are called with the same syntax and rules as builtin functions. Functions are NOT treated as first class objects and higher order functions are therefore not permitted. Helper functions may be defined and used within user-defined functions. Function names can't be reserved words (keywords, special functions, T, F, None), can't contain single quotes or parenthesis, and must start with a letter or underscore.

**None**

`None` is Phase's null value. Functions that don't return anything explicitly return `None`. `None` is falsey.

## Special Functions 
**prn**

`prn` is the printing function. prn takes in a single argument and prints it.

**let**

`let` is the assignment function. `let` takes in a variable name and an expression that evaluates to a value. The equivalent of the Pythonic assignment `x = 5` would be written as `let x 5` in Phase. Assignments must be literals; aliasing is not allowed.

**inc**

`inc` lets you increment a variable that has an integer value. Instead of writing `let x (+ x 1)` you can write `inc x`

## Control (for, while, if)
Control keyword syntax is: keyword[one space][open paren][keyword body][close paren]. For example, `if (eq x 1):`. More examples can be seen in example.phs. The control keywords work very similarly to their counterparts in Python.

**if**

The block corresponding to the `if` statement will be executed iff the evaluated expression is truthy. Note that there is (currently) no "else" or "elif" construct.

**while**

The block corresponding to the `while` statement will be executed iff the evaluated expression is truthy. If the body is executed, the expression will be checked once more and if it remains truthy, the body will be run again. This loop keeps on happening until the while expression is no longer truthy.

**for**

`for` in Phase is very similar to `for` in Python. `for` takes in a new variable name and either a list or variable whose value is a list. It then iterates through the list, allowing each value to be accessed in the loop by referring to the given variable. Code in the `if` block should be indented. The iterative variable is removed from the environment at the end of the loop.


## Boolean Keywords
`and`, `not`, and `or` are boolean keywords. If you've never used boolean operators before, you can read about them here: https://en.wikipedia.org/wiki/Boolean_algebra#Basic_operations. Syntactically, they work like functions but may not evaluate all given arguments because of short circuiting.

## Function Keywords
**def**

`def` allows the user to define his own functions. Like Scheme and Python, `def` should be followed by the function name and its parameters in the same syntax as if you were calling the function with arguments.

**return**

Use `return` to return a value. In Phase, functions and whole programs have return values. Be sure to turn the 'return_prog_val' flag on if you want the return value of a program, if you are extending the interpreter. You can print the returned program value in the command line by typing the `-p` flag before the name of your Phase file.

## Builtin Functions
Phase has a host of builtin functions. They are wrapped around Python's builtin functions, so reference for them can be found at https://docs.python.org/3/library/functions.html. Read the (very short) builtin file to read how each builtin was implemented. Check the builtin file for the most recent list of builtins, but here are a list of all provided builtins as of writing this:

`prn`, `let`, `eq`, `not_eq`, `+`, `/`, `*`, `mod`, `-`, `pow`, `abs`, `min`, `max`, `sort`, `sum`, `rand`, `zip`, `rev`, `pop`, `push`, `get`, `len`, `ind`, `seq`

## Comments
Single line comments can be written by writing a `#` at the start of a line. Everything on the line afer the `#` will be ignored by the interpreter.

Multi line comments can be written by writing `###` at the start of the line that begins the multi line comment and `###` at the start of the line that ends of the multi line comment.

