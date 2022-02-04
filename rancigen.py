import random

# module [name] (x1, x2, ..., xn);
#   input x1, x2, ..., xk;
#   output xk_1, xk_2, ..., xn;
#   [gate] [name] ([out], [in1], [in2]);
# endmodule

# Name: constant
# Gates: random
# Nets: arbitrary, but valid
# *** A simulator is needed to act as the descriminator.
# 
# WHY NOT PURE RANDOM?

module_name = "test"
gates = ["and", "or", "nand", "nor", "xor", "xnor"]
input_num = 3
output_num = 2

filename = "circuit.v"

output_prob = 0.1
drop_prob = 0.4

input_prefix = "in"
output_prefix = "out"
net_prefix = "net"
gate_prefix = "g"

# In each iteration, pick two random nets, attach them with a gate, add the 
# output as a new net.
# Each net may be an output with probability `output_prob`.

netlist = []
inputs, outputs, wires = [], [], []
usedlist = []
drop_weights = []

lines_part1, lines_part2, lines_part3 = [], [], []

for i in range(input_num):
  netlist.append (f"{input_prefix}{i+1}")
  inputs.append (f"{input_prefix}{i+1}")
  drop_weights.append(1)
outputs_generated = 0

line = f"module {module_name} ("
for net in netlist:
  line += f"{net}, "
for i in range(output_num - 1):
  line += f"{output_prefix}{i+1}, "
  outputs.append (f"{output_prefix}{i+1}")
line += f"{output_prefix}{output_num});"
lines_part1.append (line)
outputs.append (f"{output_prefix}{output_num}")

line = f"  input {inputs[0]}"
for name in inputs[1:]:
  line += f", {name}"
line += ";"
lines_part1.append(line)

line = f"  output {outputs[0]}"
for name in outputs[1:]:
  line += f", {name}"
line += ";"
lines_part1.append(line)

###################################

gate_num = 1
net_num = 1
while outputs_generated < output_num:
  net1, net2 = random.choices(netlist, k=2)
  usedlist.append(net1)
  usedlist.append(net2)

  gate = random.choice(gates)
  net_name = ""
  if random.random() > output_prob:
    net_name = f"{net_prefix}{net_num}"
    netlist.append (net_name)
    wires.append (net_name)
    # IMPORTANT: The drop rate determines how dense / sparse the result is.
    for i in range(len(drop_weights)):
      drop_weights[i] += 1
    drop_weights.append(1)
  else:
    net_name = f"{output_prefix}{outputs_generated+1}"
    outputs_generated += 1
  lines_part2.append (f"  {gate} {gate_prefix}{gate_num} ({net_name}, {net1}, {net2});")
  net_num += 1
  gate_num += 1
  if random.random() < drop_prob:
    removed = False
    while removed == False:
      i = random.choices(range(len(netlist)), weights=drop_weights, k=1)[0]
      if netlist[i] in usedlist:
        netlist.remove(netlist[i])
        drop_weights.remove(drop_weights[i])
        removed = True
    # TODO: use all inputs, prune unused nets, variable drop probability

###################################

line = ""
for i in range (len(wires)):
  if i % 5 == 0:
    line += f"  wire {wires[i]}"
  else:
    line += f", {wires[i]}"
  if i % 5 == 4:
    line += ";"
    lines_part3.append(line)
    line = ""
if i % 5 != 4:
  line += ";"
  lines_part3.append(line)

lines_part2.append ("endmodule")    ####

out = open (filename, 'w')
for line in lines_part1:
  out.write(f"{line}\n")
out.write("\n")
for line in lines_part3:
  out.write (f"{line}\n")
out.write("\n")
for line in lines_part2:
  out.write(f"{line}\n")
out.close()