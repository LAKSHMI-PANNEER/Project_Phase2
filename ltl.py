
def _get_sequence(seq):
    if len(seq) == 1:
        return ('until','True',seq)
    return ('until','True', ('and', seq[0], _get_sequence(seq[1:])))

def _get_sequence_night(seq):
    if len(seq) == 1:
        return ('until',_sn(),_snp(seq))
    return ('until',_sn(), ('and', _snp(seq[0]), _get_sequence_night(seq[1:])))

def get_option(goal):
    return _get_sequence(goal)

def get_option_night(goal):
    return _get_sequence_night(goal)

def _sn():
    return ('or',('not','n'),'s')

def _snp(proposition):
    return ('or',('and', ('not','n'), proposition),('and','s',proposition))

val = input("Enter the goal: ") 

"""
goals = ['ab','ac','de','db','fae','abdc','acfb','acfc','faeg','acfbh']

The set of propositional symbols are {a,b,c,d,e,f,g,h,n,s}:
    a: got_wood
    b: used_toolshed
    c: used_workbench
    d: got_grass
    e: used_factory
    f: got_iron
    g: used_bridge
    h: used_axe
    n: is_night
    s: at_shelter
"""

print('\n LTL Translation:', get_option(val))
print('\n Safety Constraints:', get_option_night(val))
print('\n The special constraint to go to the shelter:', _snp(val))



