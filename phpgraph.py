from networkx.readwrite import json_graph
import networkx
import json
import sys
import os
import re

patterns = (
        re.compile('include[^\']+\'(?P<filename>[^\']+)\''),
        re.compile('require_once[^\']+[\'\"](?P<filename>[^\']+)[\'\"]'),
        re.compile('require[^\']+[\'\"](?P<filename>[^\']+)[\'\"]'),
        )

def is_php_file(filename):
    return ('.' in filename and filename.split('.')[-1].lower() == 'php')

def get_php_files(path):
    php_files = []
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            if is_php_file(filename):
                php_files.append(os.path.join(root, filename))
    return php_files

def get_php_includes(filename):
    includes = []
    with open(filename, 'rb') as f:
        for line in f.readlines():
            for pattern in patterns:
                s = re.search(pattern, line)
                if s:
                    filename = s.groupdict()['filename']
                    if is_php_file(filename):
                        includes.append(filename)
                        break
    return includes

def get_php_include_edges(path):
    edges = []
    for php_file in get_php_files(path):
        for included_file in get_php_includes(php_file):
            edges.append((php_file, included_file))
    return edges

def write_edges_to_json(edges, output_path):
    dg = networkx.DiGraph()
    dg.add_edges_from(edges)
    data = json_graph.node_link_data(dg)
    with open(output_path, 'wb') as f:
        f.write(json.dumps(data))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Syntax: python phpgraph.py /path/to/phpfiles/ output.json")
        exit(1)

    search_path = sys.argv[1]
    output_path = sys.argv[2]

    edges = get_php_include_edges(search_path)
    write_edges_to_json(edges, output_path)
