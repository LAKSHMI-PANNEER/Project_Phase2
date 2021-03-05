from sympy import *
from sympy.logic import simplify_logic
from sympy.logic.boolalg import And, Or, Not
import time, collections

def get_option(goal):
    return _get_sequence(goal)

def get_option_night(goal):
    return _get_sequence_night(goal)

def _snp(proposition):
    return ('or',('and', ('not','n'), proposition),('and','s',proposition))

def _sn():
    return ('or',('not','n'),'s')

def _get_sequence(seq):
    if len(seq) == 1:
        return ('until','True',seq)
    return ('until','True', ('and', seq[0], _get_sequence(seq[1:])))

def _get_sequence_night(seq):
    if len(seq) == 1:
        return ('until',_sn(),_snp(seq))
    return ('until',_sn(), ('and', _snp(seq[0]), _get_sequence_night(seq[1:])))
    
val = input("Enter the goal: ") 

ltl_formula = get_option(val)

def extract_propositions(ltl_formula):
    return list(set(_get_propositions(ltl_formula)))

def get_dfa(ltl_formula):

    propositions = extract_propositions(ltl_formula)
    propositions.sort()
    truth_assignments = _get_truth_assignments(propositions)

    # Creating DFA using progression
    ltl2states = {'False':-1, ltl_formula: 0}
    edges = {}

    visited, queue = set([ltl_formula]), collections.deque([ltl_formula])
    while queue: 
        formula = queue.popleft()
        if formula in ['True', 'False']:
            continue
        for truth_assignment in truth_assignments:
            # progressing formula
            f_progressed = _progress(formula, truth_assignment)
            if f_progressed not in ltl2states:
                new_node = len(ltl2states) - 1
                ltl2states[f_progressed] = new_node
            # adding edge
            edge = (ltl2states[formula],ltl2states[f_progressed])
            if edge not in edges:
                edges[edge] = []
            edges[edge].append(truth_assignment)
            
            if f_progressed not in visited: 
                visited.add(f_progressed) 
                queue.append(f_progressed) 

    # Adding initial and accepting states
    initial_state = 0
    accepting_states = [ltl2states['True']]
    edges_tuple = []
    for e in edges:
        f  = _get_formula(edges[e], propositions)
        edges_tuple.append((e[0],e[1],f))
    # Adding self-loops for 'True' and 'False'
    edges_tuple.append((ltl2states['True'],ltl2states['True'], 'True'))
    edges_tuple.append((ltl2states['False'],ltl2states['False'], 'True'))

    return initial_state, accepting_states, ltl2states, edges_tuple

def _get_truth_assignments(propositions):
    # computing all possible value assignments for propositions
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
    
    # 'and', 'or', 'until'
    return _get_propositions(ltl_formula[1]) + _get_propositions(ltl_formula[2])
    
def _is_prop_formula(f):
    # returns True if the formula does not contains temporal operators
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
        # True, False, or proposition
        if len(ltl_formula) == 1:
            # ltl_formula is a proposition
            if ltl_formula in truth_assignment:
                return 'True'
            else:
                return 'False'
        return ltl_formula
    
    if ltl_formula[0] == 'not':
        # negations should be over propositions only according to the cosafe ltl syntactic restriction
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
        return res2 #('or', res2, f1)


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
    
propositions = _get_propositions(ltl_formula)

print('\n Propositions:', propositions)

ta = _get_truth_assignments(propositions)

print('\n Truth assignments:', ta)

form = _progress(ltl_formula, ta)

print('\n Progress:', form)

dfa = get_dfa(ltl_formula)

print('\n DFA:', dfa)


