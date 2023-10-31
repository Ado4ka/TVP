import os

class TuringMachine:
    def __init__(self, program_file, tape_file, alphabet_file, output_file):
        self.program = self.read_program(program_file)
        self.alphabet = self.read_alphabet(alphabet_file)
        self.current_state = 'q1'
        self.head_position = 0
        self.tape = self.read_tape(tape_file)
        self.output_file = output_file

    def read_program(self, file_name):
        program = {}
        with open(file_name, 'r') as file:
            for line in file:
            	# игнорировать пустые строки
                if line.strip():
                    values = line.strip().split()
                    if len(values) == 6:
                        state, symbol, temp, next_state, write_symbol, direction = values
                        program[(state, symbol)] = (next_state, write_symbol, direction)

        return program

    def read_alphabet(self, file_name):
        with open(file_name, 'r') as file:
            alphabet = file.read().strip().split()
        return alphabet

    def read_tape(self, file_name):
        with open(file_name, 'r') as file:
            tape = file.read().strip()
        
        # Проверка, что лента состоит только из символов алфавита
        for symbol in tape:
            if symbol not in self.alphabet:
                raise ValueError(f"Symbol '{symbol}' is not defined in the alphabet.")
        
        return list(tape)

    def run(self):
        with open(self.output_file, 'w') as file:
            file.write("Steps:\n")
            while True:
                current_key = (self.current_state, self.tape[self.head_position])
                if current_key not in self.program:
                    break
                next_state, write_symbol, direction = self.program[current_key]
                # записать текущее состояние
                # преобразовать ленту в строку
                tape_display = ''.join(self.tape)
                file.write(f"State: {self.current_state}\tTape: {tape_display}\n")
                file.write(" " * (len(self.current_state) + 20))
                file.write(" " * self.head_position + "^\n")
                # обновить символ на ленте
                self.tape[self.head_position] = write_symbol
                # определить направление головки
                if direction == 'R':
                    self.head_position += 1
                    # расширить ленту вправо для перемещения головки вправо
                    if self.head_position >= len(self.tape):
                        self.tape.append('_')
                elif direction == 'L':
                    self.head_position -= 1
                    # расширить ленту влево для перемещения головки влево
                    if self.head_position < 0:
                        self.tape.insert(0, '_')
                        self.head_position = 0
                # обновить состояние
                self.current_state = next_state

    def get_tape(self):
        return ''.join(self.tape)


# Проверка существования файлов и чтение алфавита
program_file = 'program.txt'
tape_file = 'tape.txt'
alphabet_file = 'alphabet.txt'
output_file = 'output.txt'

if not os.path.exists(program_file):
    raise FileNotFoundError(f"Program file '{program_file}' does not exist.")
if not os.path.exists(tape_file):
    raise FileNotFoundError(f"Tape file '{tape_file}' does not exist.")
if not os.path.exists(alphabet_file):
    raise FileNotFoundError(f"Alphabet file '{alphabet_file}' does not exist.")

# Создание экземпляра машины Тьюринга и выполнение программы
try:
    tm = TuringMachine(program_file, tape_file, alphabet_file, output_file)
    tm.run()
    print("Final tape content:", tm.get_tape())
except Exception as e:
    print("Error occurred:", str(e))

