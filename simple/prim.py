import sys
from collections import defaultdict, deque

class Prim:
    def __init__(self):
        pass

    def prim(self, adj_matrix, root_id):
        num_nodes = len(adj_matrix)
        in_tree = [False] * num_nodes
        distance = [sys.maxsize] * num_nodes
        parent = [-1] * num_nodes

        # Start with the root node
        distance[root_id] = 0

        for _ in range(num_nodes):
            # Find the node with the minimum distance which is not yet included in the tree
            u = min((d, idx) for idx, d in enumerate(distance) if not in_tree[idx])[1]
            in_tree[u] = True

            # Update the distance and parent of the adjacent vertices of the picked vertex
            for v in range(num_nodes):
                if 0 < adj_matrix[u][v] < distance[v] and not in_tree[v]:
                    distance[v] = adj_matrix[u][v]
                    parent[v] = u

        return parent

    def build_depth_lists(self, parent, root_id, depth):
        depth_lists = defaultdict(list)
        queue = deque([(root_id, 0)])
        
        while queue:
            node, d = queue.popleft()
            if d > depth:
                continue
            depth_lists[d].append(node)

            # Enqueue children
            for child_id, p in enumerate(parent):
                if p == node:
                    queue.append((child_id, d + 1))
        
        # Fill in all levels up to 'depth' even if they are empty
        return [depth_lists[d] for d in range(depth + 1)]

    def prim_with_depth(self, adj_matrix, root_id, depth):
        parent = self.prim(adj_matrix, root_id)
        return self.build_depth_lists(parent, root_id, depth)

    # Example adjacency matrix (for testing)
    # adj_matrix = [
    #     [0, 2, 0, 6, 0],
    #     [2, 0, 3, 8, 5],
    #     [0, 3, 0, 0, 7],
    #     [6, 8, 0, 0, 9],
    #     [0, 5, 7, 9, 0],
    # ]
    # root_id = 0
    # max_depth = 3

    # # Get the result
    # result = prim_with_depth(adj_matrix, root_id, max_depth)
    # print(result)