#!/usr/bin/env python
# coding: utf-8

import pandas as pd

def string2definition1(tabular_text_output, initial_node_value, out='model.txt'):
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
    for node in nodes:
        initial_condition = node + ' = ' + initial_node_value
        initial_conditions.append(initial_condition)
        
    # definition
    definition = '#initial conditions\n'+'\n'.join(initial_conditions)+'\n\n#rules\n'+'\n'.join(rules)
    
    return definition


def string2definition2(tabular_text_output, complexes, initial_value):
    df = pd.read_csv(tabular_text_output)
    df_complexes = pd.read_csv(complexes)

    # get list of nodes 
    nodes = list(df.node1.unique())
    
    # build dict of node inputs
    node_inputs = {}
    for node in nodes:
        inputs = list(df[df.node1 == node].node2)
        node_inputs[node] = inputs
        
    # get list of complexes 
    complexes = list(df_complexes.complex.unique())

    # build dict of components
    complex_components = {}
    for complex in complexes:
        inputs = list(df_complexes[df_complexes.complex == complex].node)
        complex_components[complex] = inputs

    # add complex inputs
    complex_inputs = get_complex_inputs(node_inputs, complex_components)
    
    # reduce complexes
    node_inputs = reduce_complexes(node_inputs, complex_components)
    
    # OR node inputs
    rules = []
    for node, inputs in node_inputs.items():
        rule = node + ' *= '
        rule = rule + ' or '.join(inputs)
        rules.append(rule)
        
    # AND complex components
    for complex, components in complex_components.items():
        rule = complex + ' *= '
        rule = rule + ' and '.join(components)
        rules.append(rule)
    
    # OR complex inputs
    for complex, inputs in complex_inputs.items():
        rule = complex + ' *= '
        rule = rule + complex + ' or '+' or '.join(inputs)
        rules.append(rule)
        
    # initial conditions
    initial_value = 'True' if initial_value else 'False'
    initial_conditions = []
    for node in (nodes+complexes):
        initial_condition = node + ' = ' + initial_value
        initial_conditions.append(initial_condition)
        
    # definition
    definition = '#initial conditions\n'+'\n'.join(initial_conditions)+'\n\n#rules\n'+'\n'.join(rules)
    
    return definition
        
        

def add_process_edgelist1(definition, edgelist, initial_process_value):
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
        
    # construct boolean rules as list
    rules = []
    for key, value in node_inputs.items():
        rule = key + ' *= '
        rule = rule + ' and '.join(value)
        rules.append(rule)
        
    # construct initial conditions
    initial_conditions = []
    for node in nodes:
        initial_condition = node + ' = ' + initial_process_value
        initial_conditions.append(initial_condition)
        
    # definition
    return definition + '\n\n#process node initial conditions\n'+'\n'.join(initial_conditions)+'\n\n#process node rules\n'+'\n'.join(rules)

def add_process_edgelist2(definition, edgelist, complexes, initial_value):
    """
    model 2
    """
    df = pd.read_csv(edgelist)
    df_complexes = pd.read_csv(complexes)

    # get list of nodes
    nodes = df.process.unique()

    # build dict of node inputs
    node_inputs = {}
    for node in nodes:
        inputs = list(df[df.process == node].node)
        node_inputs[node] = inputs
    
    # get list of complexes 
    complexes = list(df_complexes.complex.unique())

    # build dict of complexes
    complex_inputs = {}
    for complex in complexes:
        inputs = list(df_complexes[df_complexes.complex == complex].node)
        complex_inputs[complex] = inputs
    
    # reduce complexes
    node_inputs = reduce_complexes(node_inputs, complex_inputs)
    
    # construct boolean rules as list
    rules = []
    for key, value in node_inputs.items():
        rule = key + ' *= '
        rule = rule + ' and '.join(value)
        rules.append(rule)
        
    # initial conditions
    initial_value = 'True' if initial_value else 'False'
    initial_conditions = []
    for node in (nodes):
        initial_condition = node + ' = ' + initial_value
        initial_conditions.append(initial_condition)
        
    # definition
    return definition + '\n\n#process node initial conditions\n'+'\n'.join(initial_conditions)+'\n\n#process node rules\n'+'\n'.join(rules)



def add_mtb_edgelist(definition, edgelist, initial_mtb_value):
    df = pd.read_csv(edgelist)

    # get list of nodes
    target_nodes = df.node.unique()
    mtb_nodes = df.mtb.unique()
    
    # build dict of node inputs
    node_inputs = {}
    for node in target_nodes:
        inputs = list(df[df.node == node].mtb)
        node_inputs[node] = inputs
    
    # construct boolean rules as list
    rules = []
    for key, value in node_inputs.items():
        rule = key + ' *= ' + key
        rule = rule + ' and not (' +' or '.join(value) + ')'
        rules.append(rule)

    # construct initial conditions
    initial_conditions = []
    for node in mtb_nodes:
        initial_condition = node + ' = ' + initial_mtb_value
        initial_conditions.append(initial_condition)
        
    # definition
    return definition + '\n\n#mtb node initial conditions\n'+'\n'.join(initial_conditions)+'\n\n#mtb update rules\n'+'\n'.join(rules)

def reduce_complexes(node_inputs, complex_inputs):
    # remove nodes in a complex
    for components in complex_inputs.values():
        for node in node_inputs.keys():
            if node in components:
                del node_inputs[node]
                continue

    # replace complex nodes
    for node, inputs in node_inputs.items():
        for complex, components in complex_inputs.items():
            for i, input in enumerate(inputs):
                if input in components:
                    node_inputs[node][i] = complex
                    continue
        node_inputs[node] = list(set(node_inputs[node]))
    return node_inputs

def get_complex_inputs(node_inputs, complex_components):
    complex_inputs = {}
    for complex, components in complex_components.items():
        inputs = []
        for component in components:
            inputs+=node_inputs[component]
        complex_inputs[complex] = list(set(inputs))
    complex_inputs=reduce_complexes(complex_inputs, complex_components)
    for complex, inputs in complex_inputs.items():
        inputs.remove(complex)
    return complex_inputs