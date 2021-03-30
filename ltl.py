from sympy import *
from sympy.logic import simplify_logic
from sympy.logic.boolalg import And, Or, Not
import time, collections

"""
set of propositional symbols = {a,b,c,d,e,f,s}:
a: got_wood
b: used_toolshed
c: used_workbench
d: got_grass
e: used_factory
f: got_iron
s: at_shelter
    
goals = {'ab','ac','de','db','fae','abdc'}:
ab: make_plank
ac: make_stick
de: make_cloth
db: make_rope
fae: make_bridge
abdc: make_bed
"""

def get_option(goal):
    return _get_sequence(goal)

def _get_sequence(seq):
    if len(seq) == 1:
        return ('until','True',seq)
    return ('until','True', ('and', seq[0], _get_sequence(seq[1:])))

def extract_propositions(ltl_formula):
    return list(set(_get_propositions(ltl_formula)))

def get_dfa(ltl_formula):
    propositions = extract_propositions(ltl_formula)
    propositions.sort()
    truth_assignments = _get_truth_assignments(propositions)
    ltl2states = {'False':-1, ltl_formula: 0}
    edges = {}

    visited, queue = set([ltl_formula]), collections.deque([ltl_formula])
    while queue: 
        formula = queue.popleft()
        if formula in ['True', 'False']:
            continue
        for truth_assignment in truth_assignments:
            f_progressed = _progress(formula, truth_assignment)
            if f_progressed not in ltl2states:
                new_node = len(ltl2states) - 1
                ltl2states[f_progressed] = new_node
            edge = (ltl2states[formula],ltl2states[f_progressed])
            if edge not in edges:
                edges[edge] = []
            edges[edge].append(truth_assignment)
            
            if f_progressed not in visited: 
                visited.add(f_progressed) 
                queue.append(f_progressed) 

    initial_state = 0
    accepting_states = [ltl2states['True']]
    edges_tuple = []

    for e in edges:
        f  = _get_formula(edges[e], propositions)
        edges_tuple.append((e[0],e[1],f))
    edges_tuple.append((ltl2states['True'],ltl2states['True'], 'True'))
    edges_tuple.append((ltl2states['False'],ltl2states['False'], 'True'))

    return initial_state, accepting_states, ltl2states, edges_tuple

def _get_truth_assignments(propositions):
    truth_assignments = []
    for p in range(2**len(propositions)):
            truth_assignment = ""
            p_id = 0
            while p > 0:
                if p%2==1:
                    truth_assignment += propositions[p_id]
                p //= 2
                p_id += 1
            truth_assignments.append(truth_assignment)
    return truth_assignments

def _get_propositions(ltl_formula):
    if type(ltl_formula) == str:
        if ltl_formula in ['True','False']:
            return []
        return [ltl_formula]
    
    if ltl_formula[0] in ['not', 'next']:
        return _get_propositions(ltl_formula[1])
    
    return _get_propositions(ltl_formula[1]) + _get_propositions(ltl_formula[2])
    
def _is_prop_formula(f):
    return 'next' not in str(f) and 'until' not in str(f)

def _subsume_until(f1, f2):
    if str(f1) not in str(f2):
        return False
    while type(f2) != str:
        if f1 == f2:
            return True
        if f2[0] == 'until':
            f2 = f2[2]
        elif f2[0] == 'and':
            if _is_prop_formula(f2[1]) and not _is_prop_formula(f2[2]):
                f2 = f2[2]
            elif not _is_prop_formula(f2[1]) and _is_prop_formula(f2[2]):
                f2 = f2[1]
            else:
                return False
        else:
            return False
    return False

def _progress(ltl_formula, truth_assignment):
    if type(ltl_formula) == str:
        if len(ltl_formula) == 1:
            if ltl_formula in truth_assignment:
                return 'True'
            else:
                return 'False'
        return ltl_formula
    
    if ltl_formula[0] == 'not':
        result = _progress(ltl_formula[1], truth_assignment)
        if result == 'True':
            return 'False'
        elif result == 'False':
            return 'True'
        else:
            raise NotImplementedError("The following formula doesn't follow the cosafe syntactic restriction: " + str(ltl_formula))

    if ltl_formula[0] == 'and':
        res1 = _progress(ltl_formula[1], truth_assignment)
        res2 = _progress(ltl_formula[2], truth_assignment)
        if res1 == 'True' and res2 == 'True': return 'True'
        if res1 == 'False' or res2 == 'False': return 'False'
        if res1 == 'True': return res2
        if res2 == 'True': return res1
        if res1 == res2:   return res1
        if _subsume_until(res1, res2): return res2
        if _subsume_until(res2, res1): return res1
        return ('and',res1,res2)

    if ltl_formula[0] == 'or':
        res1 = _progress(ltl_formula[1], truth_assignment)
        res2 = _progress(ltl_formula[2], truth_assignment)
        if res1 == 'True'  or res2 == 'True'  : return 'True'
        if res1 == 'False' and res2 == 'False': return 'False'
        if res1 == 'False': return res2
        if res2 == 'False': return res1
        if res1 == res2:    return res1
        if _subsume_until(res1, res2): return res1
        if _subsume_until(res2, res1): return res2
        return ('or',res1,res2)
    
    if ltl_formula[0] == 'next':
        return _progress(ltl_formula[1], truth_assignment)
    
    if ltl_formula[0] == 'until':
        res1 = _progress(ltl_formula[1], truth_assignment)
        res2 = _progress(ltl_formula[2], truth_assignment)

        if res1 == 'False':
            f1 = 'False'
        elif res1 == 'True':
            f1 = ('until', ltl_formula[1], ltl_formula[2])
        else:
            f1 = ('and', res1, ('until', ltl_formula[1], ltl_formula[2]))
        
        if res2 == 'True':
            return 'True'
        if res2 == 'False':
            return f1
        return res2 

def _get_formula(truth_assignments, propositions):
    dnfs = []
    props = dict([(p, symbols(p)) for p in propositions])
    for truth_assignment in truth_assignments:
        dnf = []
        for p in props:
            if p in truth_assignment:
                dnf.append(props[p])
            else:
                dnf.append(Not(props[p]))
        dnfs.append(And(*dnf))
    formula = Or(*dnfs)
    formula = simplify_logic(formula, form='dnf')
    formula = str(formula).replace('(','').replace(')','').replace('~','!').replace(' ','')
    return formula

val = input("Enter the goal: ") 

if val in ['ab','ac','de','db','fae','abdc']:
	print('\nLTL Formula:', get_option(val))
	ltl_formula = get_option(val)
	propositions = _get_propositions(ltl_formula)
	print('\nPropositions:', propositions)
	ta = _get_truth_assignments(propositions)
	print('\nTruth assignments:', ta)
	form = _progress(ltl_formula, ta)
	print('\nProgress:', form)
	dfa = get_dfa(ltl_formula)
	print('\nDFA:', dfa)
else:
	print("Enter valid goal!")

