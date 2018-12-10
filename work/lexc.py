import ply.lex as lex
import ply.yacc as yacc
import sys
import re
from clex import *

# Error handling rule
def t_error(t):
  print ("Illegal character "+str(t.value[0])+" at line "+str(t.lineno)+" at pos "+str(t.lexpos))
  t.lexer.skip(1)

REPLACE_STR = r'##{key}##|{key}##|##{key}|\b{key}\b'
def format_template(content,*keyvalue):
  content=content[1:]
  key_value_len=len(keyvalue)/2
  for index in range(key_value_len):
      key=keyvalue[index*2+0]
      value=keyvalue[index*2+1]
      re_str=REPLACE_STR.format(key=key)
      content=re.sub(re_str,value,content)
  return content

def add_reserved(var_toaken,var_literal):
  global tokens
  global reserved_map
  globals()['t_'+var_toaken]=var_literal
  tokens += (var_toaken)
  reserved_map[var_literal]=var_toaken