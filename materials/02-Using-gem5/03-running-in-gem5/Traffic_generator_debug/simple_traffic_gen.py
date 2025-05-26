from m5.objects import *

system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('1MB')]

system.membus = SystemXBar()

# Instantiate TrafficGen with a config file
system.trafficgen = TrafficGen(config_file="linear_traffic.txt")
system.trafficgen.port = system.membus.cpu_side_ports

# Use SimpleMemory for simplicity
system.mem_ctrl = SimpleMemory()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

from m5.objects import Root
root = Root(full_system=False, system=system)
import m5
m5.instantiate()
exit_event = m5.simulate(int(10e9))  # Simulate for 10ms
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}.")
