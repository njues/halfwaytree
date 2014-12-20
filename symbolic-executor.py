#-------------------------------------------------------------------------------
# Name:        symbolic-executor
# Purpose:
#
# Author:      HDizzle
#
# Created:     06/Sept/2014
# Copyright:   (c) HDizzle 2014
# Licence:     MIT
#-------------------------------------------------------------------------------
#!/usr/bin/env python


import ast
import modules.digraph as digraph

test_code1 = """
t       =4
var1    =10
var2    =9
if var1 > var2:
    print "okay1"
    print "okay2"
    print "okay3"

if t < 5:
    print "error"

print "done"

"""

test_code2 = """
t       =4
var1    =10
var2    =9
if var1 >= -30 and var1 <= 3000 and var1 > var2 and t==3 and t>5:
    print "okay1"
    print "okay2"
    print "okay3"


print "done"
"""

test_code3 = """

if var1 >= -30 and var1 <= 3000 and t==4:
    print "okay1"
    print "okay2"
    print "okay3"

print "done"
"""

test_code4 = """
if var1 == 30:
    print "okay1"
print "done"
"""

test_code5 = """
t       =4
var1    =10
var2    =9
if var1 > var2:
    print "okay1"
    print "okay2"
    print "okay3"

    if t < 5:
        var3 = 3
        print "error"

    print "okay4"

print "done"
"""

test_code6 = """
var1 = 50
if var1 != 30-p/b:
    var2=(7-9*var1)/var1
    print "okay1"
print "done"
"""

test_code7 = """
var1 = 2
var2 = -3
var1 = 2+var2
if var1>var2 and var1>0 and var2>-8:
    var1 = var1-2
    if var1 >0:
        print "okay"
        var1=-1000
    if var1 == -1000:
        var1 = var1 + 5
        print 'var1 < 0'
    print 'hi'
print 'end'
"""

test_code8 = """
var1 = 0
var2 = 0
var3 = 0
if var1==0:
    var1 = 0
    var2 = 0
    var3 = 0
print 'end'
"""

test_code9 = """
var1 = 0
var2 = 0
if var1 == 0:
    var1 = 1
    if var1 == 1:
        var2 = 1
var1 = 2
print 'end'
"""

#step1: get abstract syntax tree
abstract_syntax_tree = ast.parse(test_code8)

#step2: build code_call_graph while symbolically executing
source_code_digraph = digraph.SourceCodeDigraph(abstract_syntax_tree)
source_code_digraph.build_code_digraph()
#source_code_digraph.visual_digraph.draw('image.ps', prog='dot')
source_code_digraph.visual_digraph.draw('image.png', prog='dot')



