import math

#this class solve the graph coloring problem as a csp with backtracking search, ordering and forward checking.
class Graph_Coloring():
    
    # the method to initialize the graph coloring class
    def __init__(self, graph, domain):  # takes the csp graph and the domains(colors) as the input. the graph is defined as a dictionary.
        self.graph = graph
        self.variable = graph.keys()    # the keys of the dictionary would be the nodes of our graph 
        self.init_domain = domain
    
    # this method will choose an unassigned variable each time, by prioritizing the variable with the smallest domain.
    def select_variable(self, domain, assignment):  
        selected_variable = None 
        min_len = +math.inf
        for key in domain.keys():   # we search in nodes 
            if len(domain[key]) < min_len and key not in assignment.keys(): # to find unassigned nodes with the smallest domain to choose first 
                min_len = len(domain[key])
                selected_variable = key
        
        return selected_variable    # we return the found variable
           
    # forward checking would remove the assigned color of a node, from the domain of all of its neighbors.
    def forward_checking(self, variable, color_assigned, domain):
        succeed = False
        for neighbor in self.graph[variable]:
            for color in domain[neighbor]:
                if color == color_assigned:
                    domain[neighbor].remove(color)
        for key in domain.keys():
            if len(domain[key]) == 0:
                return succeed  # if the domain of a node gets empty along the way, it shows that the algorithm has failed 
        succeed = True  # else it would succeed 
        return succeed
            
    # the least-constraining-value heuristic is effective to order the values in the domain of a chosen variable.
    def value_ordering(self, variable, domain):
        ordering_values = {}
        for value in domain[variable]:
            cnt = 0
            for key in domain.keys():
                if key != variable:
                    if value in domain[key]:
                        cnt+=1      # we count the value thats been repeating in the domain of the node's neighbors 
            ordering_values[value] = cnt
        return sorted(domain[variable], key= lambda item: ordering_values[item]) # that value must be our last one to choose since it has the most effects on all other nodes' domains
        
    
    # backtracking search method is the principle method of this program, which solve the csp for us.(I used the book pseudo code to implement)
    def backtracking_search(self, assignment, domain):
        print(assignment)   #print each step of the algorithm to see the results 
        if len(assignment) == len(self.graph):
            return assignment   # if all nodes are assigned the algorithm would end 
        var = self.select_variable(domain, assignment)  # we choose the variable each time by the help of select_variable method
        
        for value in self.value_ordering(var,domain):   # for each color we have in the domain of the chosen variable
            consistent = True                           # we check whether this value(color) is consistent or not
            
            for variable in self.graph[var]:            # consistency would mean that no neighbor has the same value (color)
                if variable in assignment.keys():
                    if value == assignment[variable]:
                        consistent = False
                        
            if consistent:  # if the value is consistent 
                assignment[var] = value     # we assign that color to that node 
                before_domain = domain
                inference = self.forward_checking(var,value, domain)    # we do the forward checking
                if inference:       # if the forward checking succeeds
                    result = self.backtracking_search(assignment, domain)   # we do this algorithm recursively
                    if result != None:
                        return result
            assignment.remove({var:value})  # if it doesn't succeed we backtrack  
            domain = before_domain      # we must take back the changes to the domain too
        print("No solution found")      # that way no solution is found 
        return None
                
                    
# an example for a graph to be colored     
graph = {
            "A" : ["B", "C", "D"],
            "B" : ["A", "C", "F", "E"],
            "C" : ["A", "B", "D", "F"],
            "D" : ["A", "C", "F"],
            "E" : ["B", "F"],
            "F" : ["B", "C", "D", "E"]
            }

# domain is red, green and blue. abbreviated to R, G and B.
domain = {
            "A" : ["R", "G", "B"],
            "B" : ["R", "G", "B"],
            "C" : ["R", "G", "B"],
            "D" : ["R", "G", "B"],
            "E" : ["R", "G", "B"],
            "F" : ["R", "G", "B"]     
            }

assignment = {}
    
g = Graph_Coloring(graph,domain)
    
g.backtracking_search(assignment,domain)