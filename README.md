Halfwaytree
===========

###Symbolic execution for Python applications

###What Is Symbolic Execution ?
    Symbolic execution is a method for automatically generating test 
    cases from a computer program. Some great introductory videos 
    on symbolic execution are below:
[Symbolic Execution Introductory video1](https://www.youtube.com/watch?v=CJccn9d2t5w)<br>
[Symbolic Execution Introductory video2](https://www.youtube.com/watch?v=mffhPgsl8Ws)

###About Halfwaytree
    Right now, Halfwaytree is only in its infancy (phase two of development). 
    This project is a proof of concept I use for my dissertation research. 
    You're welcome to help me extend it and bring it to the next level. I'm
    looking for someone to help write unittests.

###Why Use Halfwaytree ?
    Once the dependencies are installed, it can be used simply by importing 
    a module. The emphasis of Halfwaytree is simplicity so you can focus on 
    testing your code. See the read me file inside the doc folder to see 
    how to install Halfwaytree's dependencies.

###How To Install
[How to install Halfwaytree without Vagrant](https://github.com/sudouser2010/halfwaytree/blob/master/install-instructions.md)<br>
[How to install Halfwaytree with Vagrant](https://github.com/sudouser2010/halfwaytree/blob/master/install-instructions-with-vagrant.md)

###Example Usage

```
import modules.digraph as digraph

example1 = """
x=0
y=0
z=2*y
if z==x:
    if x>y+10:
        assert False
"""

#Step1, initialize digraph object with source code
source_code_digraph = digraph.SourceCodeDigraph(source_code=example1)

#Step2, build digraph while symbolically executing
source_code_digraph.build_code_digraph()

#Step3, [optional] draw the digraph image
source_code_digraph.visual_digraph.draw("example.png", prog='dot')
```
###Example Output:
![image generated with Halfwaytree](https://raw.githubusercontent.com/sudouser2010/halfwaytree/master/tests/source-code-tests-images/example1.png "image generated with Halfwaytree") 


    From the output of example1 (above), you can see that 
    the "inputs of death" for this program are x=22 and y=11.

###Current Limitations of Code:
####source code analyzed has the following restrictions:
    1. Statements must be one of the following:
        * assignment, if, print, or assert False
    2. If statement can only have a single conditional or multiple conditionals joined with 'and'
    3. Data type of variables must be an integer
