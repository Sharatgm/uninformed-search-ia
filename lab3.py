import fileinput
import ast
import re
# example input
'''
2
(A); (B); (C)
(A, C); X; X
'''
#input = fileinput.input()
#in_line_1 = input[0]
#in_line_2 = input[1]
#in_line_3 = input[2]

in_line_2 = '(B, A); ("C", "D", "E"); ()'

# replace parenthesis for brackets
in_line_2 = in_line_2.replace("(", "[")
in_line_2 = in_line_2.replace(")", "]")

# remove white spaces
in_line_2 = in_line_2.replace(" ", "")

# split string on semicolon, create list
list_strings_in_2 = in_line_2.split(";")
print(list_strings_in_2)

lists = []
for x in list_strings_in_2:
    # for each element on the list, evaluate string value into list of strings
    # ast input expected format:
    # ast.literal_eval('["A","B" ,"C" ," D"]')

    # change format of states from A to "A" with regex
    x = re.sub(r'', r'', x)

    # apend list to list
    lists.append(ast.literal_eval(x))
    print(lists)

print(lists)

