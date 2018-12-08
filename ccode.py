# Declare the state
states = (
  ('ccode','exclusive'),
)

# Match the first {. Enter ccode state.
def t_ccode(t):
    r'\{'
    t.lexer.code_start = t.lexer.lexpos        # Record the starting position
    t.lexer.level = 1                          # Initial brace level
    t.lexer.begin('ccode')                     # Enter 'ccode' state

# Rules for the ccode state
def t_ccode_lbrace(t):     
    r'\{'
    t.lexer.level +=1                

def t_ccode_rbrace(t):
    r'\}'
    t.lexer.level -=1

    # If closing brace, return the code fragment
    if t.lexer.level == 0:
         t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos+1]
         t.type = "CCODE"
         t.lexer.lineno += t.value.count('\n')
         t.lexer.begin('INITIAL')           
         return t

# C or C++ comment (ignore)    
def t_ccode_comment(t):
    r'(/\*(.|\n)*?*/)|(//.*)'
    pass

# C string
def t_ccode_string(t):
   r'\"([^\\\n]|(\\.))*?\"'

# C character literal
def t_ccode_char(t):
   r'\'([^\\\n]|(\\.))*?\''

# Any sequence of non-whitespace characters (not braces, strings)
def t_ccode_nonspace(t):
   r'[^\s\{\}\'\"]+'

# Ignored characters (whitespace)
t_ccode_ignore = " \t\n"

# For bad characters, we just skip over it
def t_ccode_error(t):
    t.lexer.skip(1)