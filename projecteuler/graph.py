test_graph = {
    1:[2],
    2:[3,5],
    3:[1,4],
    4:[],
    5:[3]
    }
test_graph_small = {1:[2], 2:[1,3], 3:[]}
def cycles(graph, cycle_length, simple=True):
    """Find all cycles of the given number of nodes.
       Each cycle is only found once (i.e. no rotation duplicates).
       If simple, nodes cannot be present more than once in a cycle."""
    fully_explored = set()

    def rec(stack):
        result = []
        cur_node = stack[-1]
        for next_node in graph[cur_node]:
            if next_node in fully_explored:
                continue
            if next_node in stack:
                if next_node == stack[0] and len(stack) == cycle_length:
                    return [stack]
                elif simple:
                    continue
            if len(stack) == cycle_length:
                return []
            result.extend(rec(stack + [next_node]))
        return result

    result = []                
    for scc_nodes in strongly_connected_components(graph):
        if len(scc_nodes) < cycle_length:
            continue
        scc_graph = filter_graph(graph, scc_nodes)
        for node in sorted(scc_graph):
            result.extend(rec([node]))
            fully_explored.add(node)

    return result

def filter_graph(graph, node_whitelist):
    node_whitelist = set(node_whitelist)
    return {n:[n2 for n2 in graph[n] if n2 in node_whitelist]
            for n in graph if n in node_whitelist}            

def strongly_connected_components(graph):
    """
    Tarjan's Algorithm (named for its discoverer, Robert Tarjan) is a graph theory algorithm
    for finding the strongly connected components of a graph.
    
    Based on: http://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm

    This is some tricky shit right here.
    """

    index_counter = [0]
    stack = []
    lowlinks = {}
    index = {}
    result = []
    
    def strongconnect(node):
        # set the depth index for this node to the smallest unused index
        index[node] = index_counter[0]
        lowlinks[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)
    
        # Consider successors of `node`
        try:
            successors = graph[node]
        except:
            successors = []
        for successor in successors:
            if successor not in lowlinks:
                # Successor has not yet been visited; recurse on it
                strongconnect(successor)
                lowlinks[node] = min(lowlinks[node],lowlinks[successor])
            elif successor in stack:
                # the successor is in the stack and hence in the current strongly connected component (SCC)
                lowlinks[node] = min(lowlinks[node],index[successor])
        
        # If `node` is a root node, pop the stack and generate an SCC
        if lowlinks[node] == index[node]:
            connected_component = []
            
            while True:
                successor = stack.pop()
                connected_component.append(successor)
                if successor == node: break
            component = tuple(connected_component)
            # storing the result
            result.append(component)
    
    for node in graph:
        if node not in lowlinks:
            strongconnect(node)
    
    return result
