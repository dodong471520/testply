import ply.lex as lex
#
# List of token names.   This is always required
tokens = [
   'NUMBER',
   'PLUS',
   'MINUS',
   'MULT',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'COMMA',
   'ID',
   'SEMICOLON',
   'LEFTBRACE',
   'RIGHTBRACE',
   'ASSIGN',
   'EQUAL',
   'STRING_LITERAL',
]
reserved={
    'while' : 'WHILE',
    'else' : 'ELSE',
    'if' : 'IF',
    'for' : 'FOR',
    'switch':'SWITCH',
    'case':'CASE',
    'do' : 'DO',
    'break': 'BREAK',
    'return' : 'RETURN',
    'int' : 'INT',
    'float' : 'FLOAT',
    'double' : 'DOUBLE',
    'continue' : 'CONTINUE',
    'struct' : 'STRUCT',
    'union' : 'UNION',
    'char' : 'CHAR',
    'printf':'PRINTF',
    'scanf' : 'SCANF',
}
tokens += reserved.values()
# Regular expression rules for simple tokens
t_CONTINUE = r'continue'
t_CASE = r'case'
t_ELSE = r'else'
t_BREAK = r'break'
t_INT = r'int'
t_SCANF = r'scanf'
t_UNION = r'union'
t_PRINTF = r'printf'
t_CHAR = r'char'
t_ASSIGN = r'='
t_EQUAL = r'=='
t_LEFTBRACE = r'{'
t_RIGHTBRACE = r'}'
t_PLUS = r'\+'
t_MINUS   = r'-'
t_MULT   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_COMMA = r','
t_SEMICOLON = r';'
t_FOR = r'for'
t_WHILE = r'while'
t_SWITCH = r'switch'
t_STRUCT = r'struct'
t_RETURN = r'return'
t_IF = r'if'
t_DO = r'do'
t_FLOAT = 'float'
t_DOUBLE = r'double'
t_STRING_LITERAL = r'"(\\.|[^\\"])*"'
# A regular expression rule with some action code
#
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[ t.value ]
    return t
#
def t_NUMBER(t):
  r'\d+(\.\d*)?'
  try:
    t.value = int(t.value)
  except ValueError:
    print("Line %d: Number %s is too large!" ,(t.lineno,t.value))
    t.value = 0
  return t
#
# Define a rule so we can track line numbers
def t_newline(t):
  r'\r?\n'
  t.lexer.lineno += 1

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
  print ("Illegal character "+str(t.value[0])+" at line "+str(t.lineno)+" at pos "+str(t.lexpos))
  t.lexer.skip(1)

def t_COMMENT(t):
    r'//.*'
    pass
# No return value. Token discarded
# Build the lexer


# # Test it out
# data = "3 + 4"
# data1="int gcd(int u, int v){ if(v==2) return u; else return gcd(v,u-u/v*v);}"
# # Give the lexer some input
# lexer.input(data)

# # Tokenize
# while 1:
#    tok = lexer.token()
#    if not tok: break      # No more input
#    print("This is a token: (" , tok.type,", ",tok.value,")")
