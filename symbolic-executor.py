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


#step1: get ast from source code
source_code_digraph = digraph.SourceCodeDigraph(source_code=source_codes[0],
                                                show_node_id=True,
                                                create_visual=True,
                                                show_unmutated_constraints=True
                                                )
#step2: build code_call_graph while symbolically executing
source_code_digraph.build_code_digraph()

#source_code_digraph.visual_digraph.draw('image.ps', prog='dot')
source_code_digraph.visual_digraph.draw('image.png', prog='dot')



