import pandas as pd 


def string2definition(path):
    """
    model 3
    """
    # read string model definition from file
    with open(path, 'r') as fp: return(fp.read())

    

def add_mtb2definition(definition, mtb_edgelist, initial_value = False):
    """
    model 3
    """

    # read edges
    df = pd.read_csv(mtb_edgelist)

    # build dict of mtb node edges
    target_nodes = list(df.node.unique())
    target_edges = {}
    for node in target_nodes:
        edges = list(df[df.node == node].mtb)
        target_edges[node] = edges

    # remove targets not in the network (not modelled)
    for target in target_nodes:
        if target not in definition: del target_edges[target]

    # enumerate mtb factors modelled
    mtb_nodes = list(set([node for nodes in target_edges.values() for node in nodes]))

    # generate boolean rules
    rules = []
    for target, mtb in target_edges.items():
        rule = target + ' *= ' + target # add the inhibition rule recursively
        rule = rule + ' and not (' +' or '.join(mtb) + ')'
        rules.append(rule)

    # generate mtb initilaisations
    initial_conditions = []
    initial_value = 'True' if initial_value else 'False'
    for node in mtb_nodes:
        initial_condition = node + ' = ' + initial_value
        initial_conditions.append(initial_condition)

    # message
    print 'added: '+ str(mtb_nodes)

    # construct definition 
    return (
        definition + 
            '\n\n'+
            '#mtb\n'+
            '\n'.join(initial_conditions)+
            '\n\n'+
            '#mtb rules\n'+
            '\n'.join(rules)
    )
