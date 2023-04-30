import lab2
import json
import re

CLASSES_OF_TOKENS = ['W', 'I', 'O', 'R', 'N', 'C']

def is_identifier(token):
    return ((token in inverse_tokens) and re.match(r'^I\d+$', inverse_tokens[token])) or re.match(r'^M\d+$', token) or token in ['String[]', 'args', 'System.out.println', 'System.out.print', 'int', 'double', 'boolean','float']

def is_constant(token):
    return ((token in inverse_tokens) and re.match(r'^C\d+$', inverse_tokens[token])) or ((token in inverse_tokens) and re.match(r'^N\d+$', inverse_tokens[token])) or token.isdigit() or token in ["in.nextInt()","division(num,i)"]

def is_operation(token):
    return (token in inverse_tokens) and re.match(r'^O\d+$', inverse_tokens[token])

# лексемы (код-значение)
tokens = {}

# файлы, содержащие все таблицы лексем
for token_class in CLASSES_OF_TOKENS:
    with open('%s.json' % token_class, 'r') as read_file:
        data = json.load(read_file)
        if token_class == 'C':
            for k in data.keys():
                data[k] = re.sub(r"'([^']*)'", r'"\1"', data[k])
        tokens.update(data)

# лексемы (значение-код)
inverse_tokens = {val: key for key, val in tokens.items()}

replace = {'in.nextInt()': 'cin >> ', 'System.out.println': 'cout << ', 'System.out.print': 'cout << ', 'int': 'int', 'double': 'double', '=': '=', '||': '||', '&&': '&&', '!=': '!=', '==': '==', '/': '/', '%': '%', '!': '!', '++': '+= 1'}

# файл, содержащий обратную польскую запись
f = open('reverse_polish_entry.txt', 'r')
inp_seq = f.read()
inp_seq = inp_seq.replace("public division a int b int a return b % ","")
inp_seq = inp_seq.replace("division num i == 0 2Ф 1Ф (","division(num,i) 0 ==")
inp_seq = inp_seq.replace("public static void 2 АЭМ String args ","String[] args НП ")
inp_seq = re.sub(r"(System\.out\.println\s+)(\w+)", r"\g<1>\g<2> 1 Ф", inp_seq)
inp_seq = inp_seq.replace("main "," КП ")
inp_seq = inp_seq.replace("int in . nextInt 0Ф","in.nextInt()")
inp_seq = inp_seq.replace("++","1 +=")
inp_seq = inp_seq.replace("import java . util . Scanner ","")
f.close()

t = re.findall(r'(?:\'[^\']*\')|(?:"[^"]*")|(?:[^ ]+)', inp_seq)

i = 0
stack = []
out_seq = ''
is_func = False
variable = {}
while i < len(t):
    if is_func == True and not(is_identifier(t[i])):
        out_seq += ' {\n'
        is_func = False
    if is_identifier(t[i]) or is_constant(t[i]):
        stack.append(replace[t[i]] if t[i] in replace else t[i])
    elif t[i] == 'НП':
        stack.pop()
        stack.pop()
        #arg1 = stack.pop()
        out_seq += 'void main ()'
        is_func = True
    elif t[i] == 'КП':
        out_seq += '}\n'
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
        if t[i] == '=' and len(stack) == 2:
            arg1 = stack.pop()
            arg2 = stack.pop()
            out_seq += f'{arg2} = {arg1};\n'
        elif t[i] == '=' and len(stack) >= 3:
            arg1 = stack.pop()
            arg0 = stack.pop()
            arg2 = stack.pop()
            out_seq += f'{arg0} {arg2} = {arg1};\n'
        elif t[i] in ['+=', '-=', '*=', '/=', '++']:
            op = t[i][0]
            arg1 = stack.pop()
            arg2 = stack.pop()
            out_seq += f'{arg2} {op}= {arg1};\n'
        else:
            operation = replace[t[i]] if t[i] in replace else t[i]
            arg1 = stack.pop()
            if t[i] != '!':
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
    elif t[i] in ['break','continue']:
        stack.append(replace[t[i]] if t[i] in replace else t[i])
        arg0 = stack.pop();
        out_seq += f'\t{arg0};\n'
    elif t[i] == 'Ф':
        k = int(stack.pop()) + 1
        a = []
        while k != 0:
            a.append(stack.pop())
            k -= 1
        a.reverse()
        if a[0] == 'cin >>':
            b = []
            out_seq += a[0] + '("' + ' '.join(b) + '", ' + ', '.join(map(lambda x: '&' + x, a[1:])) + ');\n'
        else:
            out_seq += a[0] + ', '.join(a[1:]) + ';\n'
    i += 1

#while
#out_seq = re.sub(r'(М\d+): if \(!\((.*)\)\) goto (М\d+);(?:\n|\n((?:.|\n)+)\n)goto \1;\n\3: ', r'while \2 {\n\4\n}\n', out_seq)
out_seq = re.sub(r'(M\d+): if \(!\((.*)\)\) goto (M\d+);(?:\n|\n((?:.|\n)+)\n)goto \1;\n\3: ', r'while \2 {\n\4\n}\n', out_seq)

# if else
out_seq = re.sub(r'if\s*\((.*)\s*<\s*(.*)\)\s*{\s*(.*?)\s*}\s*else\s*{\s*(.*?)\s*}\s*', r'if (\1 < \2)\n{\n\3\n}\nelse\n{\n\4\n}\n', out_seq)

#if
out_seq = re.sub(r"if\s*\(\s*!\s*\(\s*(.*)\s*\)\s*\)\s*goto\s+(M\d+)\s*;\s*(\n(?:.|\n)+?)\s*\2:\s*", r"if \1 {\3\n}\n", out_seq)

out_seq = 'int division(int a, int b){\nreturn a % b;\n}\n\n' + out_seq
out_seq = 'using namespace std;\n\n' + out_seq


out_seq = re.sub(r"goto M(\d);", r"else {", out_seq)
out_seq = re.sub(r"M(\d): ", r"", out_seq)

def indent_cpp_code(code):
    indented_code = ""
    indentation = 0
    for line in code.split("\n"):
        if "{" in line:
            indented_code += ("\t" * indentation) + line + "\n"
            indentation += 1
        elif "}" in line:
            indentation -= 1
            indented_code += ("\t" * indentation) + line + "\n"
        else:
            indented_code += ("\t" * indentation) + line + "\n"
    return indented_code

out_seq = indent_cpp_code(out_seq)
out_seq = out_seq.replace("+= 1","++")

#out_seq = out_seq + "}\n";

stack.clear()

# файл, содержащий текст на выходном языке программирования
f = open('c++.txt', 'w')
f.write(out_seq)
f.close()
