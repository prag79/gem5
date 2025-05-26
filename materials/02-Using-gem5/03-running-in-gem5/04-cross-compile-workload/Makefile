GEM5_PATH = /home/azureuser/gem5_workspace/googlesource/2024/gem5
ISA = arm64
GXX = aarch64-linux-gnu-g++


all: 04-cross-compile-this-static 04-cross-compile-this-dynamic

04-cross-compile-this-static: 04-cross-compile-this.cpp
# compile command with -static flag
	$(GXX) -o 04-cross-compile-this-static 04-cross-compile-this.cpp -I$(GEM5_PATH)/include -L$(GEM5_PATH)/util/m5/build/$(ISA)/out -lm5 -static
04-cross-compile-this-dynamic: 04-cross-compile-this.cpp
# compile command without -static flag
	$(GXX) -o 04-cross-compile-this-dynamic 04-cross-compile-this.cpp -I$(GEM5_PATH)/include -L$(GEM5_PATH)/util/m5/build/$(ISA)/out -lm5
clean:
	rm -f 04-cross-compile-this-static 04-cross-compile-this-dynamic

