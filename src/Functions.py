"""This file contains functions that only call standard libraries
"""
import random
from fractions import Fraction

def rank_nodes(paths):
    #Given a list of paths, output a list of lists where the nodes in every
    #sublist are at the same "temporal" level
    paths = sorted(paths, key=lambda x:len(x), reverse=True)
    total_list = {}
    for path in paths:
        if total_list == {}: #The first path is our baseline
            for i, node in enumerate(path):
                rank = Fraction(i+1, len(path))
                rank_n = rank.numerator
                rank_d = rank.denominator
                total_list[rank_n, rank_d] = [node]
            continue
        for i, node in enumerate(path):
            if any([ node in total_list[x] for x in total_list]):
                #if the node already in our list we continue
                continue
            if i == 0:
                print "The root is not already in the total paths, error, error"
                sys.exit(1)
            rank = Fraction(i+1, len(path))
            rank_n = rank.numerator
            rank_d = rank.denominator
            if (rank_n, rank_d) in total_list:
                total_list[rank_n, rank_d].append(node)
            else:
                total_list[rank_n, rank_d] = [node]
    sorted_keys = sorted(total_list.keys(), key=lambda x:float(x[0])/x[1])
    ranked_nodes_path = []
    for k in sorted_keys:
        ranked_nodes_path.append(total_list[k])
    return ranked_nodes_path

def find_node_children(id, node_names):
    for x in node_names:
        frags = x.split('+')
        if frags[0] == id:
            if len(frags) == 1:
                return None
            else:
                return tuple(frags[1:])
    return None

def find_root(node_names):
    ids = (x.split('+')[0] for x in node_names)
    for id in ids:
        #The root is the only id which is not a children in all nodes
        if all([not id in x.split('+')[1:] for x in node_names]):
            return id
    return None

def paths_node_leaves(node, node_names):
    """Given a list of node names in the format A+B+C where A is the 
    unique node identifier and B,C its children name, the output
    is a list of list, each one being a path of nodes from the root
    to a leaf
    """
    paths = []
    leaves = [x for x in node_names if '+' not in x]
    ids = [x.split('+')[0] for x in node_names]
    children = find_node_children(node, node_names)
    if children is None:
        return [[node]]
    for child in children:
        child_paths = paths_node_leaves(child, node_names)
        for x in child_paths:
            new_path = [node]
            new_path.extend(x)
            paths.append(new_path)
    return paths
    
def do_stats(numbers):
    """Given a list of numbers, the output is the tuple:
        (average, standard_deviation, min, max)
    """
    avg = float(sum(numbers))/len(numbers)
    sum_square_diffs = 0
    for x in numbers:
        sum_square_diffs += pow(x - avg, 2)
    sd = pow(sum_square_diffs / len(numbers), 0.5)
    return (avg, sd, min(numbers), max(numbers))

def bp_positions(sec_struct):
    """This function takes as input a secondary structure,
    without pseudo-knots, and outputs a list of tuples (a,b)
    of the interacting  nucleotides ( 0 <= a < b < n )
    """
    left_bps = [] #Keeps track of the seen '('
    base_pairs = [] #Keeps track of the completed base pairs
    for i, position in enumerate(sec_struct):
        if position == '(':
            left_bps.append(i)
        #Every closing must match the last opening
        elif position == ')':
            base_pairs.append((left_bps.pop(), i))
    return base_pairs

def find_complement_bp(position, bps):
    """Given an integer "position" and a list of base pairs positions"bps"
    as outputed by "bp_positions", if position is involved in a base pair,
    the pair will be returned, else None.
    """
    for left, right in bps:
        if position in (left, right):
            return (left, right)
    return None

def masoud_to_probability_vector(masoud_format, 
                              range_start='!', range_end='~'):
    """Given the probs in the Masoud* format "for an RNA
    sequence, with the encoding starting at the "range_start" char and
    ending at the "range_end" char, we output a tuple of 4-tuple as:
    ( (P_A_1, P_C_1, P_G_1, P_U_1), ..., (P_A_n, P_C_n, P_G_n, P_U_n))
    where 'P_X_i' is the probability of having nucleotide 'X' at pos. 'i'.

    *Masoud format: 4 elements, each line represent a nucleotide
    probability in the order: "A, C, G, U". At the line of nucleotide
    'X', the i-th character represent the probability of having 'X'
    at position 'i'. If the i-th character is 'y', the probability of
    'X' at position 'i' is: (ord('y') - ord(range_start)) /(
        ord(range_end)-ord(range_start))
    """
    vector = []
    probs_range = ord(range_start) - ord(range_end)
    start = ord(range_start)
    end = ord(range_end)
    for pos in range(len(masoud_format[0])):
        vector.append((
            float(ord(masoud_format[0][pos])-start)/(end-start),
            float(ord(masoud_format[1][pos])-start)/(end-start),
            float(ord(masoud_format[2][pos])-start)/(end-start),
            float(ord(masoud_format[3][pos])-start)/(end-start)
        ))
    return tuple(vector)
    
def mickael_to_probability_vector(mickael_format, 
                              range_start='!', range_end='~'):
    """Given the probs in the Masoud* format "for an RNA
    sequence, with the encoding starting at the "range_start" char and
    ending at the "range_end" char, we output a tuple of 4-tuple as:
    ( (P_A_1, P_C_1, P_G_1, P_U_1), ..., (P_A_n, P_C_n, P_G_n, P_U_n))
    where 'P_X_i' is the probability of having nucleotide 'X' at pos. 'i'.

    *Masoud format: 4 elements, each line represent a nucleotide
    probability in the order: "A, C, G, U". At the line of nucleotide
    'X', the i-th character represent the probability of having 'X'
    at position 'i'. If the i-th character is 'y', the probability of
    'X' at position 'i' is: (ord('y') - ord(range_start)) /(
        ord(range_end)-ord(range_start))
    """
    vector = []
    probs_range = ord(range_start) - ord(range_end)
    start = ord(range_start)
    end = ord(range_end)
    for pos in range(len(mickael_format[0])):
        if mickael_format[0][pos] == '!' and mickael_format[1][pos] == '!' and mickael_format[2][pos] == '!' and mickael_format[3][pos] == '!': 
            vector.append((0.25,0.25,0.25,0.25))#The ancestor program returns NULL
    	else:
            vector.append((
                float(ord(mickael_format[0][pos])-start)/(end-start),
                float(ord(mickael_format[1][pos])-start)/(end-start),
                float(ord(mickael_format[2][pos])-start)/(end-start),
                float(ord(mickael_format[3][pos])-start)/(end-start)
            ))
    return tuple(vector)    

def mickael_leaves_to_probability_vector(sequence):
    vector = []
    for pos in range(len(sequence)):#Assign the probabilities of the leaves
        if sequence[pos] == 'A':
            vector.append((1.0,0.0,0.0,0.0))
        elif sequence[pos] == 'C':
	        vector.append((0.0,1.0,0.0,0.0))
        elif sequence[pos] == 'G':
	        vector.append((0.0,0.0,1.0,0.0))
        elif sequence[pos] == 'T':
	        vector.append((0.0,0.0,0.0,1.0))
    return tuple(vector)
	

def parse_masoud_file(file_path):
    """Given the path to a file with a list of RNAs in the masoud format,
    the output is a dictionnary where keys are the name of the RNA
    and values probability vectors
    """
    tree_raw_info = [x.strip() for x in open(file_path)]
    dict_rnas = {}
    position = 0
    while position < len(tree_raw_info):
        if tree_raw_info[position][0] == '>':#Annouce a name.
            name = tree_raw_info[position][1:]#We don't want to keep '>'
            #The four next positions are the probs 
            masoud_vector = [tree_raw_info[position + x] 
                             for x in range(1,5)]
            dict_rnas[name] = masoud_to_probability_vector(masoud_vector)
            position += 5
        else:
            position += 1
    return dict_rnas
    
def parse_ancestors_file(file_path):
    """Given the path to a file with in the ancestor format,
    the output is a dictionnary where keys are the name of the RNA
    and values are the RNA-sequence
    """
    tree_raw_info = [x.strip() for x in open(file_path)]
    dict_nodes = {}
    dict_possible_leaves = {}
    position = 0
    #print tree_raw_info
    while position < len(tree_raw_info):
    	#print tree_raw_info[position]
    	if len(tree_raw_info[position]) > 1:
    		if tree_raw_info[position][0] == '>':#Annouce a node.
    			if tree_raw_info[position][1] == ' ':#It is not a leaf
    				name = tree_raw_info[position].strip('> ')#We don't want to keep '>'
    				name=name.rstrip('+')
    				dict_nodes[name]=tree_raw_info[position+1]#Add the nodes
    				if name.count('+') < 2:#If the nodes are the parents of a leave
    					leaf=name.split('+')
    					dict_nodes[leaf[0]]=dict_possible_leaves[leaf[0]]#Add one leaf 
    					dict_nodes[leaf[1]]=dict_possible_leaves[leaf[1]]#Add the other leaf
    			else:#It is a leaf
    				name = tree_raw_info[position].strip('>')#We don't want to keep '>'
    				dict_possible_leaves[name] = tree_raw_info[position+1]#Add the leaves to a temporary structure
    			position += 2
        	else:
        		position += 1
        else:
        	position +=1
    return dict_nodes

def parse_ancestors_prob_file(file_path):
    """Given the path to a file with in the ancestor_prob format,
    the output is a dictionnary where keys are the name of the RNA
    and values are the probability vectors
    """
    tree_raw_info = [x.strip() for x in open(file_path)]
    dict_nodes = {}
    dict_possible_leaves = {}
    vector = []
    position = 0
    flag_fill_tree = 0
    flag_fill_nodes = 1
    #print tree_raw_info
    while position < len(tree_raw_info):
    	#print tree_raw_info[position]
        if len(tree_raw_info[position]) > 1:
            if flag_fill_tree == 0:    	
                if tree_raw_info[position][0] == '>': #Annouce a leaf.
                    name = tree_raw_info[position].strip('>')#We don't want to keep '>'
                    dict_possible_leaves[name] = mickael_leaves_to_probability_vector(tree_raw_info[position+1])#Add the leaves to a temporary structur
                    position += 2
                else:
                    if tree_raw_info[position] == '#Corresponding tree, official classification':#Annouce that all the possible leaves hve been scanned
                          flag_fill_tree = 1
                    position += 1
            else:
                if flag_fill_nodes == 0:
                    if tree_raw_info[position][0] == '>':#Annouce a name.
                        name = tree_raw_info[position][1:]#We don't want to keep '>'
                        name=name[0:name.rfind('+')]#We don't want to keep '+   52' or something similar
                        name=name.strip()#We don't want to keep spaces
                        #The four next positions are the probs 
                        mickael_vector = [tree_raw_info[position + x] for x in range(1,5)]
                        dict_nodes[name] = mickael_to_probability_vector(mickael_vector)
                        position+=5
                        if name.count('+') < 3:#If the nodes are the parents of a leave
                            name=name.strip()
                            leaf=name.split('+')                           
                            dict_nodes[leaf[0]]=dict_possible_leaves[leaf[0]]#Add one leaf 
                            dict_nodes[leaf[1]]=dict_possible_leaves[leaf[1]]#Add the other leaf
                    else:
                        if '#Ancestors confidence levels' in tree_raw_info[position]:
                            flag_fill_nodes = 1
                        position +=1
                else:
                    if '#Ancestors probabilities ascii' in tree_raw_info[position]:#Annouce a node.
                        flag_fill_nodes = 0
                    position += 1
        else:
             position +=1
    return dict_nodes
   
def parse_ancestors_prob_file_all(file_path):
    """Given the path to a file with in the ancestor_prob format,
    the output is a dictionnary where keys are the name of the RNA
    and values are the probability vectors
    """
    tree_raw_info = [x.strip() for x in open(file_path)]
    dict_nodes = {}
    dict_possible_leaves = {}
    vector = []
    position = 0
    flag_fill_tree = 0
    flag_fill_nodes = 1
    #print tree_raw_info
    while position < len(tree_raw_info):
    	#print tree_raw_info[position]
        if len(tree_raw_info[position]) > 1:
            if flag_fill_tree == 0:    	
                if tree_raw_info[position][0] == '>': #Annouce a leaf.
                    name = tree_raw_info[position].strip('>')#We don't want to keep '>'
                    dict_nodes[name] = mickael_leaves_to_probability_vector(tree_raw_info[position+1])#Add the leaves to a temporary structur
                    position += 2
                else:
                    if tree_raw_info[position] == '#Corresponding tree, official classification':#Annouce that all the possible leaves hve been scanned
                          flag_fill_tree = 1
                    position += 1
            else:
                if flag_fill_nodes == 0:
                    if tree_raw_info[position][0] == '>':#Annouce a name.
                        name = tree_raw_info[position][1:]#We don't want to keep '>'
                        name=name[0:name.rfind('+')]#We don't want to keep '+   52' or something similar
                        name=name.strip()#We don't want to keep spaces
                        #The four next positions are the probs 
                        mickael_vector = [tree_raw_info[position + x] for x in range(1,5)]
                        dict_nodes[name] = mickael_to_probability_vector(mickael_vector)
                        position+=5
                        """if name.count('+') < 3:#If the nodes are the parents of a leave
                            name=name.strip()
                            leaf=name.split('+')                           
                            dict_nodes[leaf[0]]=dict_possible_leaves[leaf[0]]#Add one leaf 
                            dict_nodes[leaf[1]]=dict_possible_leaves[leaf[1]]#Add the other leaf
                        """    
                    else:
                        if '#Ancestors confidence levels' in tree_raw_info[position]:
                            flag_fill_nodes = 1
                        position +=1
                else:
                    if '#Ancestors probabilities ascii' in tree_raw_info[position]:#Annouce a node.
                        flag_fill_nodes = 0
                    position += 1
        else:
             position +=1
    return dict_nodes


def weighted_selection(elements, weights=None):
    """Takes as input two list. The first is the elements and in the same
    order the second list should contain their weights (default all equal) 
    in the same order. The output is a random element
    """
    if weights:
        #must make sure one of them is not float("inf"), else return it
        for i, w in enumerate(weights):
            if w == float("inf"):
                return elements[i]
        #else we pick random number,etc..
        r = random.uniform(0,sum(weights))
        sub_total = 0
        for i, w in enumerate(weights):
            sub_total += w
            if sub_total > r:
                return elements[i]
        return elements[i]
    else:
        return random.choice(elements)

def rna_bp_complement(nuc):
    """Given an rna nucleotide, will output the complement
    """
    if nuc == 'A':
        return 'U'
    elif nuc == 'C':
        return 'G'
    elif nuc == 'G':
        return 'C'
    elif nuc == 'U':
        return 'A'
    return None

def rand_rna(nuc_probs, bp_pos=None):
    """Generates a random RNA sequence given probs
    at each positions contained in "nuc_probs. It should be
    an iterable where each element in a 4-tuples (P_A, P_C_, P_G, P_U)
    """
    nucleotides = ['A', 'C', 'G', 'U']
    rna = []
    for i, position in enumerate(nuc_probs):
        if bp_pos:
            comp = [x[0] for x in bp_pos if x[1] == i]
            if len(comp) == 1:
                rna.append(rna_bp_complement(rna[comp[0]]))
                continue
        rna.append(weighted_selection(nucleotides, position))
    return ''.join(rna)

def rand_rna_population(probs, size=1000, bp_mask=None):
    """Generates "size" random RNAs given the probability
    vector "probs" who must be an iterator, the size
    of the desired RNA, where each position is a 4-tuple
    with the probs of the nucleotides: (P_A, P_C, P_G, P_U)
    """
    return [rand_rna(probs,bp_pos=bp_mask) for x in range(size)]

def mutate_rna(rna, mask=None, nuc_probs=None,
                               mutate_into_probs=None):
    """Given an rna sequence will output a mutated sequence. By default
    the probability of any nucleotide to mutate is 1/len(rna). The keyword
    argument "nuc_probs" can be given a dictionary the
    nucleotides and values the probability of each one mutating.
    The keyword "mask" can be given a secondary structure, and
    will make sure to make random compensatory mutations.
    Finally the keyword argument "mutate_into_probs" can be given
    as value a dictionnary with keys the nucleotides and value a list
    of weight for the probability of mutating into each one of the others.
    The order for the probabilities MUST be : [P_A, P_C, P_G, P_U] where
    P_X is the probability of mutating into nucleotide X. By default, 
    a nucleotide has a probability of 1/3 of mutating into any other.
    """
    rna = list(rna)#We work on a list, easier to mutate :).
    pool = ['A', 'C', 'G', 'U'] #Our nucleotides
    #If we don't have a mutation into probs, we give 1/3 to each
    if not mutate_into_probs:
        mutate_into_probs = {'A':[0,     1.0/3, 1.0/3, 1.0/3],
                             'C':[1.0/3, 0,     1.0/3, 1.0/3],
                             'G':[1.0/3, 1.0/3, 0,     1.0/3],
                             'U':[1.0/3, 1.0/3, 1.0/3, 0    ]}
    #if there is no mutation rate "nuc_probs", we give 1/100 to each one
    if not nuc_probs:
        nuc_probs = {x:1.0/len(rna) for x in ['A', 'U', 'C', 'G']}
    #If we have a mask, we prepare the list of base pairs
    if not mask:
        for i, nuc in enumerate(rna):
            if random.random() < nuc_probs[nuc]:
                rna[i] = weighted_selection(pool,mutate_into_probs[nuc])
    else:
        mask_bp = bp_positions(mask)
        for i, nuc in enumerate(rna):
            if random.random() < nuc_probs[nuc]:
                rna[i] = weighted_selection(pool,mutate_into_probs[nuc])
                #We check if there is a complement, if there is a mask
                cplt = find_complement_bp(i, mask_bp)
                if cplt and cplt[0] != i:
                    rna[cplt[0]] = rna_bp_complement(nuc)
                elif cplt and cplt[1] != i:
                    rna[cplt[1]] = rna_bp_complement(nuc)
    return ''.join(rna)

if __name__ == '__main__':

    print rand_rna([( 0, 0, 0, 1), ( 0,0,0,1)], bp_pos=[(0,1)])
