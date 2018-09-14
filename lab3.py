import fileinput
import ast
import re

def format(line):

    # split string on semicolon, create list
    list_strings_in_2 = line.split(";")
    print(list_strings_in_2)

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

    print(lists)
    return lists

def main():
    # example input
    '''
    2
    (A); (B); (C)
    (A, C); X; X
    '''
    input = fileinput.input()
    in_line_1 = int(input[0])
    in_line_2 = format(input[1])
    in_line_3 = format(input[2])

    #in_line_2 = '(B, A); (C, D, E); ()'

    print("Line 1: %d\nLine 2: %s\nLine 3: %s" % (in_line_1, in_line_2, in_line_3))

if __name__ == "__main__":
    main()
