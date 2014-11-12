# -*- coding: utf-8 -*-
"""
Created on Thu Oct 23 15:51:31 2014

@author: pavla
"""

from ply import lex, yacc

keywords = {
   "en" : "EN",
   "du" : "DU",
   "ex" : "EX",
   "entry" : "ENTRY",
   "during" : "DURING",
   "exit" : "EXIT"
}

tokens = (["WHITESPACE", "AL_NUM", "OTHER"] + list(keywords.values()))

literals = ",;:"

t_WHITESPACE = r"\s+"

def t_AL_NUM(t):
    r"\w+"
    t.type = keywords.get(t.value, "AL_NUM")
    return t

t_OTHER = r"[^\s,;:\w]+"

def t_error(t):
    raise TypeError("Unknown text '%s'" % t.value)

def p_start(p):
    "start : ws label"
    p[0] = p[2]

def p_label(p):
    """label : keywords actions label
             | empty"""
    if len(p) == 4:
        if p[3] == None:
            p[0] = [[p[1], p[2]]]
        else:
            p[0] = [[p[1], p[2]]] + p[3]
    else:
        p[0] = p[1]

def p_empty(p):
    "empty :"
    pass

def p_ws(p):
    """ws : WHITESPACE
          | empty"""
    p[0] = p[1]

def p_keywords(p):
    """keywords : keyword separator keyword
                | keyword ws ':'"""
    if p[3] != ':':
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_keyword(p):
    """keyword : EN
               | DU
               | EX
               | ENTRY
               | DURING
               | EXIT"""
    p[0] = p[1]

def p_separator(p):
    """separator : ws ',' ws
                 | ws ';' ws"""
    p[0] = p[2]

def p_actions(p):
    """actions : AL_NUM actions
               | WHITESPACE actions
               | ',' actions
               | ';' actions
               | ':' actions
               | OTHER actions
               | AL_NUM
               | WHITESPACE
               | ','
               | ';'
               | ':'
               | OTHER"""
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]

def p_error(p):
    if p is None:
        raise ValueError("Unknown error")
    raise ValueError("Syntax error, line {0}: {1}".format(p.lineno, p.type))

lexer = lex.lex()
parser = yacc.yacc()

def parse(text, lexer=lexer):
    return parser.parse(text, lexer)
