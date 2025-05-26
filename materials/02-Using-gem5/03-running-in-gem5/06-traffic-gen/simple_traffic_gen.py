import m5
from m5.objects import *
from gem5.resources.resource import obtain_resource
#from m5.isas import ISA

system = System()

# Clock and voltage domains
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Memory mode and range
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('2GB')]

# System bus
system.membus = SystemXBar()

# Traffic Generator (linear)
system.trafficgen = TrafficGen(config_file="linear_traffic.txt")
system.trafficgen.port = system.membus.cpu_side_ports
print("TrafficGen config file:", system.trafficgen.config_file)

# Memory controller (LPDDR5)
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = LPDDR5_6400_1x16_BG_BL32()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

#system.mem_ctrl = SimpleMemory()
#system.mem_ctrl.range = system.mem_ranges[0]
#system.mem_ctrl.port = system.membus.mem_side_ports

#from gem5.components.processors.simple_processor import SimpleProcessor
#from gem5.components.processors.cpu_types import CPUTypes

#system.processor = SimpleProcessor(cpu_type=CPUTypes.TIMING, # Or ATOMIC, O3, MINOR
                          #        isa=ISA.ARM,
                         #         num_cores=1) # Single core example


#system.processor.connect_icache(system.membus)
#system.processor.connect_dcache(system.membus)
#system.processor.connect_walker_ports(system.membus)

system.traffic_gen1 = TrafficGen()
system.traffic_gen1.config_file = "/home/azureuser/gem5_workspace/gem5_release_23.0/test/traffic_generator/traffic_gen.cfg" # Needs its own config file
# Connect its master port to the memory bus
system.traffic_gen1.port = system.membus.cpu_side_ports
# Root and instantiation
from m5.objects import Root
root = Root(full_system=False, system=system)
import m5
m5.instantiate()

# Run simulation
max_ticks = int(10e9)
exit_event = m5.simulate(max_ticks)
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}.")
