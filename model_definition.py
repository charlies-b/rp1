#!/usr/bin/env python
# coding: utf-8

# In[58]:


from JL_Mtb_model import model_definition


# In[59]:


print model_definition


# In[60]:


rules_header = "# Next are the boolean rules determining wether a node is turned on or off"
model_initialisation, model_rules = model_definition.split(rules_header)


# In[63]:


# helper functions

def define_model(model_initialisation, model_rules):
    return model_initialisation+'\n'+rules_header+'\n'+model_rules
    return model
print define_model(model_initialisation, model_rules)


# In[ ]:


# export
# model_initialisation
# model_rules
    # intitalise random()
    # initialise subset()
    # initialise dict()
# define_model()

