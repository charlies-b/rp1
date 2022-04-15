import pandas as pd 

def string2definition(tabular_text_output, complex_map, initial_value=True):
    """
    model 2
    """
    
    # read edges
    df = pd.read_csv(tabular_text_output)

    # build dict of factor node edges
    factor_nodes = list(df.node1.unique())
    node_edges = {}
    for node in factor_nodes:
        edges = list(df[df.node1 == node].node2)
        node_edges[node] = edges

    # read complexes
    df = pd.read_csv(complex_map)

    # build complex maps
    complex_nodes = list(df.complex.unique())
    complex2component = {}
    component2complex = {}
    for node in complex_nodes:
        components = list(df[df.complex == node].component)
        component2complex.update(dict([(component, node) for component in components]))
        complex2component[node] = components

    # build OR edges
    node_edges_or = {}   
    component_nodes = df.component.unique() # all components

    for complex in complex_nodes: # aggregate edges for each complex
        complex_edges = []
        for node, edges in node_edges.items():
            if node in component_nodes: 
                if node in complex2component[complex]: complex_edges+=edges
                # node is a component AND belongs to this complex
            else:
                node_edges_or[node]=edges # if node is not a complex component store down
        node_edges_or[complex] = list(set(complex_edges)) # store down unique set of edeges foe each complex
    
    for node, edges in node_edges_or.items(): 
        # now replace edge nodes that are complex components with complex nodes
        or_edges =[] 
        for edge in edges:
            or_edge = component2complex[edge] if edge in component_nodes else edge          
            or_edges.append(or_edge)
        node_edges_or[node] = list(set(or_edges)) # unique values
        
        # for complexes this will enable us to easily add 'OR edges' as a recursive rule
        # complex *= complex OR edge OR ...
        # and then the complex components can be included in a seperate AND rule
        # complex *= component AND ...
        # this rule will be evaluated first before OR edges, resulting in the effect of using brackets

    # build AND edges
    node_edges_and = complex2component # components AND to complex nodes
    
    # generate rules
    complex_and = []
    for node, edges in node_edges_and.items(): # AND rules
        rule = node + ' *= ' + ' and '.join(edges)
        complex_and.append(rule)
    
    factor_or = []
    complex_or = []
    for node, edges in node_edges_or.items(): # OR rules
        if node in complex_nodes:
            edges.remove(node)
            rule = node + ' *= ' + node + ' or ' + ' or '.join(edges) # order the recursive rule for niceness
            complex_or.append(rule)

        else:
            rule = node + ' *= ' + ' or '.join(edges)
            factor_or.append(rule)
    
    
    # generate node initialisations
    initial_conditions = []
    initial_value = 'True' if initial_value else 'False'
    for node in factor_nodes + complex_nodes:
        initial_condition = node + ' = ' + initial_value
        initial_conditions.append(initial_condition)
        
    # construct definition 
    return(
            '#initial conditions\n'+
            '\n'.join(initial_conditions)+         
            '\n\n'+
            '#rules\n'+
            '\n'.join(complex_and) + # AND rules first, so OR rules can be added recursively
            '\n\n'+
            '\n'.join(complex_or) +
            '\n\n'+
            '\n'.join(factor_or)
    )       


def add_processes2definition(definition, process_edgelist, complex_map, initial_value=True):
    """
    model 2
    """
    
    # read edges
    df = pd.read_csv(process_edgelist)

    # build dict of process node edges
    process_nodes = list(df.process.unique())
    process_edges = {}
    for node in process_nodes:
        edges = list(df[df.process == node].node)
        process_edges[node] = edges

    # remove nodes not in the network (not modelled)
    for edges in process_edges.values():
        for node in edges:
            if node not in definition: edges.remove(node)

    # read complexes
    df = pd.read_csv(complex_map)

    # build complex maps
    complex_nodes = list(df.complex.unique())
    component2complex = {}
    for node in complex_nodes:
        components = list(df[df.complex == node].component)
        component2complex.update(dict([(component, node) for component in components]))

    # replace component factor nodes with complex node
    components = df.component.unique() # all components
    for process, edges in process_edges.items():
        for i, node in enumerate(edges):
            if node in components: edges[i] = component2complex[node]
        process_edges[process] = list(set(edges))

    # generate boolean rules
    rules = []
    for process, edges in process_edges.items():
        rule = process + ' *= ' + ' and '.join(edges) # assume AND
        rules.append(rule)

    # generate process initilaisations
    initial_conditions = []
    initial_value = 'True' if initial_value else 'False'
    for process in process_nodes:
        initial_condition = process + ' = ' + initial_value
        initial_conditions.append(initial_condition)

    # message
    print 'added: '+str(process_nodes)
    
    # construct definition 
    return(
        definition +
            '\n\n'+
            '#processes\n'+
            '\n'.join(initial_conditions)+         
            '\n\n'+
            '#process rules\n'+
            '\n'.join(rules)
    ) 

def add_mtb2definition(definition, mtb_edgelist, initial_value = False):
    """
    model 2
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
    print 'added: '+str(mtb_nodes)

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
