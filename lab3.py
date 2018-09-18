import fileinput
import ast
import re


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


def uniform_cost_search(max_h, goal, initial_state):
    # Frontier list: list of dictionaries in format:
    # node = {state: [[a, b], [c], []], cost: 4, parent: [[a, b, c], [], []], action: (1, 2)}
    initial_node = {'state': initial_state, 'cost': 0, 'parent': None, 'action': None}
    frontier = [initial_node]
    # list of nodes visited
    visited = []
    while True:
        if len(frontier) == 0:
            return False
        node = frontier.pop()
        if test_goal(node, goal):
            display_goal(node, visited)
            return True
        visited.append(node)
        frontier = expand(frontier, max_h, node)


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
    print(actions)
    return


def test_display_goal_function():
    visited_nodes = [
        {'state': [['a', 'b', 'c'], [], []], 'cost': 0, 'parent': None, 'action': None},
        {'state': [['a', 'b'], ['c'], []], 'cost': 1, 'parent': [['a', 'b', 'c'], [], []], 'action': (0, 1)},
        {'state': [['a'], ['c'], ['b']], 'cost': 2, 'parent': [['a', 'b'], ['c'], []], 'action': (0, 2)},
        {'state': [['a', 'c'], [], ['b']], 'cost': 3, 'parent': [['a'], ['c'], ['b']], 'action': (1, 0)}
    ]
    goal_node = {'state': [['a', 'c'], [], ['b']], 'cost': 3, 'parent': [['a'], ['c'], ['b']], 'action': (1, 0)}
    display_goal(goal_node, visited_nodes)


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

    print("Line 1: %d\nLine 2: %s\nLine 3: %s" % (max_h, initial_state, goal))

    # uniform_cost_search(max_h, goal, initial_state)


if __name__ == "__main__":
    test_display_goal_function()
    #main()
