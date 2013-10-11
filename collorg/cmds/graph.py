#!/usr/bin/env python
#-*- coding: utf-8 -*-

### This file is part of collorg

### collorg is free software: you can redistribute it and/or modify
### it under the terms of the GNU General Public License as published by
### the Free Software Foundation, either version 3 of the License, or
### (at your option) any later version.

### This program is distributed in the hope that it will be useful,
### but WITHOUT ANY WARRANTY; without even the implied warranty of
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.

### You should have received a copy of the GNU General Public License
### along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import networkx as nx
try:
    import matplotlib.pyplot as plt
except:
    print("You must install matplotlib to use cog graph")
    sys.exit()
import argparse
from collorg.controller.controller import Controller

class Cmd():
    def __init__(self, controller, *args):
        self.__ctrl = controller
        if self.__ctrl is None:
            self.__ctrl = Controller()
        self.__parse_args()
        self.__draw()

    def __parse_args(self):
        parser = argparse.ArgumentParser(prog="cog graph")
        parser.add_argument(
            "-s", "--schema_name", help = "restrict graph to a schema")
        self.__args = parser.parse_args()

    def __draw(self):
        db = self.__ctrl.db
        graph = db._di_graph
        d_nodes = {}
        da_nodes = {}
        png_file = db.name
        if self.__args.schema_name:
            png_file = "%s_%s" % (db.name, self.__args.schema_name)
            l_schema_nodes = []
            l_keep = []
            for node in graph.nodes():
                if node.find(self.__args.schema_name) == 0:
                    l_schema_nodes.append(node)
            print(l_schema_nodes)
            for node in graph.nodes():
                if node in l_schema_nodes:
                    continue
                else:
                    for edge in graph.edges():
                        n1,n2 = edge
                        if n1 in l_schema_nodes and not n2 in l_keep:
                            l_keep.append(n2)
                        if n2 in l_schema_nodes and not n1 in l_keep:
                            l_keep.append(n1)
            for node in graph.nodes():
                if( not node in l_keep and
                    not node in l_schema_nodes):
                    graph.remove_node(node)
#            print(l_schema_nodes)
#            print(l_keep)
        for node in graph.nodes():
            d_nodes["%s" % ( node )] = node
        pos=nx.graphviz_layout(graph, prog="neato")
        if self.__args.schema_name:
            for node in graph.nodes():
                pass
        nx.draw_networkx_nodes( graph, pos, node_size=0.3, alpha=0.4)
        nx.draw_networkx_labels(
            graph, pos, labels = da_nodes, font_size=4, font_color="b")
        nx.draw_networkx_labels( graph, pos, labels = d_nodes, font_size=4 )
        nx.draw_networkx_edges(
            graph, pos, alpha=0.2, node_size=0, width=0.5, edge_color='k')
        png_file = "graph_%s.png" % (png_file)
        plt.axis('off')
        print(plt.margins())
        #plt.margins(0.1,0.1)
        plt.savefig(png_file, dpi = 600)
        print("the graph is in %s" % (png_file))
