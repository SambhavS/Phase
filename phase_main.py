import re
import random
from phase_builtins import *

DIGITS = set(["-","1","2","3","4","5","6","7","8","9","0"])
SPECIAL_WORDS = set(["let", "inc", "and", "or", "not"])
"""
error/exception handling, timing issues
"""
def eval_program(program, return_prog_val=False, complement_env={}):
	env = {"prn": prn, "let": let, "eq" : eq, "not_eq": not_eq, "add": add,
		   "div": fldiv, "mul": mul, "mod": mod, "sub": sub, "pow": powx, 
		   "abs": absx, "min": minx, "max": maxx, "sort": sortx, "sum": sumx, 
		   "rand": rand, "zip": zipx, "rev": revx, "pop": popx, "push": pushx, 
		   "get": get, "len": length, "ind": indx, "seq": seqx}
	env.update(complement_env)
	prog_val = eval_func(env, program+"\n")
	if return_prog_val:
		return prog_val

def eval_func(env, func_call):
	code, indents = extract_code(func_call)
	line_num = 0
	loops = []
	for_env = {}
	while line_num < len(code):
		code_str = code[line_num]
		ind_lvl = indents[line_num]
		if len(loops) and ind_lvl <= loops[-1][-1]:
			loop_type, expression, loop_linenum, var_dict, _ = loops[-1]
			if eval_expr(env, expression):
				if loop_type == "for":
					inc(env, var_dict["ind_name"])
					index = eval_expr(env, var_dict["ind_name"])
					lst = eval_expr(env, var_dict["lst"])
					let(env, var_dict["var_name"], lst[index])
				line_num = loop_linenum + 1
			else:
				loops.pop()
			continue
		if code_str and code_str[0] != "#":
			tokens = code_str.split()
			command = tokens[0]
			# Control		
			if command in ("while", "if", "for"):

				if command == "for":
					expression = code_str[code_str.find("(")+1 : code_str.rfind(")")]
					ind = expression.index(" ")
					var_name, lst_expression = expression[:ind], expression[ind+1:]
					lst = eval_expr(env, lst_expression)
					if lst:
						ind_name = "FOR_{}".format(var_name)
						let(env, ind_name, 0)
						let(env, var_name, lst[0])
						expression = "not_eq {} (sub (len {}) 1)".format(ind_name, phasify(lst))
						loops.append((command, expression, line_num, 
									 {"var_name":var_name, "ind_name":ind_name, "lst": phasify(lst)}, ind_lvl))

				if command in ("if", "while"):
					expression = code_str[code_str.find("(")+1 : code_str.rfind(")")]
					if not eval_expr(env, expression):
						line_num += 1
						while line_num < len(code) and indents[line_num] > ind_lvl:
							line_num += 1
						continue
					elif command == "while":
						loops.append((command, expression, line_num, {}, ind_lvl))

			elif command == "return":
				return eval_expr(env, code_str[code_str.find(" "):].strip())
			elif command == "def":
				def_tokens = code_str[code_str.find("(")+1 : code_str.rfind(")")].split()
				func_name, arguments = def_tokens[0], def_tokens[1:]
				func_body = ""
				line_num += 1
				while line_num < len(code) and indents[line_num] > ind_lvl:
					func_body += "\t"*indents[line_num] + code[line_num] + "\n"
					line_num += 1
				let(env, func_name, lambda env, *params: user_func(env, func_body, arguments, *params))
			else:
				eval_expr(env, code_str)

		line_num += 1

def phasify(obj):
	if isinstance(obj, bool):
		return 'T' if obj else 'F'
	if isinstance(obj, int):
		return str(obj)
	if isinstance(obj, str):
		return "'" + obj + "'"
	if isinstance(obj, list):
		phasified_list = [phasify(i)+" " for i in obj]
		return "[" + "".join(phasified_list).strip() + "]"
	err("Bad obj: {}".format(obj))

def eval_expr(env, expression):
	expression = deparen(env, expression.strip())
	tokens = tokenize(expression)
	fst = tokens[0]

	if fst[0] == "'":
		return fst[1:-1]
	elif set([i for i in fst]).issubset(DIGITS):
		return int(fst)
	elif fst[0] == "[":
		return [eval_expr(env, i) for i in expression[1:-1].split()]
	elif fst in ('T', 'F'):
		return True if fst == 'T' else False
	elif fst in SPECIAL_WORDS:

		# Keyword Functions
		if fst == "let":
			arguments = [tokens[1], eval_expr(env, tokens[2])]
			let(env, *arguments)
			return
		if fst == "inc":
			inc(env, tokens[1])
			return
		if fst == "and":
			if not eval_expr(env, tokens[1]):
				return False
			return eval_expr(env, tokens[2])
		if fst == "or":
			fst_arg = eval_expr(env, tokens[1])
			if fst_arg:
				return fst_arg
			return eval_expr(env, tokens[2])
		if fst == "not":
			return not eval_expr(env, tokens[1])

	elif fst in env:

		# Built-ins & User Defined Functions
		if callable(env[fst]):
			arguments = [eval_expr(env, arg) for arg in tokens[1:]]
			return env[fst](env, *arguments)
		else:
			return env[fst]

	else:
		print(env)
		print("Expression", expression, type(expression))
		err("Bad term: {}".format(expression))

def tokenize(expression):
	if not expression:
		return []
	if expression[0] in ("'", "["):
		if len(expression) < 2:
			err("Unmatched quote")
		matching = "'" if expression[0] == "'" else "]"
		end_ind = 1 + expression[1:].find(matching)
		return [expression[0:end_ind+1]] + tokenize(expression[end_ind+1:].strip())
	if " " not in expression:
		return [expression]
	end_ind = expression.find(" ")
	return [expression[:end_ind]] + tokenize(expression[end_ind+1:].strip())

def extract_code(func_call):
	# Seperates whitespace from code and returns both
	lines = func_call.split("\n")
	code = []
	indents = []
	for line in lines:
		white_space, rest = re.match(r"\s*", line).group(), line.strip()
		if len(set(white_space)) > 1:
			err("Inconsistent use of spaces and tabs")
		elif len(set(white_space)) == 0:
			ind_lvl = 0
		elif white_space[0] == "\t":
			ind_lvl = len(white_space)
		elif white_space[0] == " ":
			ind_lvl = len(white_space)//4
		code.append(rest)
		indents.append(ind_lvl)
	return (code, indents)

def deparen(env, expression):
	# Finds and evaluates parenthetical expressions. Returns evaluated expression
	if "(" not in expression or ")" not in expression:
		return expression
	coords = [-1, -1]
	left = 0
	for i, c in enumerate(expression):
		if c == "(":
			left += 1
			if coords[0] == -1:
				coords[0] = i
		elif c == ")":
			left -= 1
			coords[1] = i
		if (coords[0] != -1 or coords[1] != -1) and left == 0:
			break
	evaluated_expression = phasify(eval_expr(env, expression[coords[0]+1:coords[1]]))
	new_expression = expression[:coords[0]] + evaluated_expression + expression[coords[1]+1:]
	return deparen(env, new_expression)

def user_func(env, func_body, args, *params):
	# Executes user defined function
	params = list(params)
	if len(args) != len(params):
		err("Incorrect number of arguments")
	else:
		copy_env = {key:val for key,val in env.items()}
		for param, arg in zip(params, args):
			let(copy_env, arg, param)
		return eval_func(copy_env, func_body)

def err(string):
	raise Exception("Error  - {}".format(string))

def load(fname):
	with open(fname) as f:
		return f.read()
def prn(env, string):
	print(phasify(string))

def repl():
	prog, next_line, ind_count = "", "", 0
	while True:
		whitespace = "\t" * ind_count
		next_line = whitespace + input(">> {}".format(whitespace))
		prog += next_line + "\n"	
		if next_line in ("quit", "exit"):
			break
		elif not next_line.strip() or (next_line[-1] != ":" and ind_count == 0):
			ret_val = eval_program(prog, return_prog_val=True)
			if ret_val != None:
				print(ret_val)
			prog, next_line, ind_count = "", "", 0
		elif next_line[-1] == ":":
			ind_count += 1

def temp():
	loc = """
	for (k ['hi' 1 2 3]):
		prn k
	"""
	eval_program(loc)


#repl()
#temp()










