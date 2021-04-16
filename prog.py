import math
import time,collections
import random, os
from sympy import *
from enum import Enum
from collections import deque
from sympy.logic import simplify_logic
from sympy.logic.boolalg import And, Or, Not
start = time.time()

class Entity:
    def __init__(self,i,j):
        self.i = i
        self.j = j

    def change_position(self,i,j):
        self.i = i
        self.j = j

    def idem_position(self,i,j):
        return self.i==i and self.j==j

    def interact(self, agent):
        return True

class Agent(Entity):
    def __init__(self,i,j,actions):
        super().__init__(i,j)
        self.num_keys = 0
        self.reward  = 0
        self.actions = actions

    def get_actions(self):
        return self.actions

    def update_reward(self, r):
        self.reward += r

    def __str__(self):
        return "A"

class Obstacle(Entity):
    def __init__(self,i,j):
        super().__init__(i,j)

    def interact(self, agent):
        return False

    def __str__(self):
        return "X"

class Empty(Entity):
    def __init__(self,i,j,label=" "):
        super().__init__(i,j)
        self.label = label

    def __str__(self):
        return self.label

class Actions(Enum):
    up    = 0
    right = 1
    down  = 2
    left  = 3

def get_sequence_of_subtasks():
    tasks = []
    tasks.append(_get_sequence('ab'))
    tasks.append(_get_sequence('ac'))
    tasks.append(_get_sequence('de'))
    tasks.append(_get_sequence('db'))
    tasks.append(_get_sequence('fae'))
    tasks.append(_get_sequence('abdc'))
    #tasks.append(_get_sequence('acfb'))
    #tasks.append(_get_sequence('acfc'))
    return tasks

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

class DFA:
    def __init__(self, ltl_formula):
        initial_state, accepting_states, ltl2state, edges = get_dfa(ltl_formula)

        self.formula   = ltl_formula
        self.state     = initial_state    
        self.terminal  = accepting_states 
        self.ltl2state = ltl2state        
        self.state2ltl = dict([[v,k] for k,v in self.ltl2state.items()])
        self.nodelist = {}
        for v1, v2, label in edges:
            if v1 not in self.nodelist:
                self.nodelist[v1] = {}
            self.nodelist[v1][v2] = label

    def progress(self, true_props): 
        self.state = self._get_next_state(self.state, true_props)

    def _get_next_state(self, v1, true_props):
        for v2 in self.nodelist[v1]:
            if _evaluate_DNF(self.nodelist[v1][v2], true_props):
                return v2
        return -1

    def progress_LTL(self, ltl_formula, true_props): 
        if ltl_formula not in self.ltl2state:
            raise NameError('ltl formula ' + ltl_formula + " is not part of this DFA")
        return self.get_LTL(self._get_next_state(self.ltl2state[ltl_formula], true_props))

    def in_terminal_state(self):
        return self.state in self.terminal

    def get_LTL(self, s = None):
        if s is None: s = self.state
        return self.state2ltl[s]

    def is_game_over(self):
        return self.in_terminal_state() or self.state == -1

    def __str__(self):
        aux = []
        for v1 in self.nodelist:
            aux.extend([str((v1,v2,self.nodelist[v1][v2])) for v2 in self.nodelist[v1]])
        return "\n".join(aux)

def _evaluate_DNF(formula,true_props):
    if "|" in formula:
        for f in formula.split("|"):
            if _evaluate_DNF(f,true_props):
                return True
        return False
    if "&" in formula:
        for f in formula.split("&"):
            if not _evaluate_DNF(f,true_props):
                return False
        return True
    if formula.startswith("!"):
        return not _evaluate_DNF(formula[1:],true_props)
    if formula == "True":  return True
    if formula == "False": return False
    return formula in true_props

def value_iteration(S, actions, T, V, discount=1, v_init=0, e=0.01):
    for s in S:
        if s not in V:
            V[s] = v_init
    while True:
        error = 0
        for s in S:
            v = V[s]
            V[s] = max([get_value_action(s,a,T,V,discount) for a in actions])
            error = max([error,abs(V[s]-v)])
        if error < e:
            break

def get_value_action(s,a,T,V,discount=1):
    return sum([T[s][a].get_probability(s2) * (T[s][a].get_reward(s2) + discount * V[s2]) for s2 in T[s][a].get_next_states()])

class Transition:
    def __init__(self, s, a):
        self.s = s    
        self.a = a    
        self.R = {}   
        self.T = {}   

    def add_successor(self, s_next, prob, reward):
        self.T[s_next] = prob
        self.R[s_next] = reward

    def get_next_states(self):
        return self.T.keys()

    def get_reward(self, s_next):
        return float(self.R[s_next])

    def get_probability(self, s_next):
        return float(self.T[s_next])

def evaluate_optimal_policy(map, agent_i, agent_j, consider_night, tasks, task_id):
    map_height, map_width = len(map), len(map)
    actions = [Actions.up, Actions.down, Actions.left, Actions.right]

    summary = []
    for ltl_task in tasks:
        dfa = DFA(ltl_task)
        S = set()
        for i in range(1,map_height-1):
            for j in range(1,map_width-1):
            	for ltl in dfa.ltl2state:
                        if ltl not in ['True', 'False']:
                            S.add((i,j,ltl))
             
        S.add('False')
        S.add('True')
        T = {}
        for s in S:
            T[s] = {}
            for a in actions:
                T[s][a] = Transition(s,a)
                if s in ['False','True']:
                    T[s][a].add_successor(s, 1, 0)
                else:
                    i,j,ltl = s
                    s2_i, s2_j = i, j
                    if a == Actions.up:    s2_i-=1
                    if a == Actions.down:  s2_i+=1
                    if a == Actions.left:  s2_j-=1
                    if a == Actions.right: s2_j+=1
                    if str(map[s2_i][s2_j]) == "X":
                        s2_i, s2_j = i, j
                    true_props = str(map[s2_i][s2_j]).strip()
                    s2_ltl = dfa.progress_LTL(ltl, true_props)
                    if s2_ltl in ['False','True']:
                        s2 = s2_ltl
                    else:
                        s2 = (s2_i,s2_j,s2_ltl)

                    T[s][a].add_successor(s2, 1, -1 if s2 != 'False' else -1000)
                    if s2 not in S:
                        print("Error!")

        V = {}
        value_iteration(S, actions, T, V)
        s = (agent_i, agent_j, dfa.get_LTL())

        summary.append(int(-V[s]))
    print(summary)

def addElements(map, elements, num_per_type):
    map_height, map_width = len(map), len(map[0])
    for _ in range(num_per_type):
        for e in elements:
            while(True):
                i, j = random.randint(1, map_height-1), random.randint(1, map_width-1)
                if map[i][j] == " ":
                    map[i][j] = e
                    break

def getObjects(map):
    objs = {}
    for i in range(len(map)):
        for j in range(len(map[i])):
            e = map[i][j]
            if e == "A": agent = i,j
            elif e not in " X":
                if e not in objs: objs[e] = []
                objs[e].append((i,j))
    return objs, agent

def getMD(a, o):
    return sum([abs(a[i]-o[i]) for i in range(len(a))])

def getMyopicSolution(agent, objs, task):
    if task == "": return 0
    min_cost = min([getMD(agent, pos) for pos in objs[task[0]]])
    return min([getMD(agent, pos) + getMyopicSolution(pos, objs, task[1:]) for pos in objs[task[0]] if getMD(agent, pos) == min_cost])

def getOptimalSolution(agent, objs, task):
    if task == "": return 0
    return min([getMD(agent, pos) + getOptimalSolution(pos, objs, task[1:]) for pos in objs[task[0]]])

def computeOptimalSolutions(map, tasks):
    objs, agent = getObjects(map)
    myopic_optimal = 0
    for t in tasks:
        optimal = getOptimalSolution(agent, objs, t)
        myopic  = getMyopicSolution(agent, objs, t)
        myopic_optimal += 0.9**(myopic - optimal)
    return myopic_optimal/len(tasks)

def createMap(conf_params, seed, show):
    map_width, map_height, resources, workstations, shelter_locations, tasks, num_resource_per_type, num_workstations_per_type=conf_params
    random.seed(10)
    map = [["X"]+[" " for _ in range(map_width-2)]+["X"] for _ in range(map_height)]
    map[0] = ["X" for _ in range(map_width)]
    map[-1] = ["X" for _ in range(map_width)]
    map[map_height//2][map_width//2] = "A"
    agent_i, agent_j = map_height//2, map_width//2
    for i,j in shelter_locations:
        map[i][j] = "s"
    addElements(map, workstations, num_workstations_per_type)
    addElements(map, resources, num_resource_per_type)

    if show:
        print("Computing optimal policies in number of steps")
        evaluate_optimal_policy(map, agent_i, agent_j, False, get_sequence_of_subtasks(), 1)
    computeOptimalSolutions(map, tasks)
'''
	for row in map:
            print("".join(row))
'''
 
if __name__ == '__main__':
    map_width  = 21
    map_height = 21
    resources = 'adf'
    workstations = 'bce'
    num_resource_per_type = 5
    num_workstations_per_type = 2
    shelter_locations = [(i,j) for i in range(8,13) for j in range(11,20)]
    tasks = ["ab", "ac", "de", "db", "fae", "abdc"]
    conf_params = map_width, map_height, resources, workstations, shelter_locations, tasks, num_resource_per_type,num_workstations_per_type

#seed = input("Enter a seed value:" )
seed = random.randint(0,5)
createMap(conf_params, seed, show=True)

end = time.time()
print("Execution time => %s seconds" % (end - start))
