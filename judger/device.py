from typing import List
import string


class Switch(object):
    def __init__(self, order: int, up_out: int, down_out: int, scale: int) -> None:
        super().__init__()
        self.order = order
        self.fan_out: List[int] = [up_out, down_out]
        self.fan_in: List[List[int]] = [[] for i in range(0, scale)] 
        self.fan_emitter: List[List[int]] = [[] for i in range(0, scale)]

    def new_request(self, src: int, dst: int):
        # 0 for upper pin, 1 for lower pin
        self.fan_in[dst].append(src)
        self.fan_emitter[src].append(dst)

    def clear(self):
        for fan_id in range(0, len(self.fan_in)):
            fan_set = set(self.fan_in[fan_id])
            if len(fan_set) > 1:
                print("Switch output congestion: ", string.ascii_uppercase[self.order], fan_id)
            self.fan_in[fan_id].clear()
        
        for fan_id in range(0, len(self.fan_emitter)):
            fan_set = set(self.fan_emitter[fan_id])
            if len(fan_set) > 1:
                print("Switch input congestion: ", string.ascii_uppercase[self.order], fan_id)
            self.fan_emitter[fan_id].clear()
    
    def printer(self):
        print(string.ascii_uppercase[self.order], self.fan_in)


class Group(object):
    def __init__(self) -> None:
        super().__init__()
        self.switches: List[Switch] = []
    
    def add_switch(self, switch: Switch):
        self.switches.append(switch)

    def clear(self):
        for switch in self.switches:
            switch.clear()

    def printer(self):
        for switch in self.switches:
            switch.printer()


class Network(object):
    def __init__(self) -> None:
        super().__init__()
        self.groups: List[Group] = []
    
    def add_group(self, group: Group):
        self.groups.append(group)

    def clear(self):
        for group in self.groups:
            group.clear()

    def printer(self):
        for group in self.groups:
            group.printer()
