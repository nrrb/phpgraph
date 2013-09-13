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

def strip_base_path_from_path(base_path, path):
    pattern = re.compile(base_path + '(?P<path_we_want>.*)')
    return re.search(pattern, path).groupdict()['path_we_want']

def get_edges(path):
    edges = []
    for php_file in get_php_files(path):
        php_file = os.path.abspath(os.path.join(path, php_file))
        relative_path = os.path.dirname(php_file)
        for included_file in get_php_includes(php_file):
            # if the file path starts with a /, this screws up the os.path.join
            if included_file[0] == '/':
                included_file = included_file[1:]
            included_file = os.path.abspath(os.path.join(relative_path, included_file))
            if os.path.exists(included_file):
                # strip out the base path, no one wants to see that
                edge_start = strip_base_path_from_path(path, php_file)
                edge_end = strip_base_path_from_path(path, included_file)
                edges.append((edge_start, edge_end))
    return edges

def write_edges_to_json(edges, output_path):
    dg = networkx.DiGraph()
    dg.add_edges_from(edges)
    data = json_graph.node_link_data(dg)
    # d3js apparently doesn't like JSON files with single quotes
    json_data = json.dumps(data, indent=4).replace('\'', '"')
    with open(output_path, 'wb') as f:
        f.write(json_data)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Syntax: python phpgraph.py /path/to/phpfiles/ output.json")
        exit(1)

    search_path = sys.argv[1]
    output_path = sys.argv[2]

    edges = get_edges(search_path)
    write_edges_to_json(edges, output_path)
