#-------------------------------------------------------------------------------
# Name:        digraph
# Purpose:
#
# Author:      HDizzle
#
# Created:     06/Sept/2014
# Copyright:   (c) HDizzle 2014
# Licence:     MIT
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import pygraphviz as pgv
import modules.astor as astor

class Node:
    def __init__(self, type, statement, state, children, node_id):
        """
            param type: string
            param statement: string
            param state: dictionary
            param children: list of nodes
            param node_id: int
        """

        self.type           = type
        self.statement      = statement
        self.state          = state
        self.children       = children
        self.node_id        = node_id


class SourceCodeDigraph:
    """
        This is a directed graph of the source code
    """

    def __init__(self, abstract_syntax_tree, create_visual=True):
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

    def add_node_to_visual_digraph(self, node_statement, node_id, node_type):
        """
            param node_statement: string
            param node_id: int
            param node_type: string
        """
        try:
            """
                if node already exists. This may occur because the children of this node
                were created first and referred to the parent which created the parent
                before this point
            """
            self.visual_digraph.get_node(node_id).attr.update(label=node_statement, shape='box')
        except:
            #if node does not exist, then add it
            self.visual_digraph.add_node(node_id, label=node_statement)


    def connect_node_to_parent_node_on_visual_digraph(self, node_id, parent_node_id):
        """
            param node_id: int
            param prent_node_id: int
        """
        self.visual_digraph.add_edge(parent_node_id, node_id)

    def extract_constraints_from_conditionals(self, conditions):
        """
            param conditions: list
            this method takes a list of conditions and extracts constraints
        """

        if hasattr(conditions, 'values'):
            condition_values = conditions.values
        else:
            """
                condition.values is false when there is only one constraint.
                In such cases, put that one constraint into a contraints array
                and handle it as usual
            """
            condition_values = [conditions]

        constraints = []
        for condition in condition_values:
            constraints.append(astor.to_source(condition))

        return constraints

    def flatten_constraints(self, constraints):
        """
            param constraints: list
            this joins all the constraints into one list
        """
        return "\n".join(constraints)

    def update_node_variable_state(self, node, variables):
        variables[node.targets[0].id] = astor.to_source(node.value)
        pass

    def return_node_and_all_its_children(self, this_index, this_body, parent_index = None,
                                         parent_body = None, parent_node_id = 0,
                                         node_state = None):
        """
            This method returns node and all its siblings.
            It sends the state of the previous node down to the child node.
            The state contains the parent's constraints and variable_state
        """
        node                = this_body[this_index]
        node_type           = type(node).__name__
        node_statement      = ""
        if node_state == None:
            node_state          = {'constraints':[], 'variables':{}}
        node_children       = []
        node_id             = self.node_count

        self.node_count += 1


        if      node_type == "Assign":
            node_statement = astor.to_source(node)
            self.update_node_variable_state(node, node_state['variables'])
        elif    node_type == "Print":
            node_statement = astor.to_source(node)
        elif    node_type == "If":
            """
                add true branch of if statement,
                code adds statements inside if body
            """
            node_state['constraints'] = self.extract_constraints_from_conditionals(node.test)
            node_statement = self.flatten_constraints(node_state['constraints'])
            node_children.append(self.return_node_and_all_its_children(0, node.body, this_index, this_body, node_id))

        #---------------------------------create node if needed
        if self.create_visual:
            #add node to visual digraph
            self.add_node_to_visual_digraph(node_statement, node_id, node_type)

            if node_id > 0:
                #connect node to a parent digraph
                self.connect_node_to_parent_node_on_visual_digraph(node_id, parent_node_id)
        #---------------------------------create node if needed

        if self.index_exists(this_index+1, this_body):
            #if the index exists in this body, add it as a child
            node_children.append(
                self.return_node_and_all_its_children(this_index+1, this_body,
                                                      parent_index, parent_body,
                                                      node_id, node_state=node_state))
        else:
            #here when at the end of the this body
            if parent_body != None and self.index_exists(parent_index+1, parent_body):
                #if the parent boy has more node, then start adding nodes from the parent body
                node_children.append(
                    self.return_node_and_all_its_children(parent_index+1, parent_body,
                                                          parent_node_id=node_id, node_state=node_state))

        return Node(node_type, node_statement, node_state, node_children, parent_node_id)



    def build_code_digraph(self):
        """
            the digraph consists of the root node and all its siblings
        """

        if self.create_visual:
            self.visual_digraph = pgv.AGraph(strict=False, directed=True)
            self.visual_digraph.layout(prog='dot')
            self.visual_digraph.graph_attr['label']='State Space of Code'
            self.visual_digraph.node_attr['shape']='rectangle' #circle, rectangle | box,

        self.digraph    = self.return_node_and_all_its_children(0, self.abstract_syntax_tree.body)
