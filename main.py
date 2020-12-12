from judger import device
import typing
import re

# The band & width & height of the net
scale, scale_x, scale_y = 2, 3, 4
connect_matrix = [[0, 2, 1, 3, 4, 6, 5, 7], [0, 4, 2, 6, 1, 5, 3, 7], [0, 4, 1, 5, 2, 6, 3, 7]]
network = device.Network()

def network_init():
    for i in range(0, scale_x):
        group = device.Group()
        for j in range(0, scale_y):
            switch = device.Switch(i*scale_y+j, connect_matrix[i][j*2], connect_matrix[i][j*2+1], scale)
            group.add_switch(switch) 
        network.add_group(group)

def input_args():
    pattern = input("Input connection patterns like (0 7 6 4 2)(1 3)(5):\n")
    if pattern == "quit":
        exit(0)
    else:
        exchange = re.split(r"[)(]+", pattern)[1:-1]
        network_route(exchange)
        congestion_detector()
        # network.printer()

def network_route(exchange: typing.List[str]):
    for op in exchange:
        op_list = re.split(r" ", op)
        for index in range(0, len(op_list)):
            bin_id = bin(int(op_list[index]))[2:].zfill(scale_x)
            src_id = int(op_list[index-1])
            for trans_id in range(0, scale_x):
                cur_switch = network.groups[trans_id].switches[int(src_id/scale)]
                fan_out = int(bin_id[-(trans_id+1)])
                cur_switch.new_request(src_id%scale, fan_out)
                src_id = cur_switch.fan_out[fan_out]

def congestion_detector():
    network.clear()

if __name__ == "__main__":
    network_init()
    while True:
        input_args()