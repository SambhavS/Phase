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

def loadx(env, fname):
	with open(fname) as f:
		# Escape special chars
		string = f.read()
		string = re.sub(r"\'", "\\'", string)
		string = re.sub(r"\(", "\(", string)
		string = re.sub(r"\)", "\)", string)
	return string

# String/List Functions

def get(env, ind, seq):
	return seq[ind]

def length(env, seq):
	return len(seq)

def indx(env, item, seq):
	return seq.index(item)

def lastx(env, seq):
	return seq[-1]

def zipx(env, seq1, seq2):
	return list(zip(seq1, seq2))

# List Functions
def popx(env, lst):
	return lst.pop()

def pushx(env, item, lst):
	lst.append(item)

def seqx(env, start, end):
	return list(range(start, end))

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

def strx(env, nstring):
	return str(nstring)

def intx(env, nint):
	return int(nint)

def helpx(env):
	print("Welcome to Phase!")
	print("Read the documentation here:")
	print("https://github.com/SambhavS/Phase#documentation")
	print("To exit the repl, type `exit`")

"*Many functions end with an x to prevent shadowing of a Python keyword or builtin name*"
