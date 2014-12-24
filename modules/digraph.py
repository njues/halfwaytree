#-------------------------------------------------------------------------------
# Name:         digraph
# Purpose:      Symbolic execution for Python applications
#
# Author:       HDizzle
# url:          https://github.com/sudouser2010/halfwaytree
# Created:      06/Sept/2014
# Copyright:    (c) HDizzle 2014
# License:      MIT
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import pygraphviz as pgv
import modules.astor as astor
import z3

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

    def __init__(self, abstract_syntax_tree, create_visual=True, show_unmutated_constraints=True,
                 show_node_id=True, use_html_like_label=True):
        """
            param abstract_syntax_tree: an ast object
        """
        self.abstract_syntax_tree       = abstract_syntax_tree
        self.node_count                 = 0
        self.create_visual              = create_visual
        self.show_unmutated_constraints = show_unmutated_constraints
        self.show_node_id               = show_node_id
        self.use_html_like_label        = use_html_like_label

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
            self.visual_digraph.get_node(node_id).attr.update(label=node_statement,
                                                              shape='box')
        except:
            #if node does not exist, then add it
            self.visual_digraph.add_node(node_id, label=node_statement)


    def connect_node_to_parent_node_on_visual_digraph(self, node_id, parent_node_id):
        """
            param node_id: int
            param prent_node_id: int
        """
        self.visual_digraph.add_edge(parent_node_id, node_id)

    def make_condition_symbolic(self, condition, node_variables):
        self.place_symbolic_variables_into_local_scope(node_variables, locals())
        exec("local_condition ={0}".format(condition))
        return  local_condition




    def extract_constraints_from_conditionals(self, conditions, node_variables):
        """
            param conditions: list
            this method takes a list of conditions and extracts constraints
        """

        if hasattr(conditions, 'values'):
            condition_values = conditions.values
        else:
            """
                condition.values is absent when there is only one constraint.
                In such cases, put that one constraint into a contraints array
                and handle it as usual
            """
            condition_values = [conditions]

        true_constraints = []
        """
            unmutated constraints show the original condition which is present in the
            code and it is a list of strings.
            contraints show the condition with expressed in terms of variables at
            a particular time/state and it is a list of z3 arithmetic boolean
        """
        unmutated_constraints   = []

        """
            false constraints are the negation of the true branch in an if statement.
            Pretty much, these are the contraints when the if statement is false
        """
        false_constraints    = []
        for condition in condition_values:
            condition = astor.to_source(condition)
            unmutated_constraints.append(condition)
            condition = self.make_condition_symbolic(condition, node_variables)
            true_constraints.append(condition)
            false_constraints.append(z3.Not(condition))

        return true_constraints, false_constraints, unmutated_constraints

    def flatten_constraints(self, constraints):
        """
            param constraints: has list of z3 arithmetic statements.
            loop gets the string representation of arithmetic
            and then adds it to a string
        """
        out = ""
        for item in constraints:
            if out=="":
                out = item.__str__()
            else:
                out = item.__str__() + "\n" + out

        return out

    def variable_is_type(self, variable, string_of_type):
        return type(variable).__name__ == string_of_type

    def place_symbolic_variables_into_local_scope(self,
                                         symbolic_variable_scope,
                                         local_scope):
        """
            the symbolic scope is a dictionary containing
            symbolic variables.
            the local scope is the dictionary containing
            the local variables.
            (passed by reference)
        """
        for key, value in symbolic_variable_scope.iteritems():
            local_scope[key] = value

    def place_local_variables_into_symbolic_scope(self,
                                         symbolic_variable_scope,
                                         local_scope):
        """
            the symbolic scope is updated with the changes that
            occurred in the local scope
            (passed by reference)
        """
        for key, value in symbolic_variable_scope.iteritems():
            symbolic_variable_scope[key] = local_scope[key]


    def update_node_variable_state(self, node, variables):

        if hasattr(node.value, 'n') and \
            self.variable_is_type(node.value.n, "int"):
            """
                when variable is defined/assigned as an integer,
                symbolically define it with z3
            """

            if node.targets[0].id in variables:
                """
                    if this variable is in scope,it's being redefined.
                    So make it concrete
                """
                variables[node.targets[0].id] = node.value.n
            else:
                """
                    if this variable is not in scope,it's being defined for the first time.
                    So make it symbolic
                """
                variables[node.targets[0].id] = z3.Int(node.targets[0].id)
        else:
            statement = astor.to_source(node)
            self.place_symbolic_variables_into_local_scope(variables, locals())
            exec(statement) #symbolic execution occurs here
            self.place_local_variables_into_symbolic_scope(variables, locals())

    def get_ast_statement_from_path(self, ast_path, ast):
        local_ast = ast
        for item in ast_path:
            if type(item).__name__ == 'int':
                local_ast = local_ast[item]
            else:
                local_ast = local_ast.body

        return local_ast

    def create_node_on_digraph(self, node_statement, node_id, parent_node_id, node_type):
        #---------------------------------create node if needed
        if self.create_visual:
            #add node to visual digraph
            self.add_node_to_visual_digraph(node_statement, node_id, node_type)

            if node_id > 0:
                #connect node to a parent digraph
                self.connect_node_to_parent_node_on_visual_digraph(node_id, parent_node_id)
        #---------------------------------create node if needed

    def get_ast_body_that_ast_path_is_in(self, ast_path, ast):

        last_element_in_ast_path = ast_path[-1]
        if type(last_element_in_ast_path).__name__ == 'int':
            #if path refers to a statement index inside body, then get body
            body_path = ast_path[:-1]
        else:
            #if the path already refers to a body
            body_path =  ast_path

        return self.get_ast_statement_from_path(body_path, ast)

    def get_number_of_statements_in_ast_body(self, ast_body):
        return len(ast_body)

    def there_is_an_ast_statement_below_in_same_body(self, ast_path, ast):
        """
            this code assumes the ast path refers to an ast statement
        """
        index_of_ast_statement = ast_path[-1]
        if type(index_of_ast_statement).__name__ != 'int':
            raise ValueError("index of ast statement must be and integer")

        ast_body = self.get_ast_body_that_ast_path_is_in(ast_path, ast)
        number_of_statements_in_ast_body = self.get_number_of_statements_in_ast_body(ast_body)

        return number_of_statements_in_ast_body > index_of_ast_statement+1


    def there_is_an_ast_statement_below_in_body_directly_above(self, ast_path, ast):
        """
            this code assumes the ast path refers to an ast statement
        """
        index_of_ast_statement = ast_path[-1]
        if type(index_of_ast_statement).__name__ != 'int':
            raise ValueError("index of ast statement must be and integer")

        if len(ast_path) >= 3:
            """
                remove the body and the index of the statement inside
                if statement body.
                ie: if ast_path was [1, 'b', 2], then it becomes [1]
            """
            ast_path = ast_path[0:-2]
            index_of_ast_statement = ast_path[-1]
            ast_body = self.get_ast_body_that_ast_path_is_in(ast_path, ast)
            number_of_statements_in_ast_body = self.get_number_of_statements_in_ast_body(ast_body)
            return number_of_statements_in_ast_body > index_of_ast_statement+1
        else:
            """
                otherwise, there is no ast_body above this one, return false
            """
            return False

    def remove_last_two_items_in_list_by_reference(self, local_list):
        for x in range(0, 2):
            del local_list[-1]

    def there_is_an_ast_statement_below_in_any_ast_body_above(self, ast_path, ast):
        ast_body_exists = False
        while len(ast_path)>2 and not ast_body_exists:
            """
                stop loop when the ast_path len is < 2
                or when ast_body_exists is true
            """
            if self.there_is_an_ast_statement_below_in_body_directly_above(ast_path, ast):
                ast_body_exists = True

            self.remove_last_two_items_in_list_by_reference(ast_path)

        return ast_body_exists

    def add_node_from_ast_statements_inside_if_statement_body(self, ast=None, ast_path=None, node_state=None,
                                                        node_id=None, node_children=None):
        """
            code assumes current ast_path refers to an if statment
        """
        ast_path += ['b', 0]
        node_children.append(
            self.return_node_and_all_its_children(ast=ast, ast_path=ast_path, node_state=node_state,
                                              parent_node_id=node_id )
        )


    def add_node_from_ast_statements_below_in_same_body(self, ast=None, ast_path=None, node_state=None,
                                                        node_id=None, node_children=None):
        if self.there_is_an_ast_statement_below_in_same_body(ast_path, ast):
            ast_path[-1] += 1
            node_children.append(
                self.return_node_and_all_its_children(ast=ast, ast_path=ast_path, node_state=node_state,
                                                  parent_node_id=node_id )
            )

    def variable_is_symbolic(self, variable_as_string, node_state):
        """
            this function assumes two things,
            (1) value of variable being tracked is symbolic or int
            (2) variable_as_string key exists in node_state dictionary
        """
        return type(node_state['variables'][variable_as_string]).__name__ != 'int'

    def get_concrete_value_of_variable_as_string(self, variable, node_state, z3_solutions):
        if self.variable_is_symbolic(variable, node_state):
            return str(z3_solutions[node_state['variables'][variable]])
        else:
            return str(node_state['variables'][variable])

    def get_solutions(self, z3_solutions, node_state):
        solution = ""
        for variable in node_state['variables']:
            if solution == "":
                solution = str(variable) + " = " + \
                           self.get_concrete_value_of_variable_as_string(variable, node_state, z3_solutions)
            else:
                solution = solution + ", " + str(variable) + " = " + \
                           self.get_concrete_value_of_variable_as_string(variable, node_state, z3_solutions)


        return solution


    def is_statement_on_root_body(self, ast_path):
        return len(ast_path) == 1

    def is_statement_the_last(self, ast_path, ast):

        if self.is_statement_on_root_body(ast_path):
            if not self.there_is_an_ast_statement_below_in_same_body(ast_path, ast):
                return True
            return False

        if not self.there_is_an_ast_statement_below_in_any_ast_body_above(ast_path, ast):
            return True
        return False


    def calculate_concrete_variables_on_last_statement(self, node_state, ast_path, ast, node_statement):

        if self.is_statement_the_last(ast_path, ast):
            #if this ast body has no statement below

            if len(ast_path)==1:
                #if this statement is on the root ast_body
                s = z3.Solver()
                s.add(node_state['constraints'])
                is_satisfied    = s.check()

                if is_satisfied.r == 1:
                    #if path conditions are satisfiable
                    string_solutions = self.get_solutions(s.model(), node_state)
                else:
                    string_solutions = "path unsatisfiable"

                node_statement += "\n[font color='red']{0}[/font]".format(string_solutions)

        return node_statement


    def add_node_from_ast_statements_below_in_any_ast_body_above(self, ast=None, ast_path=None, node_state=None,
                                                        node_id=None, node_children=None):

        if self.there_is_an_ast_statement_below_in_same_body(ast_path, ast):
            """
                this function should only be used at the bottom of an ast_body
            """
            return

        if self.there_is_an_ast_statement_below_in_any_ast_body_above(ast_path, ast):
            #increment last index in path, to go to the next statement
            ast_path[-1] += 1
            node_children.append(
                self.return_node_and_all_its_children(ast=ast, ast_path=ast_path, node_state=node_state,
                                                  parent_node_id=node_id )
            )

    def get_node_statement_from_constraints(self, unmutated_constraints, node_state):
        if self.show_unmutated_constraints:
            node_statement = self.flatten_constraints(unmutated_constraints)
        else:
            node_statement = self.flatten_constraints(node_state['constraints'])

        return node_statement

    def modify_node_statement(self, node_statement, node_id):
        if self.show_node_id:
            node_statement = "Node "+node_id.__str__() + ":\n" + node_statement

        if self.use_html_like_label:
            node_statement = node_statement.replace('<','&lt;')
            node_statement = node_statement.replace('>','&gt;')
            node_statement = node_statement.replace('[','<')
            node_statement = node_statement.replace(']','>')
            node_statement = node_statement.replace('\n','<br/>')

        node_statement = "<"+node_statement+">"
        return node_statement

    def build_true_and_false_node_states_from_constraints(self, node_state,
                                                                         true_constraints,
                                                                         false_constraints):

        true_node_state     = self.get_copy_of_node_state(node_state) #copy by value
        false_node_state    = node_state    #copy by reference
        true_node_state['constraints']  = true_node_state['constraints']    + true_constraints
        false_node_state['constraints'] = false_node_state['constraints']   + false_constraints

        return true_node_state, false_node_state

    def get_copy_of_node_state(self, node_state):
        node_state_copy = {'variables':{}, 'constraints':[]}

        #get copy of node_state variables
        for key, value in node_state['variables'].iteritems():
            node_state_copy['variables'][key] = value

        #get copy of node_state constraints
        for value in node_state['constraints']:
            node_state_copy['constraints'].append(value)

        return node_state_copy


    def return_node_and_all_its_children(self, ast=None, ast_path=None,
                                          node_state=None, parent_node_id=None):
        """
            This method returns node and all its siblings.
            It sends the state of the previous node_state down to the child node.
            The node_state contains the parent's constraints and variable_state

            definitions:

        """
        if ast_path == None:
            ast_path    = [0]
            node_state  = {'constraints':[], 'variables':{}}
        ast_statement    = self.get_ast_statement_from_path(ast_path, ast)

        #-------------------------initialize stuff for digraph node
        node_type           = type(ast_statement).__name__
        node_statement      = ""
        node_children       = []
        node_id             = self.node_count
        self.node_count += 1
        #-------------------------initialize stuff for digraph node

        if      node_type == "Assign":
            node_statement = astor.to_source(ast_statement)
            self.update_node_variable_state(ast_statement, node_state['variables'])
        elif    node_type == "Print":
            node_statement = astor.to_source(ast_statement)
        elif    node_type == "If":
            """
                add true branch of if statement,
                code adds statements inside if body
            """
            true_constraints, false_constraints, unmutated_constraints = \
                self.extract_constraints_from_conditionals(ast_statement.test, node_state['variables'])

            true_node_state, false_node_state = \
                self.build_true_and_false_node_states_from_constraints(node_state,
                                                                       true_constraints,
                                                                       false_constraints
                )

            node_statement = self.get_node_statement_from_constraints(unmutated_constraints, true_node_state)

            self.add_node_from_ast_statements_inside_if_statement_body(ast, list(ast_path), true_node_state,
                                                                       node_id, node_children)
            """
                the following line makes the node_state equal to the false_node_state to
                represent the branch of code executed if the if-statement conditions
                were false.
            """
            node_state = false_node_state



        node_statement = self.calculate_concrete_variables_on_last_statement(node_state, list(ast_path),
                                                                             ast, node_statement)
        node_statement = self.modify_node_statement(node_statement, node_id)

        self.create_node_on_digraph(node_statement, node_id, parent_node_id, node_type)

        self.add_node_from_ast_statements_below_in_same_body(ast, list(ast_path), node_state, node_id, node_children)

        self.add_node_from_ast_statements_below_in_any_ast_body_above(ast, list(ast_path), node_state, node_id, node_children)



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

        self.digraph    = self.return_node_and_all_its_children(ast=self.abstract_syntax_tree.body)
