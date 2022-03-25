import pandas as pd 

def string2definition(tabular_text_output, initial_value):
    """
    model 1
    """
    df = pd.read_csv(tabular_text_output)
    
    # get list of nodes
    nodes = df.node1.unique()
    
    # build dict of node inputs
    node_inputs = {}
    for node in nodes:
        inputs = list(df[df.node1 == node].node2)
        node_inputs[node] = inputs
        
    # construct boolean rules as list
    rules = []
    for key, value in node_inputs.items():
        rule = key + ' *= '
        rule = rule + ' or '.join(value)
        rules.append(rule)
        
    # construct initial conditions
    initial_conditions = []
    initial_value = 'True' if initial_value else 'False'
    for node in nodes:
        initial_condition = node + ' = ' + initial_value
        initial_conditions.append(initial_condition)
        
    # definition
    return (
        '#initial conditions\n'+
        '\n'.join(initial_conditions)+         
        '\n\n'+
        '#rules\n'+
        '\n'.join(rules)
    )        

def add_process_edgelist(definition, edgelist, initial_value):
    """
    model 1
    """
    df = pd.read_csv(edgelist)
    
    # get list of nodes
    nodes = df.process.unique()

    # build dict of node inputs
    node_inputs = {}
    for node in nodes:
        inputs = list(df[df.process == node].node)
        node_inputs[node] = inputs
    
    # remove input nodes not in the network (not modelled)
    for inputs in node_inputs.values():
        for input in inputs:
            if input not in definition: inputs.remove(input)

    # construct boolean rules as list
    rules = []
    for key, value in node_inputs.items():
        rule = key + ' *= '
        rule = rule + ' and '.join(value)
        rules.append(rule)
        
    # construct initial conditions
    initial_conditions = []
    initial_value = 'True' if initial_value else 'False'
    for node in nodes:
        initial_condition = node + ' = ' + initial_value
        initial_conditions.append(initial_condition)
        
    # definition
    return (
        definition + 
        '\n\n'+
        '#process node initial conditions\n'+
        '\n'.join(initial_conditions)+
        '\n\n'+
        '#process node rules\n'+
        '\n'.join(rules)
    )

def add_mtb_edgelist(definition, mtb_edgelist, initial_value):
    """
    model 1
    """
    df = pd.read_csv(mtb_edgelist)

    # get list of nodes
    target_nodes = df.node.unique()
    
    # build dict of node inputs
    node_inputs = {}
    for node in target_nodes:
        inputs = list(df[df.node == node].mtb)
        node_inputs[node] = inputs
    
    # remove factors without target nodes in the network (not modelled)
    mtb_nodes = []
    for node, mtb in node_inputs.items():
        if node not in definition:
            del node_inputs[node]
        else:
            mtb_nodes+=mtb
            mtb_nodes = list(set(mtb_nodes)) #unique values

    # construct boolean rules as list
    rules = []
    for target_node, mtb in node_inputs.items():
        rule = target_node + ' *= ' + target_node # add the inhibition rule recursively
        rule = rule + ' and not (' +' or '.join(mtb) + ')'
        rules.append(rule)

    # construct initial conditions
    initial_conditions = []
    initial_value = 'True' if initial_value else 'False'
    for node in mtb_nodes:
        initial_condition = node + ' = ' + initial_value
        initial_conditions.append(initial_condition)
        
    # definition
    return (
        definition + 
        '\n\n'+
        '#mtb node initial conditions\n'+
        '\n'.join(initial_conditions)+
        '\n\n'+
        '#mtb update rules\n'+
        '\n'.join(rules)
    )


        