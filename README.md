phpgraph
========

Extracts the linked PHP files from a PHP project and creates a JSON file suitable for use with d3js. 

Outputs graph data as JSON, suitable for use by d3js as seen in this example:

    http://bl.ocks.org/mbostock/4062045

Example provided of PHP files found in MediaWiki 1.21.2:

    http://download.wikimedia.org/mediawiki/1.21/mediawiki-1.21.2.tar.gz

Outputs to JSON using this NetworkX function:

    http://networkx.github.io/documentation/latest/reference/generated/networkx.readwrite.json_graph.node_link_data.html#networkx.readwrite.json_graph.node_link_data
