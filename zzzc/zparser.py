from plyplus import Grammar, STransformer

# using C99 math grammar
zzz_grammar = Grammar("""

@start : add_expr ;

mul_op : '\*' | '/' ;
add_op : '\+' | '-' ;

mul_expr : (mul_expr mul_op)? atom ;
add_expr : (add_expr add_op)? mul_expr ;

atom : variable | number | neg | '\(' add_expr '\)' ;
neg : '-' atom ;

variable : 'waking_up' | 'falling_asleep' | 'awake' | 'asleep' ;
number : '[\d]+' ;

WS: '[ \t\n]+' (%ignore) (%newline);
""")

def augment_to_list(t):
	if type(t) is not type([]):
		t = [t]
	return t

def lapply(func, maybe_list_1, maybe_list_2=None):
	maybe_list_1 = augment_to_list(maybe_list_1)
	if maybe_list_2:
		maybe_list_2 = augment_to_list(maybe_list_2)
		#print("lapply:", maybe_list_1, maybe_list_2)
		return list( map(func, [ (x,y) for x in maybe_list_1 for y in maybe_list_2] ) )
	else:
		return list( map(func, [ x for x in maybe_list_1 ] ) )


from .util import SleepState

class ExprParser(STransformer):

	__default__ = lambda self, exp : exp.tail[0]

	def _bin_op(self, exp):
		#print("bin op:", exp.tail)
		if len(exp.tail) == 1:
			return exp.tail[0]

		arg1, op, arg2 = exp.tail

		if op == "+":
			return lapply( lambda x : x[0] + x[1], arg1, arg2 )
		elif op == "-":
			return lapply( lambda x : x[0] - x[1], arg1, arg2 )
		elif op == "*":
			return lapply( lambda x : x[0] * x[1], arg1, arg2 )
		elif op == "/":
			return lapply( lambda x : x[0] // x[1], arg1, arg2 )

		raise Error("no matching operation")

	add_expr = _bin_op
	mul_expr = _bin_op

	def neg(self, exp):
		return lapply(lambda x: -x, exp.tail[0])

	number = lambda self, exp : int(exp.tail[0])

	def variable(self, exp):
		#print("variable lookup: ", exp.tail[0] )
		return self.times[ SleepState[ exp.tail[0] ] ];


	def __init__(self, time_dict):
		self.times = time_dict

def get_parser(times_dict):
	return ( zzz_grammar, ExprParser(times_dict) )

