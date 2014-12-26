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


import modules.digraph as digraph
from test_source_codes import source_codes
import unittest

class HalfwaytreeTest(unittest.TestCase):

    def test_symbolic_execution(self):
        """
            This test does symbolic execution on all the test source codes
            and creates an image which shows all possible execution paths and
            the concrete values of independent variables which lead to each path's
            execution.
        """
        increment = 0
        for source_code in source_codes:

            #step1: get ast from source code
            source_code_digraph = digraph.SourceCodeDigraph(source_code=source_code,
                                                            show_node_id=True,
                                                            create_visual=True,
                                                            show_unmutated_constraints=True
                                                            )

            #step2: build code_call_graph while symbolically executing
            source_code_digraph.build_code_digraph()

            #draw the digraph
            output_digraph_test_image = "source-code-tests-images/source_code{0}.png".format(increment)
            source_code_digraph.visual_digraph.draw(output_digraph_test_image, prog='dot')

            increment += 1
            print "Output location: {0}".format(output_digraph_test_image)



unittest.main()
