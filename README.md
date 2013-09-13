phpgraph
========

Usage
-----

> python phpgraph.py /path/to/phpfiles/ output.json

Notes
-----

Extracts the linked PHP files from a PHP project and creates a JSON file suitable for use with [d3js](http://d3js.org/).

Outputs graph data as JSON, suitable for use by d3js [as seen in this example](http://bl.ocks.org/mbostock/4062045).

Example provided of PHP files found in [MediaWiki 1.21.2](http://download.wikimedia.org/mediawiki/1.21/mediawiki-1.21.2.tar.gz). [See this example visualized with d3js here](http://bl.ocks.org/tothebeat/6551304). 

Outputs to JSON using the [json_graph.node_link_data](http://networkx.github.io/documentation/latest/reference/generated/networkx.readwrite.json_graph.node_link_data.html#networkx.readwrite.json_graph.node_link_data) function of the [NetworkX Python library](http://networkx.github.io/).
