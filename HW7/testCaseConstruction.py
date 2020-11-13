"""
Homework 6 Test Case Construction File
"""
import pickle
# TEST CASE 1
# This test case contains 10 different nodes
index = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
# Save the file using pickle
with open('datasets/test_index_10.pkl', 'wb') as handle:
   pickle.dump(index, handle)
# We can define adjacency lists for each node. For example,
# node 0 has an edge that points to node 9. Do not worry about,
# the third element in each tuple for this assignment.
links = [('0', ['9'], 0),
        ('1', ['6'], 0),
        ('2', [], 0),
        ('3', ['4'], 0),
        ('4', ['3'], 0),
        ('5', [], 0),
        ('6', [], 0),
        ('7', ['6'], 0),
        ('8', ['1', '6', '7'], 0),
        ('9', ['2'], 0)]
# Save the file using pickle
with open('datasets/articles_with_links_10.pkl', 'wb') as handle:
   pickle.dump(links, handle)
# TEST CASE 2
index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
with open('datasets/test_index_13.pkl', 'wb') as handle:
   pickle.dump(index, handle)
links = [('A', ['A', 'B'], 0),
        ('B', ['B', 'C'], 0),
        ('C', ['C'], 0),
        ('D', ['E'], 0),
        ('E', ['E'], 0),
        ('F', ['G'], 0),
        ('G', ['H'], 0),
        ('H', ['I'], 0),
        ('I', ['G', 'J'], 0),
        ('J', [], 0),
        ('K', ['L'], 0),
        ('L', ['L', 'M'], 0),
        ('M', [], 0)]
with open('datasets/articles_with_links_13.pkl', 'wb') as handle:
   pickle.dump(links, handle)
