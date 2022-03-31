import networkx as nx
import matplotlib.pyplot as plt


def draw_edgelists(network, 
                  highlight = [], 
                  add_process = False, 
                  add_mtb = False,
                  node_colour = 'blue',
                  process_colour = 'lightgreen', 
                  mtb_colour = 'red', 
                  highlight_colour='lightblue'):

    # create edgelist

    edges = []
    nodes = {}

    lines = open(network).readlines()[1:] # remove headers
    for line in lines:
        line = line.split(',')

        node1=line[0].strip()
        node2=line[1].strip()
        if node1 not in nodes: nodes[node1] = node_colour
        if node2 not in nodes: nodes[node2] = node_colour

        edge = line[0].strip()+' '+line[1].strip()
        edges.append(edge)

    add_nodes={}
    process = open(add_process).readlines()[1:] if add_process else []
    mtb =  open(add_mtb).readlines()[1:] if add_mtb else []
    for lines, colour in zip([process, mtb], [process_colour, mtb_colour]): # keep ordered
        for node in nodes:
            for line in lines:
                if node in line:
                    line = line.split(',')

                    node1=line[0].strip()
                    node=line[1].strip()
                    if node1 not in nodes: add_nodes[node1] = colour
                    if node2 not in nodes: add_nodes[node2] = colour

                    edge = line[0].strip()+' '+line[1].strip()
                    edges.append(edge)
    
    nodes.update(add_nodes)
    
    
    for node in nodes:     # color highlight nodes
        if node in highlight: nodes[node]=highlight_colour

    nodelist = nodes.keys()
    colorlist = nodes.values()
    
    # write/read edgelist
    
    open("edgelist.nx", 'w+').write('\n'.join(edges))
    G=nx.read_edgelist('edgelist.nx')

    # plot
    
    nx.draw(G, with_labels=True, node_size=100, font_color='white', font_size=16, nodelist=nodelist, node_color=colorlist)
    plt.gcf().set_size_inches(20, 20)
    plt.gcf().set_facecolor('grey')



