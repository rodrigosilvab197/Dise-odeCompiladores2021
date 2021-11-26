import ply.yacc as yacc
from node import Node
from tac import GeneratorTac
from lexer import *

def whiledeX(x):
    x[0] = Node('while', [x[3], x[6]])
def conddeX(x):
    x[0] = Node('if', [x[3], x[6]])
    if x[8]:
        x[0].children.append(x[8])
    if p[9]:
        x[0].children.append(x[9])
def errordeX(x):
    raise(Exception(x))
def elifsdeX(x):
    if len(x) > 2:
        x[0] = Node('elif', [x[3], x[6]])
        if x[8]:
            x[0].children.append(x[8])


def elseX(x):
    if len(x) > 2:
        x[0] = Node('else', [x[3]])

def bloque(x):
    if len(x) == 3:
        x[0] = Node('bloque', [x[1], x[2]])
    elif x[1]:
        x[0] = x[1]



def declaraciondeX(x):
    if len(x) == 4:
        x[0] = Node('declaracion', [x[1], x[2]])
    else:
        x[0] = Node('delcaracionAsignada', [x[1], x[2], x[4]])


def typedeX(x):
    x[0] = x[1]


def exprdeX(x):
    x[0] = x[1]

def compdeX(x):
    x[0] = x[1]


def boolopdeX(x):
    x[0] = x[1]

def boolexprBoolX(x):
    if x[1] == '(':
        x[0] = Node('bool', [x[2]])
    elif len(x) == 2:
        x[0] = Node('bool', [x[1]])
    else:
        x[0] = Node('boolop', [x[1], x[2], x[3]])


def boolexprNumdeX(x):
    x[0] = Node('numcomp', [x[1], x[2], x[3]])


def boolconstdeX(x):
    x[0] = x[1]

def numexprdeX(x):
    if x[1] == '(':
        x[0] = Node('num', x[2])
    if len(x) == 2:
        x[0] = Node('num', x[1])
    else:
        x[0] = Node('numop', [x[1], x[2], x[3]])


def numopdeX(x):
    x[0] = x[1]


def strexprdeX(x):
    if len(x) == 4:
        x[0] = Node('concat', [x[1], x[3]])
    elif len(x) == 5:
        x[0] = Node('strcast', [x[3]])
    else:
        x[0] = Node('str', [x[1]])


def assigndeX(x):
    x[0] = Node('assign', [x[1], x[3]])

def emptydeX(x):
    pass


def stmtdeX(x):
    x[0] = x[1]
    
parser = yacc.yacc()
resNode = parser.parse(lexer=lexer, input=open("program.txt").read())
print("Compiled succesfully")
generator = GeneratorTac()
generator.tacGenerator(resNode)
f = open('program_output.txt', 'w')
f.write(generator.tac_str)
f.close()
