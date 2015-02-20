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

example4 = """
left=0
right=0
op=0
result=0
#----------------represents errors caused by input number memory restrictions
if left > 1000:
    print "Input can not be greater than 1000"
    assert False
if left < -1000:
    print "Input can not be less than 1000"
    assert False
if right > 1000:
    print "Input can not be greater than 1000"
    assert False
if right < -1000:
    print "Input can not be less than 1000"
    assert False
#----------------represents errors caused by input number memory restrictions


if op == 0:
    #when op is +
    result = left + right

    #----------------represents error due to bad code
    if result == 231:
        assert False
    #----------------represents error due to bad code

if op == 1:
    #when op is -
    #----------------represents error due to bad code
    if left == 45 and right == -342:
        assert False
    #----------------represents error due to bad code
    result = left - right

if op == 2:
    #when op is *
    #----------------represents error due to bad code
    if left > 2*right - 34:
        assert False
    #----------------represents error due to bad code

    result = left * right

if op == 3:
    #when op is /
    #----------------represents error due to bad code
    if right == 791:
        assert False
    #----------------represents error due to bad code

    #-------------------represents errors caused by division by zero
    if right == 0:
        print "Error: Can not divide by zero"
        assert False
    #-------------------represents errors caused by division by zero

    result = left / right

if op == 4:
    #---represents errors caused by operations not covered by calculator
    print "Invalid Operation"
    assert False
    #---represents errors caused by operations not covered by calculator



#----------------represents errors caused by output number memory restrictions
if result > 1000:
    print "Output can not be greater than 1000"
    assert False
if result < -1000:
    print "Output can not be less than -1000"
    assert False
#----------------represents errors caused by output number memory restrictions

"""


#Step1, initialize digraph object with source code
source_code_digraph = digraph.SourceCodeDigraph(source_code=example4)

#Step2, build digraph while symbolically executing: uses
source_code_digraph.build_code_digraph()

#Step3, [optional] draw the digraph image
source_code_digraph.visual_digraph.draw("example.png", prog='dot')

#print source_code_digraph.test_cases
