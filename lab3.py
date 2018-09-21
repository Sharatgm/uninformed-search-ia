import fileinput
import ast
import re
from pprint import pprint


def format_input(line):

    # split string on semicolon, create list
    list_strings_in_2 = line.split(";")
    # print(list_strings_in_2)

    lists = []
    for x in list_strings_in_2:
        # for each element on the list, delete parenthesis, whitespaces and commas

        # replace parenthesis for brackets
        x = x.replace("(", "")
        x = x.replace(")", "")

        # remove white spaces
        x = x.replace(" ", "")

        # remove commas
        x = x.replace(",", "")

        # remove \n
        x = x.replace("\n", "")

        # apend list to list
        lists.append(list(x))

    # print(lists)
    return lists

def heuristic(state, goal, type):
    elements = 0
    count = 0
    blocks = {}

    if(type == 1): # Heuristic = 0
        return 0
    elif(type == 2): # Consistent 1
        for i,stack in enumerate(goal):
            elements += len(stack)
            for j,block in enumerate(stack):
                if(len(state[i]) > j):
                    if(state[i][j] == block):
                        count += 1
        return elements - count
    elif(type == 3): # Consistent 2
        for i,stack in enumerate(goal):
            for j,block in enumerate(stack):
                blocks[block] = i

        for i,stack in enumerate(state):
            for j,block in enumerate(stack):
                if block in blocks:
                    diff = abs(i-blocks[block])
                    if (diff != 0 ):  count += (diff + 1)
        return count

    elif(type == 4): # Inconsistent
        for i,stack in enumerate(goal):
            elements += len(stack)
            for j,block in enumerate(stack):
                if(len(state[i]) > j ):
                    if(state[i][j] == block):
                        count += 1
        return elements - count + len(goal)

def get_wildcards(input_goal):
    wildcards = []
    for index, stack in enumerate(input_goal):
        if 'X' in stack:
            wildcards.append(index)
    return wildcards


def remove_wildcards_from_stacks(input_goal):
    for stack in input_goal:
        if 'X' in stack:
            stack.pop()
    return input_goal

def search_state_in_frontier(state, frontier):
    for i,node in enumerate(frontier):
        if(node['state'] == state):
            return i
    return -1

def expand(frontier, h, node, visited, goal, type):
    state = node['state'].copy()
    # Loop in every stack of state
    for i in range(0, len(state)):
        stack = state[i].copy() # Select stack from state
        for j in range(0, len(state)):  # Loop every stack to check where to move
            new_state = state.copy()
            if(j != i): # Avoid trying to move a block from stack x to the same stack x
                stack2 = state[j].copy()
                if(len(stack2) < h and len(stack) > 0): # If stack2 has space and stack has blocks to move
                    block = stack[len(stack)-1]
                    new_state[i] = stack.copy()
                    new_state[i].remove(block)
                    new_state[j] = stack2
                    new_state[j] += [block]
                    action = (i,j)
                    cost = (max(j,i)-min(j,i)) + 1 + node['cost'] + heuristic(state, goal['state'], type)
                    new_node = {'state': new_state, 'cost': cost, 'parent': node['state'], 'action': action}
                    #print("New node = ", new_node)
                    node_in_frontier = search_state_in_frontier(new_state, frontier)
                    node_in_visited = search_state_in_frontier(new_state, visited)
                    if(node_in_visited == -1):
                        if (node_in_frontier != -1):
                            if(frontier[node_in_frontier]['cost'] > cost):
                                del frontier[node_in_frontier]
                                frontier.append(new_node)
                                #print("New node = ", new_node)
                        else:
                            frontier.append(new_node)
                            #print("New node = ", new_node)

    return frontier

def test_goal(node, goal):
    for index, stack in enumerate(node['state']):
        if index not in goal['wildcards']:
            if stack != goal['state'][index]:
                return False
    return True


def display_goal(goal_node, visited):
    # do the back track to parent nodes starting with goal_node
    cost = goal_node['cost']
    actions = []
    node = goal_node
    while True:
        actions.append(node['action'])
        parent_node = list(filter(lambda visited_node: visited_node['state'] == node['parent'], visited))[0]
        # parent_node = visited.pop(index)
        if parent_node['parent'] is None:
            break
        node = parent_node
    actions.reverse()
    print(cost)
    print(str(actions).replace("[", "").replace("]", "").replace("),", ");"))
    pass

def search(max_h, goal, initial_state, type):
    # Frontier list: list of dictionaries in format:
    # node = {state: [[a, b], [c], []], cost: 4, parent: [[a, b, c], [], []], action: (1, 2)}
    initial_node = {'state': initial_state, 'cost': 0, 'parent': None, 'action': None}
    frontier = [initial_node]
    # list of nodes visited
    visited = []
    while True:
        if len(frontier) == 0:
            print("No solution found")
            return False
        frontier = sorted(frontier, key=lambda n: n['cost'])
        node = frontier.pop(0)
        if test_goal(node, goal):
            display_goal(node, visited)
            return True
        visited.append(node)
        frontier = expand(frontier, max_h, node, visited, goal, type)



def test_display_goal_function():
    visited_nodes = [
        {'state': [['a', 'b', 'c'], [], []], 'cost': 0, 'parent': None, 'action': None},
        {'state': [['a', 'b'], ['c'], []], 'cost': 1, 'parent': [['a', 'b', 'c'], [], []], 'action': (0, 1)},
        {'state': [['a'], ['c'], ['b']], 'cost': 2, 'parent': [['a', 'b'], ['c'], []], 'action': (0, 2)},
        {'state': [['a', 'c'], [], ['b']], 'cost': 3, 'parent': [['a'], ['c'], ['b']], 'action': (1, 0)}
    ]
    visited = []
    frontier = []
    goal_node = {'state': [['a', 'c'], [], ['b']], 'cost': 3, 'parent': [['a'], ['c'], ['b']], 'action': (1, 0)}
    #display_goal(goal_node, visited_nodes)
    expand(frontier, 3, {'state': [['b', 'a'], ['c','d','e'], []], 'cost': 0, 'parent': None, 'action': None}, visited_nodes, {'state': [['d', 'e'], [], []], 'cost': 3, 'parent': [['a'], ['c'], ['b']], 'action': (1, 0)}, 1)

def main():
    # example input
    '''
    2
    (A); (B); (C)
    (A, C); X; X
    '''
    file_input = fileinput.input()
    max_h = int(file_input[0])
    initial_state = format_input(file_input[1])
    input_goal = format_input(file_input[2])

    # goal dictionary:
    # - state: stacks with the desired position of the containers
    # - wildcards: list of indexes of stacks where the order of the containers is not important
    wildcards = get_wildcards(input_goal)
    input_goal = remove_wildcards_from_stacks(input_goal)
    goal = {'state': input_goal, 'wildcards': wildcards}

    #print("Line 1: %d\nLine 2: %s\nLine 3: %s" % (max_h, initial_state, goal))
    heuristic=1
    search(max_h, goal, initial_state, heuristic)


if __name__ == "__main__":
    #test_display_goal_function()
    main()
