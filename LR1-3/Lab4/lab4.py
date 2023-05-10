import lab1
import json
import re
import sys

# лексемы
tokens = {'W': {}, 'I': {}, 'O': {}, 'R': {}, 'N': {}, 'C': {}}

# файлы, содержащие все таблицы лексем
for token_class in tokens.keys():
    with open('%s.json' % token_class, 'r') as read_file:
        data = json.load(read_file)
        tokens[token_class] = data

# файл, содержащий последовательность кодов лексем входной программы
f = open('tokens.txt', 'r')
input_sequence = f.read()
f.close()

regexp = '[' + '|'.join(tokens.keys()) + ']' + '\d+'
match = re.findall(regexp, input_sequence)

i = -1 # индекс разбираемого символа
nxtsymb = None # разбираемый символ
row_counter = 1 # счётчик строк

# обработка ошибочной ситуации
def error():
    print('Ошибка в строке', row_counter)
    sys.exit()

# помещение очередного символа в nxtsymb
def scan():
    global i, nxtsymb, row_counter
    i += 1
    if i >= len(match):
        if not(nxtsymb in ['\n', ';', '}']):
            error()
    else:
        for token_class in tokens.keys():
            if match[i] in tokens[token_class]:
                nxtsymb = tokens[token_class][match[i]]
        if nxtsymb == '\n':
            row_counter += 1
            scan()
        print(i, row_counter, nxtsymb)

# программа
def program():
    operators()

# операторы
def operators():
    global i
    scan()
    while name() or \
          nxtsymb in ['int', 'double', 'string', 'boolean', 'float', '{', 'public static void main(String[] args)',\
                      'if', 'for', 'while', 'break', 'continue', 'return']:
        operator()
        if nxtsymb == ';':
            scan()
        if nxtsymb == '}':
            break

# оператор
def operator():
    if nxtsymb in ['int','double','float','boolean','string']:
        description()
        if nxtsymb != ';': error()
    elif name():
        scan()
        if nxtsymb == ':':
            scan()
            operator()
        elif nxtsymb == '(':
            scan()
            if nxtsymb != ')':
                expression()
                while nxtsymb == ',':
                    scan()
                    expression()
                if nxtsymb != ')': error()
            scan()
        elif nxtsymb == '=':
            scan()
            expression()
            if nxtsymb != ';': error()
        else: error()
    elif nxtsymb == '{': compound_operator()
    elif nxtsymb == 'public static': function()
    elif nxtsymb == 'if': conditional_operator()
    elif nxtsymb == 'for': for_loop()
    elif nxtsymb == 'while': while_loop()
    elif nxtsymb == 'break':
        break_operator()
        scan()
        if nxtsymb != ';': error()
    elif nxtsymb == 'continue':
        continue_operator()
        scan()
        if nxtsymb != ';': error()
    elif nxtsymb == 'return':
        return_operator()
        if nxtsymb != ';': error()
    else: error()

# имя (идентификатор)
def name():
    return nxtsymb in tokens['I'].values() or \
           nxtsymb in ['System.out.println', 'alert']

# описание
def description():
    scan()
    if not(name()): error()
    scan()
    if nxtsymb == ',':
        while nxtsymb == ',':
            scan()
            if not(name()): error()
            scan()
    elif nxtsymb == '=':
        scan()
        if nxtsymb == 'new':
            scan()
            if not(name()): error()
            if not(nxtsymb == '['): error()
            scan()
            if not(integer()): error()
            scan()
            if not(nxtsymb == ']'): error()
            scan()
        else:
            expression()

# список имен
def list_of_names():
    if not(name()): error()
    scan()
    while nxtsymb == ',':
        scan()
        if not(name()): error()
        scan()

# функция
def function():
    if nxtsymb != 'public static void main(String[] args)\n{': error()
    scan()
    if not(name()): error()
    scan()
    if nxtsymb == '(':
        scan()
        if name():
            list_of_names()
    if nxtsymb != ')': error()
    scan()
    compound_operator()

# выражение
def expression():
    if nxtsymb == '(':
        scan()
        expression()
        if nxtsymb != ')': error()
        scan()
    elif name():
        scan()
        if nxtsymb == '(':
            scan()
            if nxtsymb != ')':
                expression()
                while nxtsymb == ',':
                    scan()
                    expression()
                if nxtsymb != ')': error()
            scan()
        elif nxtsymb == '[':
            scan()
            expression()
            while nxtsymb == ',':
                scan()
                expression()
            if nxtsymb != ']': error()
            scan()
    elif number() or line(): scan()
    else: error()
    if arithmetic_operation():
        scan()
        expression()

# число (числовая константа)
def number():
    return nxtsymb in tokens['N'].values()

# целое число (числовая константа)
def integer():
    return nxtsymb in tokens['N'].values()

# # вещественное число (числовая константа)
# def real_number():
#     return nxtsymb in tokens['N'].values()

# строка (символьная константа)
def line():
    return nxtsymb in tokens['C'].values()

# переменная
def variable():
    if not(name()): error()
    scan()
    if nxtsymb == '[':
        scan()
        expression()
        if nxtsymb != ']': error()
        scan()

# арифметическая операция
def arithmetic_operation():
    return nxtsymb in ['%', '*', '+', '-', '/', '+=','-=', '*=', '/=', '%=']

# составной оператор
def compound_operator():
    if nxtsymb != '{': error()
    operators()
    if nxtsymb != '}': error()
    scan()

# оператор присваивания
def assignment_operator():
    scan()
    variable()
    if nxtsymb != '=': error()
    scan()
    expression()

# условный оператор
def conditional_operator():
    if nxtsymb != 'if': error()
    scan()
    if nxtsymb != '(': error()
    condition()
    if nxtsymb != ')': error()
    scan()
    operator()
    if nxtsymb == 'else':
        scan()
        operator()

# условие
def condition():
    if unary_log_operation():
        scan()
        if nxtsymb != '(': error()
        log_expression()
        if nxtsymb != ')': error()
        scan()
    else:
        log_expression()
        while binary_log_operation():
            log_expression()

# унарная логическая операция
def unary_log_operation():
    return nxtsymb == '!'

# логическое выражение
def log_expression():
    scan()
    expression()
    comparison_operation()
    scan()
    expression()

# операция сравнения
def comparison_operation():
    return nxtsymb in ['!=', '<', '<=', '==', '>', '>=']

# бинарная логическая операция
def binary_log_operation():
    return nxtsymb == '&&' or nxtsymb == '||'

# цикл for
def for_loop():
    if nxtsymb != 'for': error()
    scan()
    if nxtsymb != '(': error()
    assignment_operator()
    if nxtsymb != ';': error()
    condition()
    if nxtsymb != ';': error()
    assignment_operator()
    if nxtsymb != ')': error()
    scan()
    operator()

# цикл while
def while_loop():
    if nxtsymb != 'while': error()
    scan()
    if nxtsymb != '(': error()
    condition()
    if nxtsymb != ')': error()
    scan()
    operator()

# оператор break
def break_operator():
    return nxtsymb == 'break'

# оператор continue
def continue_operator():
    return nxtsymb == 'continue'

# оператор return
def return_operator():
    if nxtsymb != 'return': error()
    scan()
    expression()

program()
