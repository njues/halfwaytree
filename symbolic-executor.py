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


class Node:
    def __init__(self, type, statement, contraints, solutions, children):
        """
            param type: string
            param statement: string
            param constraints: list
            param solution: list
        """

        self.type           = type
        self.statement      = statement
        self.constraints    = contraints
        self.solutions      = solutions
        self.children       = children

class SourceCodeDigraph:
    """
        This is a directed graph of the source code
    """

    def __init__(self, abstract_syntax_tree):
        """
            param abstract_syntax_tree: an ast object
        """
        self.abstract_syntax_tree = abstract_syntax_tree

    def return_digraph_segment_from_body(self, body):
        local_digraph = []
        for index, item in enumerate(body):
            local_type          = type(item).__name__
            local_statement     = "{0}={1}".format(item.targets[0].id, item.value.n)
            local_contraints    = []
            local_solutions     = []
            local_digraph.append(Node(local_type, local_statement, local_contraints, local_solutions))
            a=1

    def return_node_and_all_its_children(self, this_index, this_body, parent_index = None, parent_body = None):
        """
            method returns node and all its siblings
        """
        node                = this_body[this_index]
        node_type           = type(node).__name__
        node_contraints     = []
        node_solutions      = []
        node_children       = []
        node_statement      = ""


        if node_type == "Assign":
            node_statement = "{0}={1}".format(node.targets[0].id, node.value.n)
            node_children.append(self.return_node_and_all_its_children(this_index+1, this_body))
        elif node_type == "if":
            """
                add true branch of if statement,
                code adds statements inside if body
            """
            node_children.append(self.return_node_and_all_its_children(0, node.body, this_index, this_body))

            if parent_index+1  <= len(parent_body):
                """
                    add false branch of if statement,
                    here code skips over entire if body
                """
                node_children.append(self.return_node_and_all_its_children(parent_index+1, parent_body))

        if( this_index+1    >= len(this_body) and
            parent_index    != None and
            parent_index+1  <= len(parent_body)):
            """
                if inner branch is exhausted, then add node from outer branch as child.
                When inner branch is finished, continue adding
            """
            node_children.append(self.return_node_and_all_its_children(parent_index+1, parent_body))


        return Node(node_type, node_statement, node_contraints, node_solutions, node_children)



    def build_code_digraph(self):
        """
            the digraph consists of the root node and all its siblings
        """
        self.digraph    = self.return_node_and_all_its_children(0, abstract_syntax_tree.body)

        a=1

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





import ast

#step1: get abstract syntax tree
abstract_syntax_tree = ast.parse(test_code1)

#step2: build code_call_graph
source_code_digraph = SourceCodeDigraph(abstract_syntax_tree)
source_code_digraph.build_code_digraph()
a=1


#exec(compile(abstract_syntax_tree, filename="<ast>", mode="exec"))











