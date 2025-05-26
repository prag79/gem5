#from m5.objects import System, SrcClockDomain, VoltageDomain, AddrRange, SystemXBar
#from m5.objects import TimingSimpleCPU, TrafficGen
#from m5.objects.DDR4_2400_8x8 import DDR4_2400_8x8
#from m5.objects import Process
import m5
from m5.objects import *
from m5.objects import Cache
from gem5.simulate.simulator import Simulator
from gem5.resources.resource import obtain_resource
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
#from gem5 import AddrRange

system = System()

# Set up clock and voltage domains
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Set up memory mode and range
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange(start=0x80000000, size="1GB"),AddrRange(start=0xC0000000, size= "1GB")]  # Example ranges

# Create a system crossbar (bus)
system.membus = SystemXBar()
#system.membus.max_routing_table_size = 4096 # Default is 512, try 1024 or higher


# Create the SimpleProcessor
# This encapsulates the CPU core(s)
#processor= SimpleProcessor(cpu_type=CPUTypes.TIMING, isa=ISA.ARM, num_cores=1)
#processor.connect_to_mem_bus(system.membus)

#system.cpu_cluster = processor
# Connect the SimpleProcessor's memory ports to the membus's CPU-side ports
#system.cpu.connect_memory_ports(system.membus.cpu_side_ports)
#system.cpu.connect_mem_side(system.membus)
# Create a CPU
system.cpu = ArmTimingSimpleCPU()

# Create a Traffic Generator (linear and random)
system.trafficgen = TrafficGen()
system.trafficgen.config_file = "traffic_gen4.cfg"

# Connect CPU and TrafficGen to the bus
#system.cpu.icache_port = system.membus.cpu_side_ports
#system.cpu.dcache_port = system.membus.cpu_side_ports
#for cpu_core_simobj in processor.cores:
 #   cpu_core_simobj.icache.cpu_side = system.membus.cpu_side_ports
  #  cpu_core_simobj.dcache.cpu_side = system.membus.cpu_side_ports
    # Walker ports for TLBs (TimingSimpleCPU/AtomicSimpleCPU have these)
 #   cpu_core_simobj.itb.walker.port = system.membus.cpu_side_ports
#    cpu_core_simobj.dtb.walker.port = system.membus.cpu_side_ports

system.trafficgen.port = system.membus.cpu_side_ports

system.l2cache = Cache(size="1MB", assoc=8,tag_latency=10,
    data_latency=10,
    response_latency=10,
    mshrs=64,
    tgts_per_mshr=20)


system.cpu.createInterruptController()

system.l2bus = SystemXBar()
#system.l2bus.max_routing_table_size = 4096
system.l2cache.cpu_side = system.membus.mem_side_ports
system.l2cache.mem_side = system.l2bus.cpu_side_ports


# Set up memory controller (LPDDR5) and connect to bus
system.mem_ctrl1 = MemCtrl()
system.mem_ctrl1.dram = LPDDR5_5500_1x16_BG_BL32()
system.mem_ctrl1.dram.range = system.mem_ranges[0]
system.mem_ctrl1.port = system.l2bus.mem_side_ports

system.mem_ctrl2 = MemCtrl()
system.mem_ctrl2.dram = LPDDR5_5500_1x16_BG_BL32()
system.mem_ctrl2.dram.range = system.mem_ranges[1]
system.mem_ctrl2.port = system.l2bus.mem_side_ports

binary_resource = obtain_resource("arm-hello64-static")
binary_path = binary_resource.get_local_path()
print("ARM binary path:", binary_path)

# Set up the SE binary workload on the SimpleProcessor
#system.cpu.set_se_binary_workload(binary_resource)
# Set up a simple process for the CPU (if using SE mode)

system.workload = SEWorkload.init_compatible(binary_path)
#system.process = Process(pid=100)
#system.process.executable = binary_path
#system.process.cmd = [binary_path]
process.cmd = [binary_path]
system.cpu.workload = process
system.cpu.createThreads()

#for cpu in system.cpu_cluster.cpus:
 #   cpu.workload = system.process
  #  cpu.createThreads()

   # cpu.createInterruptController()
# Set up the root object and instantiate
#system.cpu.set_se_binary_workload(binary_resource)
#system.cpu.connect_mem_side(system.membus)
from m5.objects import Root
root = Root(full_system=False, system=system)
import m5
m5.instantiate()


#simulator = Simulator(board=system)
# Example: configure the traffic generator to generate linear traffic

# Run the simulation using the classic m5 API for 10 ms
#max_ticks = int(10e9)  # 10 milli seconds
exit_event = m5.simulate(200*1000*1000)
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}.")
m5.stats.dump()
# Run the simulation
#simulator = Simulator(root)
#simulator.run(200*1000*1000)  # Run for 200 million ticks (200 ms)
