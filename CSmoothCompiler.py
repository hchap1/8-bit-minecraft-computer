#COMMANDS
# 0000 ADD save to ADDR ------ ADD TO ADDR
# 0001 SUBTRACT save to ADDR - SUB TO ADDR
# 0100 JUMP to ADDR ---------- IF != JUMP TO ADDR
# 1000 LOAD ADDR to ALU 1 ---- LOAD ADDR TO 0
# 1001 LOAD ADDR to ALU 2 ---- LOAD ADDR TO 1
# 1010 READ FROM RAM @ ADDR -- READ ADDR
# 1011 WRITE TO RAM ---------- WRITE ADDR
# 1111 & ADDR 1111 = HALT ---- HALT

#INIT NUM TO NUM

import keyboard as k
from time import sleep

def int_to_bin(integer: int):
    binary = bin(integer)[2:]
    binary = "0" * (4 - len(binary)) + binary
    return binary

def eight_int_to_bin(integer: int):
    binary = bin(integer)[2:]
    binary = "0" * (8 - len(binary)) + binary
    return binary

def compile(program):
    inits = [None, None, None, None]
    binary = ""
    for command in program.split("\n"):
        action = command.split(" ")[0].lower()
        if action == "init": 
            data = (command.strip("init ")).split(" to ")
            num = int(data[0])
            target = int(data[1])
            inits[target] = num
        if action == "add": binary += int_to_bin(int(command.split(" ")[2])) + "0000\n"
        if action == "sub": binary += int_to_bin(int(command.split(" ")[2])) + "0001\n"
        if action == "if" and command.split(" ")[1].lower() == "!=": binary += int_to_bin(int(command.split(" ")[4])) + "0100\n"
        if action == "load": binary += int_to_bin(int(command.split(" ")[1])) + ("100%s\n" % command.split(" ")[3])
        if action == "halt": binary += "11111111\n"
        if action == "display": binary += int_to_bin(int(command.split(" ")[1])) + "1101\n"
    return [binary, inits]

program = []
filename = "%s" % input("FILENAME:\n> ")
with open(filename, "r") as program_file:
    temp = program_file.readlines()
    for line in temp:
        program.append(line.strip("\n"))
compiled_program, compiled_inits = compile("\n".join(program))
print(compiled_program)
with open("COMPILED_CODE.txt", "w") as program_file:
    program_file.write(compiled_program)
z_coord = 28
commands_list = []
for instruction in compiled_program.split("\n"):
    x_coord = 120
    for bitstate in instruction:
        if bitstate == "0":
            commands_list.append("/setblock %s 100 %s redstone_block" % (x_coord, z_coord))
        else:
            commands_list.append("/setblock %s 100 %s air" % (x_coord, z_coord))
        x_coord -= 2
    z_coord -= 4

while not k.is_pressed("f9"):
    sleep(0.1)

for com in range(4):
    #Start 100 111 96
    #End 100 111 61
    #Each row -4 x
    if compiled_inits[com] != None:
        bits = list(eight_int_to_bin(compiled_inits[com]))
        bits.reverse()
        x = 100 - (com * 3)
        y = 111
        z = 96
        for bit in bits:
            if str(bit) == "0":
                commands_list.append("/setblock %s %s %s redstone_block" % (x, y, z))
            else:
                commands_list.append("/setblock %s %s %s air" % (x, y, z))
            z -= 5

for command in commands_list:
    k.press_and_release("t")
    sleep(0.08)
    k.write(command)
    sleep(0.08)
    k.press_and_release("enter")
    sleep(0.08)