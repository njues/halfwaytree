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
    def __init__(self, type, statement, contraints, solutions, children, node_id):
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
        self.node_id        = node_id

class SourceCodeDigraph:
    """
        This is a directed graph of the source code
    """

    def __init__(self, abstract_syntax_tree, create_visual = True):
        """
            param abstract_syntax_tree: an ast object
        """
        self.abstract_syntax_tree   = abstract_syntax_tree
        self.node_count             = 0
        self.create_visual          = create_visual

    def index_exists(self, index, list):
        """
            param list: list
            param index: int
            this returns true if the list[index] exists
        """

        if len(list) > index:
            return True
        return False

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
        node_id             = self.node_count

        self.node_count += 1


        if      node_type == "Assign":
            node_statement = "{0}={1}".format(node.targets[0].id, node.value.n)
        elif    node_type == "Print":
            node_statement = 'print "{0}"'.format(node.values[0].s)
        elif    node_type == "If":
            """
                add true branch of if statement,
                code adds statements inside if body
            """
            node_children.append(self.return_node_and_all_its_children(0, node.body, this_index, this_body))


        if self.index_exists(this_index+1, this_body):
            #if the index exists in this body, add it as a child
            node_children.append(self.return_node_and_all_its_children(this_index+1, this_body, parent_index, parent_body))
        else:
            #here when at the end of the this body
            if parent_body != None and self.index_exists(parent_index+1, parent_body):
                #if the parent boy has more node, then start adding nodes from the parent body
                node_children.append(self.return_node_and_all_its_children(parent_index+1, parent_body))


        return Node(node_type, node_statement, node_contraints, node_solutions, node_children, node_id)



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











