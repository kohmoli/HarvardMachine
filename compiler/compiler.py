import re
import sys
import copy


class Compiler:
   variable_id = 0
   instant_variable_id = 0
   variables = {}
   instruction_length_list = []


   @staticmethod
   def error(message):
      print(message)
      sys.exit(-1)


   def assign_instant_variable_id(self):
      self.instant_variable_id = self.instant_variable_id + 1
      self.variables[f'{self.variable_id + self.instant_variable_id}'] = f'{self.variable_id + self.instant_variable_id}'
      return f'{self.variable_id + self.instant_variable_id}'


   def assign_variable(self, name):
      self.variable_id = self.variable_id + 1
      self.variables[name] = f'{self.variable_id}'
      return f'{self.variable_id}'


   def assemble_unary_operator(self, tokens, i):
      operetator, a = tokens.pop(i), tokens.pop(i)
      tokens.insert(i, self.assign_instant_variable_id())
      
      AM = 'IMM' if type(a) is int else 'ABS'
      a = a if type(a) is int else self.variables[a]

      if operetator == '+' :
         return [f'LOAD {AM} 0', f'STORE IMM {tokens[i]}']
      
      if operetator == '-' :
         return ['LOAD IMM 0', f'SUB {AM} {a}', f'STORE IMM {tokens[i]}']
      
      if operetator == '!' :
         return [f'LOAD {AM} {a}', 'NOT IMM 0', f'STORE IMM {tokens[i]}']


   def assemble_binary_operator(self, tokens, i):
      a, operetator, b = tokens.pop(i), tokens.pop(i), tokens.pop(i)
      tokens.insert(i-1, self.assign_instant_variable_id())

      AM1 = 'IMM' if type(a) is int else 'ABS'
      AM2 = 'IMM' if type(b) is int else 'ABS'
      a = a if type(a) is int else self.variables[a]
      b = b if type(b) is int else self.variables[b]

      if operetator == '+' :
         return [f'LOAD {AM1} {a}', f'ADD {AM2} {b}', f'STORE IMM {tokens[i]}']
      
      if operetator == '-' :
         return [f'LOAD {AM1} {a}', f'SUB {AM2} {b}', f'STORE IMM {tokens[i]}']
      
      if operetator == '*' :
         return [f'LOAD {AM1} {a}', f'MUL {AM2} {b}', f'STORE IMM {tokens[i]}']
      
      if operetator == '/' :
         return [f'LOAD {AM1} {a}', f'DIV {AM2} {b}', f'STORE IMM {tokens[i]}']
      
      if operetator == '%' :
         return [f'LOAD {AM1} {a}', f'MOD {AM2} {b}', f'STORE IMM {tokens[i]}']
      
      if operetator == '&' :
         return [f'LOAD {AM1} {a}', f'AND {AM2} {b}', f'STORE IMM {tokens[i]}']
      
      if operetator == '|' :
         return [f'LOAD {AM1} {a}', f'OR {AM2} {b}', f'STORE IMM {tokens[i]}']


   def assemble_expression(self, tokens):
      result = self.assemble_unary_operator(tokens, 0) if tokens[0] in ('+', '-') else []

      for i, token in enumerate(tokens):
         if token == '(' :
            tokens.pop(i)
            j = list(reversed(tokens)).index(')') + 1
            result = result + self.assemble_expression(tokens[i:-j])
            del tokens[i: -j]
            tokens[-j] = self.assign_instant_variable_id()
            result = result + [f'STORE IMM {tokens[i]}']
            print(tokens)
      
      for i, token in enumerate(tokens):
         if token == '!' :
            result = result + self.assemble_unary_operator(tokens, i)

      for i, token in enumerate(tokens):
         if token == '*' or token == '/' or token == '%':
            result = result + self.assemble_binary_operator(tokens, i-1)
         
      for i, token in enumerate(tokens):
         if token == '+' or token == '-' :
            result = result + self.assemble_binary_operator(tokens, i-1)
         
      for i, token in enumerate(tokens):
         if token == '&' or token == '|' :
            result = result + self.assemble_binary_operator(tokens, i-1)
      
      
      AM = 'IMM' if type(tokens[0]) is int else 'ABS'
      tokens[0] = tokens[0] if type(tokens[0]) is int else self.variables[tokens[0]]
      
      return result + [f'LOAD {AM} {tokens[0]}']


   def assemble_conditional_operator(self, tokens, pc=0):
      operetator, b = tokens[0], tokens[1]

      AM2 = 'IMM' if type(b) is int else 'ABS'
      b = b if type(b) is int else self.variables[b]

      if len(tokens) > 2 :
         if operetator == '==' or operetator == '!=' :
            PC1 = f'{pc + 4}' if tokens[2] == '&&' else '$start_of_clause'
            PC2 = f'{pc + 4}' if tokens[2] == '||' else '$end_of_clause'
         else:
            PC1 = f'{pc + 2}' if tokens[2] == '&&' else '$start_of_clause'
            PC2 = f'{pc + 2}' if tokens[2] == '||' else '$end_of_clause'

      if operetator == '==' :
         return [f'LT {AM2} {b}', f'BEQ IMM {PC2}', f'GT {AM2} {b}', f'BEQ IMM {PC2}']
      
      if operetator == '!=' :
         return [f'LT {AM2} {b}', f'BEQ IMM {PC1}', f'GT {AM2} {b}', f'BNE IMM {PC2}']
      
      if operetator == '<' :
         return [f'LT {AM2} {b}', f'BNE IMM {PC2}']
      
      if operetator == '>' :
         return [f'GT {AM2} {b}', f'BNE IMM {PC2}']
      
      if operetator == '<=' :
         return [f'GT {AM2} {b}', f'BEQ IMM {PC2}']
      
      if operetator == '>=' :
         return [f'LT {AM2} {b}', f'BEQ IMM {PC2}']


   def assemble_keyword(self, tokens):
      if tokens[0] == 'break' :
         return ['JUMP IMM $end_of_loop_clause']
      if tokens[0] == 'skip' :
         return ['JUMP IMM $start_of_loop_header']
      if tokens[0] == 'print' :
         return self.assemble_expression(tokens[1:]) + ['STORE IMM 0', 'PRINT ABS 2']
      if tokens[0] == 'sleep' :
         exp = self.assemble_expression(tokens[1:])
         return exp + ['GT IMM 0', f'BNE IMM {sum(self.instruction_length_list) + len(exp) + 4}',
            'SUB IMM 1', f'JUMP IMM {sum(self.instruction_length_list) + len(exp)}']
      if tokens[1] == '=' :
         if not tokens[0] in self.variables:
            self.assign_variable(tokens[0])
         return self.assemble_expression(tokens[2:]) + [f'STORE IMM {self.variables[tokens[0]]}']
      
      self.error('')


   def assemble_header(self, tokens):
      result = []
      a_list = []
      b_list = []

      for token in tokens:
         if token in ('==', '!=', '<', '>', '<=', '>='):
            a_list = copy.deepcopy(b_list)
            b_list = []
            operetator = token
         elif token in ('&&', '||'):
            b = self.assign_instant_variable_id()
            result = result + self.assemble_expression(b_list) + [f'STORE ABS {b}']
            result = result + self.assemble_expression(a_list)
            result = result + self.assemble_conditional_operator([operetator, b, token], sum(self.instruction_length_list) + len(result))
            a_list = []
            b_list = []
         else:
            b_list = b_list + [token]
      
      b = self.assign_instant_variable_id()
      result = result + self.assemble_expression(b_list) + [f'STORE ABS {b}']
      result = result + self.assemble_expression(a_list)
      result = result + self.assemble_conditional_operator([operetator, b, token])
      
      self.instant_variable_id = 0
      return result
   

   def assemble_clause(self, lines, header_indent):
      result = []
      self.instruction_length_list.append(0)

      for i in range(len(lines)):
         if len(lines[i]['tokens']) == 0:
            continue

         if lines[i]['indentlevel'] >= header_indent + 2:
            continue

         if lines[i]['indentlevel'] <= header_indent:
            break
         
         if lines[i]['tokens'][0] == 'while' :
            header = self.assemble_header(lines[i]['tokens'][1:-1])
            clause = self.assemble_clause(lines[i+1:], header_indent+1)

            for i, h in enumerate(header):
               if '$start_of_clause' in h:
                  header[i] = h.replace('$start_of_clause', f'{sum(self.instruction_length_list) + len(header)}')
               if '$end_of_clause' in h:
                  header[i] = h.replace('$end_of_clause', f'{sum(self.instruction_length_list) + len(header) + len(clause) + 1}')

            for i, c in enumerate(clause):
               if '$start_of_loop_header' in c:
                  clause[i] = c.replace('$start_of_loop_header', f'{sum(self.instruction_length_list)}')
               if 'end_of_loop_clause' in c:
                  clause[i] = c.replace('$end_of_loop_clause', f'{sum(self.instruction_length_list) + len(header) + len(clause) + 1}')
               
            result = result + header + clause + [f'JUMP IMM {sum(self.instruction_length_list)}']
         elif lines[i]['tokens'][0] == 'if' :
            header = self.assemble_header(lines[i]['tokens'][1:-1])
            clause = self.assemble_clause(lines[i+1:], header_indent+1)

            for i, h in enumerate(header):
               if '$start_of_clause' in h:
                  header[i] = h.replace('$start_of_clause', f'{sum(self.instruction_length_list) + len(header)}')
               if '$end_of_clause' in h:
                  header[i] = h.replace('$end_of_clause', f'{sum(self.instruction_length_list) + len(header) + len(clause)}')

            result = result + header + clause
         elif lines[i]['tokens'][0] == 'else' :
            clause = self.assemble_clause(lines[i+1:], header_indent+1)
            result = result + [f'JUMP IMM {sum(self.instruction_length_list) + len(clause) + 1}'] + clause
         else:
            result = result + self.assemble_keyword(lines[i]['tokens'])
         
         self.instruction_length_list[-1] = len(result)
         self.instant_variable_id = 0
      
      self.instruction_length_list.pop(-1)
      return result


   def assemble(self, lines):
      return self.assemble_clause(lines, -1) + ['EOP IMM 0']
   

   @staticmethod
   def decode(line):
      tokens = []

      indent = re.compile(r' *')
      space = re.compile(r' +')
      keyword = re.compile(r'(break)|(skip)|(print)|(sleep)|(if)|(else)|(while)')
      operetor = re.compile(r'\+|\*|\-|/|%|!|&|\||<|>|(<=)|(>=)|(==)|(!=)|(&&)|(\|\|)|\(|\)|:|=')
      variable = re.compile(r'([a-z]|[A-Z]|_)+')
      number = re.compile(r'[0-9]+')
      
      i = indent.match(line).end()
      indentlevel = i//3

      while i < len(line):
         token0 = space.match(line[i:])
         token1 = keyword.match(line[i:])
         token2 = operetor.match(line[i:])
         token3 = variable.match(line[i:])
         token4 = number.match(line[i:])

         if token0 != None:
            i += token0.end()
         elif token1 != None:
            i += token1.end()
            tokens.append(token1.group())
         elif token2 != None:
            i += token2.end()
            tokens.append(token2.group())
         elif token3 != None:
            i += token3.end()
            tokens.append(token3.group())
         elif token4 != None:
            i += token4.end()
            tokens.append(int(token4.group()))
         else:
            return Compiler.error('エラー: 不正な文字が含まれています')
      return {'indentlevel': indentlevel, 'tokens': tokens}
   

   @staticmethod
   def compile(instructions):
      for i in range(len(instructions)):
         instructions[i] = instructions[i].replace(' ', '')
         instructions[i] = instructions[i].replace('NOP'  , '00000')
         instructions[i] = instructions[i].replace('PRINT', '00001')
         instructions[i] = instructions[i].replace('LOAD' , '00010')
         instructions[i] = instructions[i].replace('STORE', '00011')
         instructions[i] = instructions[i].replace('EOP'  , '00100')
         instructions[i] = instructions[i].replace('LT'   , '01000')
         instructions[i] = instructions[i].replace('GT'   , '01001')
         instructions[i] = instructions[i].replace('JUMP' , '01100')
         instructions[i] = instructions[i].replace('BEQ'  , '01101')
         instructions[i] = instructions[i].replace('BNE'  , '01110')
         instructions[i] = instructions[i].replace('ADD'  , '10000')
         instructions[i] = instructions[i].replace('SUB'  , '10001')
         instructions[i] = instructions[i].replace('MUL'  , '10010')
         instructions[i] = instructions[i].replace('DIV'  , '10011')
         instructions[i] = instructions[i].replace('MOD'  , '10100')
         instructions[i] = instructions[i].replace('NOT'  , '10101')
         instructions[i] = instructions[i].replace('OR'   , '10110')
         instructions[i] = instructions[i].replace('AND'  , '10111')

         instructions[i] = instructions[i].replace('ABS'  , '0')
         instructions[i] = instructions[i].replace('IMM'  , '1')

         instructions[i] = instructions[i][:6] + format(int(instructions[i][6:]) & 0xffff, '016b')

      return instructions


if(len(sys.argv)<2):
   Compiler.error('エラー: アセンブルするファイル名が指定されていません')

with open(sys.argv[1], mode='r') as rf, open('./Instruction.v', mode='w') as wf:
   lines = rf.read().split('\n')
   for i in range(len(lines)):
      lines[i] = Compiler.decode(lines[i])
   
   instructions = Compiler.compile(Compiler().assemble(lines))

   for i in range(256):
      if i < len(instructions):
         instructions[i] = instructions[i]
      else:
         instructions.append('0000000000000000000000')


   wf.write('\n'.join(instructions))
