Halfwaytree
===========

###Symbolic execution for Python applications

###What Is Symbolic Execution ?
    Symbolic execution is a method for automatically generating test 
    cases from a computer program. Some great introductory videos 
    on symbolic execution are below:
    [https://www.youtube.com/watch?v=CJccn9d2t5w](https://www.youtube.com/watch?v=CJccn9d2t5w)
    [https://www.youtube.com/watch?v=mffhPgsl8Ws](https://www.youtube.com/watch?v=mffhPgsl8Ws)

###About Halfwaytree
    Right now, Halfwaytree is only in its infancy (phase two of development). 
    This project is a proof of concept I use for my dissertation research. 
    You're welcome to help me extend it and bring it to the next level.

###Why Use Halfwaytree ?
    Once the dependencies are installed, it can be used simply by importing 
    a module. The emphasis of Halfwaytree is simplicity so you can focus on 
    testing your code. See the read me file inside the doc folder to see 
    how to install Halfwaytree's dependencies.

###Example Usage

```
import modules.digraph as digraph

example1 = """
x=0
y=0
z=2*y
if z==x:
    if x>y+10:
        print "ERROR !"
"""

#Step1, initialize digraph object with source code
source_code_digraph = digraph.SourceCodeDigraph(source_code=example1)

#Step2, build digraph while symbolically executing
source_code_digraph.build_code_digraph()

#Step3, [optional] draw the digraph image
source_code_digraph.visual_digraph.draw("example.png", prog='dot')
```
###Generated image of execution tree:
![Alt text](https://raw.githubusercontent.com/sudouser2010/halfwaytree/master/tests/source-code-tests-images/single_source_code.png "Optional title attribute") 
