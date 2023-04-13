import lab2
import json
import re

CLASSES_OF_TOKENS = ['W', 'I', 'O', 'R', 'N', 'C']

def is_identifier(token):
    return ((token in inverse_tokens) and re.match(r'^I\d+$', inverse_tokens[token])) or token in ['abs', 'cos', 'exp', 'ln', 'read', 'readln', 'sin', 'sqrt', 'write', 'writeln'] or re.match(r'^М\d+$', token)

def is_constant(token):
    return ((token in inverse_tokens) and re.match(r'^C\d+$', inverse_tokens[token])) or ((token in inverse_tokens) and re.match(r'^N\d+$', inverse_tokens[token])) or token.isdigit()

def is_operation(token):
    return (token in inverse_tokens) and re.match(r'^O\d+$', inverse_tokens[token])

# лексемы (код-значение)
tokens = {}

# файлы, содержащие все таблицы лексем
for token_class in CLASSES_OF_TOKENS:
    with open('%s.json' % token_class, 'r') as read_file:
        data = json.load(read_file)
        tokens.update(data)

# лексемы (значение-код)
inverse_tokens = {val: key for key, val in tokens.items()}

replace = {'abs': 'Math.abs', 'cos': 'Math.cos', 'exp': 'Math.exp', 'ln': 'Math.log', 'read': 'prompt', 'readln': 'prompt', 'sin': 'Math.sin', 'sqrt': 'Math.sqrt', 'write': 'alert', 'writeln': 'alert', ':=': '=', 'or': '||', 'and': '&&', '<>': '!=', '=': '==', 'div': '/', 'mod': '%', 'not': '!'}

# файл, содержащий обратную польскую запись
f = open('reverse_polish_entry.txt', 'r')
inp_seq = f.read()
f.close()

t = re.findall(r'(?:\'[^\']*\')|(?:[^ ]+)', inp_seq)

i = 0
stack = []
out_seq = ''
is_func = False
while i < len(t):
    if is_func == True and not(is_identifier(t[i])):
        out_seq += '() {\n'
        is_func = False
    if is_identifier(t[i]) or is_constant(t[i]):
        stack.append(replace[t[i]] if t[i] in replace else t[i])
    elif t[i] == 'НП':
        stack.pop()
        stack.pop()
        arg1 = stack.pop()
        out_seq += f'function {arg1}'
        is_func = True
    elif t[i] == 'КП':
        out_seq += '}'
    elif t[i] in ['integer', 'real', 'string']:
        k = int(stack.pop())
        a = []
        while k != 0:
            a.append(stack.pop())
            k -= 1
        a.reverse()
        out_seq += 'var ' + ', '.join(a) + ';\n'
    elif t[i] == 'КО':
        stack.pop()
        stack.pop()
    elif t[i] == 'УПЛ':
        arg1 = stack.pop()
        arg2 = stack.pop()
        out_seq += f'if (!({arg2})) goto {arg1};\n'
    elif t[i] == 'БП':
        arg1 = stack.pop()
        out_seq += f'goto {arg1};\n'
    elif t[i] == ':':
        arg1 = stack.pop()
        out_seq += f'{arg1}: '
    elif is_operation(t[i]):
        if t[i] == ':=':
            arg1 = stack.pop()
            arg2 = stack.pop()
            out_seq += f'{arg2} = {arg1};\n'
        else:
            operation = replace[t[i]] if t[i] in replace else t[i]
            arg1 = stack.pop()
            if t[i] != 'not':
                arg2 = stack.pop()
                stack.append(f'({arg2} {operation} {arg1})')
            else:
                stack.append(f'({operation}{arg1})')
    elif t[i] == 'АЭМ':
        k = int(stack.pop())
        a = []
        while k != 0:
            a.append(stack.pop())
            k -= 1
        a.reverse()
        out_seq += a[0] + '[' + ']['.join(a[1:]) + ']'
    elif t[i] == 'Ф':
        k = int(stack.pop()) + 1
        a = []
        while k != 0:
            a.append(stack.pop())
            k -= 1
        a.reverse()
        out_seq += a[0] + '(' + ', '.join(a[1:]) + ');\n'
    i += 1

out_seq = re.sub(r'(М\d+): if \(!\((.*)\)\) goto (М\d+);(?:\n|\n((?:.|\n)+)\n)goto \1;\n\3: ', r'while \2 {\n\4\n}\n', out_seq)
out_seq = re.sub(r'if \(!\((.*)\)\) goto (М\d+);(?:\n|\n((?:.|\n)+)\n)goto (М\d+);\n\2: ((?:\n|.)+)\n?\4: ', r'if \1 {\n\3\n} else {\n\5\n}\n', out_seq)
out_seq = re.sub(r'if \(!\((.*)\)\) goto (М\d+);(?:\n|\n((?:.|\n)+)\n)\2: ', r'if \1 {\n\3\n}\n', out_seq)
out_seq = re.sub(r'alert\(([^\)]+)\);\nprompt\(([^\)]+)\);', r'\2 = prompt(\1);', out_seq)

c = 0
a = out_seq.split('\n')
for i in range(len(a)):
    if len(a[i]) == 0:
        continue
    if a[i][0] == '}':
        c -= 1
    a[i] = 4*c*' ' + a[i]
    if a[i][len(a[i]) - 1] == '{':
        c += 1
out_seq = '\n'.join(a)
a = out_seq.split('\n')
a = [i for i in a if len(i.strip()) > 0]
out_seq = '\n'.join(a)
while re.search(r'= \(([^\)]+)\);\n', out_seq):
    out_seq = re.sub(r'= \(([^\)]+)\);\n', r'= \1;\n', out_seq)

# файл, содержащий текст на выходном языке программирования
f = open('java_script.txt', 'w')
f.write(out_seq)
f.close()
