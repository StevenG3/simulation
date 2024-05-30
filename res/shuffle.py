import random
import math

def partial_shuffle(A, n, c):
    """
    Perform a partial Fisher-Yates shuffle to select c time slots from n.
    
    Parameters:
    A (list): List of time slots
    n (int): Number of nodes requiring transmission among neighbors
    c (int): Number of selected slots

    Returns:
    list: A list of c selected time slots
    """
    for i in range(c):
        j = random.randint(i, n - 1)
        A[i], A[j] = A[j], A[i]
    return A[:c]

'''
# Example usage:
time_slots = list(range(1, 11))  # Example list of time slots
n = len(time_slots)
c = 5  # Number of slots to select
selected_slots = partial_shuffle(time_slots, n, c)
print("Selected time slots:", selected_slots)
'''

def select_slots(y, n):
    p = y[0] / sum(y)
    c = math.ceil(p * n)
    A = list(range(1, n + 1))
    partial_shuffle(A, n, c)
    s = set()
    for i in range(c):
        s.add(A[i])
    return s

# Example usage
y = [10, 1, 1, 1, 1]  # Example queue lengths including self node
n = len(y)
selected_slots = select_slots(y, n)
print("Selected transmission slots:", selected_slots)