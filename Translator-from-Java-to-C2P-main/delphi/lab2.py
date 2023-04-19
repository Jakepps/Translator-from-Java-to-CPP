import lab1
import json
import re

CLASSES_OF_TOKENS = ['W', 'I', 'O', 'R', 'N', 'C']

def is_identifier(token):
    return re.match(r'^I\d+$', inverse_tokens[token]) or \
           token in ['abs', 'cos', 'exp', 'ln', 'read', 'readln', 'sin', 'sqrt', \
                     'write', 'writeln']

def get_priority(token):
    if token in ['(', 'for', 'if', 'repeat', 'while', '[', 'АЭМ', 'Ф', 'begin']:
        return 0
    if token in [')', ',', ';', 'do', 'downto', 'else', 'then', 'to', 'until', ']']:
        return 1
    if token == ':=' or token == 'goto':
        return 2
    if token == 'or':
        return 3
    if token == 'and':
        return 4
    if token == 'not':
        return 5
    if token in ['<', '<=', '<>', '=', '>', '>=']:
        return 6
    if token == '+' or token == '-':
        return 7
    if token in ['*', '/', 'div', 'mod']:
        return 8
    if token in ['end', 'function', 'procedure', 'program', 'var']:
        return 9
    return -1

def description_var(block, out_seq):
    i = 0
    var_count = 0
    while i < len(block):
        while i < len(block) and block[i] != ':':
            if not(block[i] in ['\n', ',', ';']):
                out_seq += block[i] + ' '
                var_count += 1
            i += 1
        if i == len(block):
            break
        i += 1
        if block[i] == 'array':
            i += 1
            aem_count = 1
            while block[i] != ']':
                if block[i] == ',':
                    out_seq += '.. '
                    aem_count += 1
                else:
                    out_seq += block[i] + ' '
                i += 1
            i += 2
            aem_count += 1
            out_seq += '.. ' + str(aem_count) + ' АЭМ '
        out_seq += str(var_count) + ' ' + block[i] + ' '
        var_count = 0
        i += 1
    return out_seq

# лексемы (код-значение)
tokens = {}

# файлы, содержащие все таблицы лексем
for token_class in CLASSES_OF_TOKENS:
    with open('%s.json' % token_class, 'r') as read_file:
        data = json.load(read_file)
        tokens.update(data)

# лексемы (значение-код)
inverse_tokens = {val: key for key, val in tokens.items()}

# файл, содержащий последовательность кодов лексем входной программы
f = open('tokens.txt', 'r')
inp_seq = f.read()
f.close()

regexp = '[' + '|'.join(CLASSES_OF_TOKENS) + ']' + '\d+'
match = re.findall(regexp, inp_seq)

t = [tokens[i] for i in match]

i = 0
stack = []
out_seq = ''
aem_count = proc_level = 1
func_count = tag_count = proc_num = if_count = while_count = repeat_count = \
             for_count = begin_count = end_count = 0
is_func = False
while i < len(t):
    p = get_priority(t[i])
    if t[i] == '.':
        stack.pop()
        out_seq += 'КП '
    elif p == -1:
        if t[i] != '\n':
            out_seq += t[i] + ' '
        if is_func and t[i + 1] == '(':
            i += 2
            block = []
            while t[i] != ')':
                block.append(t[i])
                i += 1
            out_seq = description_var(block, out_seq)
            i -= 1
            is_func = False
    else:
        if t[i] == '[':
            aem_count += 1
            stack.append(str(aem_count) + ' АЭМ')
        elif t[i] == ']':
            while not(re.match(r'^\d+ АЭМ$', stack[-1])):
                out_seq += stack.pop() + ' '
            out_seq += stack.pop() + ' '
            aem_count = 1
        elif t[i] == '(':
            if is_identifier(t[i - 1]):
                func_count += 1
                stack.append(str(func_count) + ' Ф')
            else:
                stack.append(t[i])
        elif t[i] == ')':
            if t[i + 1] == ':':
                i += 2
                out_seq += '1 ' + t[i] + ' КО '
            else:
                while stack[-1] != '(' and not(re.match(r'^\d+ Ф$', stack[-1])):
                    out_seq += stack.pop() + ' '
                if re.match(r'^\d+ Ф$', stack[-1]):
                    stack.append(str(func_count + 1) + ' Ф')
                    func_count = 0
            stack.pop()
        elif t[i] == ',':
            while not(re.match(r'^\d+ АЭМ$', stack[-1])) and \
                  not(re.match(r'^\d+ Ф$', stack[-1])):
                out_seq += stack.pop() + ' '
            if re.match(r'^\d+ АЭМ$', stack[-1]):
                aem_count += 1
                stack.append(str(aem_count) + ' АЭМ')
            if re.match(r'^\d+ Ф$', stack[-1]):
                func_count += 1
                stack.append(str(func_count) + ' Ф')
            stack.pop()
        elif t[i] == 'goto':
            out_seq += t[i + 1] + ' БП '
            i += 2
        elif t[i] == 'if':
            stack.append(t[i])
            if_count += 1
        elif t[i] == 'then':
            while stack[-1] != 'if':
                out_seq += stack.pop() + ' '
            tag_count += 1
            stack[-1] += ' М' + str(tag_count)
            out_seq += 'М' + str(tag_count) + ' УПЛ '
        elif t[i] == 'else':
            while not(re.match(r'^if М\d+$', stack[-1])):
                out_seq += stack.pop() + ' '
            stack.pop()
            tag_count += 1
            stack.append('if М' + str(tag_count))
            out_seq += 'М' + str(tag_count) + ' БП М' + str(tag_count - 1) + ' : '
        elif t[i] == 'while':
            tag_count += 1
            stack.append(t[i] + ' М' + str(tag_count))
            out_seq += 'М' + str(tag_count) + ' : '
            while_count += 1
        elif t[i] == 'do':
            while not(re.match(r'^while М\d+$', stack[-1])) and \
                  not(re.match(r'^for [a-z][a-z\d]+ М\d+$', stack[-1])):
                out_seq += stack.pop() + ' '
            tag_count += 1
            if re.match(r'^for [a-z][a-z\d]+ М\d+$', stack[-1]):
                out_seq += '<= '
            out_seq += 'М' + str(tag_count) + ' УПЛ '
            stack[-1] += ' М' + str(tag_count)
        elif t[i] == 'repeat':
            tag_count += 1
            stack.append(t[i] + ' М' + str(tag_count))
            out_seq += 'М' + str(tag_count) + ' : '
            repeat_count += 1
        elif t[i] == 'until':
            while not(re.match(r'^repeat М\d+$', stack[-1])):
                out_seq += stack.pop() + ' '
        elif t[i] == 'for':
            stack.append(t[i] + ' ' + t[i + 1])
            for_count += 1
        elif t[i] == 'to':
            while not(re.match(r'^for [a-z][a-z\d]+$', stack[-1])):
                out_seq += stack.pop() + ' '
            variable = re.search('[a-z][a-z\d]', stack[-1]).group(0)
            tag_count += 1
            stack[-1] += ' М' + str(tag_count)
            out_seq += 'М' + str(tag_count) + ' : ' + variable + ' '
        elif t[i] == 'var':
            block = []
            i += 1
            while not(t[i] in ['begin', 'function', 'procedure']):
                block.append(t[i])
                i += 1
            i -= 1
            out_seq = description_var(block, out_seq)
            out_seq += str(proc_num) + ' ' + str(proc_level) + ' КО '
        elif t[i] in ['function', 'procedure', 'program']:
            if t[i] == 'function' or t[i] == 'procedure':
                is_func = True
            proc_num += 1
            stack.append('PROC ' + str(proc_num) + ' ' + str(proc_level))
        elif t[i] == 'begin':
            begin_count += 1
            proc_level = begin_count - end_count + 1
            stack.append(t[i])
        elif t[i] == 'end':
            end_count += 1
            proc_level = begin_count - end_count + 1
            while stack[-1] != 'begin':
                out_seq += stack.pop() + ' '
            stack.pop()
            if not(if_count > 0 and re.match(r'^if М\d+$', stack[-1])) and \
               not(while_count > 0 and re.match(r'^while М\d+ М\d+$', stack[-1])) and \
               not(for_count > 0 and re.match(r'^for [a-z][a-z\d]+ М\d+ М\d+$', stack[-1])):
                stack.append(t[i])
        elif t[i] == ';':
            if len(stack) > 0 and re.match(r'^PROC', stack[-1]):
                num = re.findall(r'\d+', stack[-1])
                stack.pop()
                out_seq += str(num[0]) + ' ' + str(num[1]) + ' НП '
            elif len(stack) > 0 and stack[-1] == 'end':
                stack.pop()
                out_seq += 'КП '
            elif if_count > 0 or while_count > 0 or repeat_count > 0 or \
                 for_count > 0:
                while not(len(stack) > 0 and stack[-1] == 'begin') and \
                      not(if_count > 0 and re.match(r'^if М\d+$', stack[-1])) and \
                      not(while_count > 0 and re.match(r'^while М\d+ М\d+$', stack[-1])) and \
                      not(repeat_count > 0 and re.match(r'^repeat М\d+$', stack[-1])) and \
                      not(for_count > 0 and re.match(r'^for [a-z][a-z\d]+ М\d+ М\d+$', stack[-1])):
                    out_seq += stack.pop() + ' '
                if if_count > 0 and re.match(r'^if М\d+$', stack[-1]):
                    tag = re.search('М\d+', stack[-1]).group(0)
                    out_seq += tag + ' : '
                    if_count -= 1
                if while_count > 0 and re.match(r'^while М\d+ М\d+$', stack[-1]):
                    tag = re.findall('М\d+', stack[-1])
                    out_seq += tag[0] + ' БП ' + tag[1] + ' : '
                    while_count -= 1
                if repeat_count > 0 and re.match(r'^repeat М\d+$', stack[-1]):
                    tag_count += 1
                    out_seq += str(tag_count) + ' УПЛ '
                    tag = re.search('М\d+', stack[-1]).group(0)
                    out_seq += tag + ' БП ' + str(tag_count) + ' : '
                    repeat_count -= 1
                if for_count > 0 and re.match(r'^for [a-z][a-z\d]+ М\d+ М\d+$', stack[-1]):
                    out_seq += '1 + := '
                    tag = re.findall('М\d+', stack[-1])
                    out_seq += tag[0] + ' БП ' + tag[1] + ' : '
                    for_count -= 1
                if len(stack) > 0 and stack[-1] != 'begin':
                    stack.pop()
            else:
                while len(stack) > 0 and stack[-1] != 'begin':
                    out_seq += stack.pop() + ' '
        else:
            while len(stack) > 0 and get_priority(stack[-1]) >= p:
                out_seq += stack.pop() + ' '
            stack.append(t[i])
    i += 1

while len(stack) > 0:
    out_seq += stack.pop() + ' '

# файл, содержащий обратную польскую запись
f = open('reverse_polish_entry.txt', 'w')
f.write(out_seq)
f.close()
