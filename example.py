#-------------------------------------------------------------------------------
# Name:         Halfwaytree
# Purpose:      Symbolic execution for Python applications
#
# Author:       HDizzle
# url:          https://github.com/sudouser2010/halfwaytree
# Created:      06/Sept/2014
# Copyright:    (c) HDizzle 2014
# License:      MIT
#
#See test folder for more examples
#-------------------------------------------------------------------------------
#!/usr/bin/env python


import modules.digraph as digraph

example1 = """
var1=2
assert False
if var1 == 30:
    print "okay1"
"""

example2 = """
x=0
y=0
z=2*y
if z==x:
    if x>y+10:
        assert False
"""

example3 = """
var1=0
if var1 == 30 and var1 != 30:
    print "this path is infeasible"
"""

#Step1, initialize digraph object with source code
source_code_digraph = digraph.SourceCodeDigraph(source_code=example3)

#Step2, build digraph while symbolically executing: uses
source_code_digraph.build_code_digraph()

#Step3, [optional] draw the digraph image
source_code_digraph.visual_digraph.draw("example.png", prog='dot')

#print source_code_digraph.test_cases
