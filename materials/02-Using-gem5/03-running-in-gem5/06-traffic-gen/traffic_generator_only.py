from m5.objects import *
from gem5.resources.resource import obtain_resource

system = System()

# Clock and voltage domains
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Memory mode and range
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('1024MB')]

# System bus
system.membus = SystemXBar()

# Traffic Generator (linear)
system.trafficgen = TrafficGen(config_file="/home/azureuser/gem5_workspace/googlesource/2024/materials/02-Using-gem5/03-running-in-gem5/06-traffic-gen/linear_traffic.txt")
system.trafficgen.port = system.membus.cpu_side_ports
print("TrafficGen config file:", system.trafficgen.config_file)

# Memory controller (LPDDR5)
#system.mem_ctrl = MemCtrl()
#system.mem_ctrl.dram = DDR4_2400_8x8()
#system.mem_ctrl.dram.range = system.mem_ranges[0]
#system.mem_ctrl.port = system.membus.mem_side_ports

system.mem_ctrl = SimpleMemory()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# Root and instantiation
from m5.objects import Root
root = Root(full_system=False, system=system)
import m5
m5.instantiate()

# Run simulation
max_ticks = int(10e9)
exit_event = m5.simulate(max_ticks)
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}.")
