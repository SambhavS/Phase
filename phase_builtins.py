import random
import re

## Built-in Functions ##

# Special Keyword Functions
def inc(env, name):
	env[name] += 1

def let(env, name, value):
	env[name] = value

# Boolean Functions
def eq(env, a, b):
	return a == b

def not_eq(env, a, b):
	return a != b	

# IO Functions
def inputx(env):
	return input()


# List Functions
def get(env, ind, lst):
	return lst[ind]

def length(env, lst):
	return len(lst)

def popx(env, lst):
	return lst.pop()

def pushx(env, item, lst):
	lst.append(item)

def indx(env, item, lst):
	return lst.index(item)

def seqx(env, start, end):
	return list(range(start, end))

def zipx(env, lst1, lst2):
	return list(zip(lst1, lst2))

# Math Functions
def add(env, a, b):
	return a + b

def mod(env, a, b):
	return a % b

def sub(env, a, b):
	return a - b

def mul(env, a, b):
	return a * b

def fldiv(env, a, b):
	return a // b

def powx(env, a, b):
	return pow(a, b)

def absx(env, num):
	return abs(num)

def minx(env, lst):
	return min(lst)

def maxx(env, lst):
	return max(lst)

def sortx(env, lst):
	return list(sorted(lst))

def sumx(env, lst):
	return sum(lst)

def rand(env, start, end):
	return random.randint(start, end)

def revx(env, lst):
	return lst[::-1]
