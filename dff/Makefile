TOPLEVEL_LANG ?= vhdl
VHDL_SOURCES = $(shell pwd)/dff.vhd

SIM ?= ghdl
MODULE = test_dff
TOPLEVEL = dff

WAVES = 1

## save waveforms for ghdl (WAVES=1 doesn't work for ghdl)
ifeq ($(SIM),ghdl)
  SIM_ARGS += --vcd=${TOPLEVEL}.vcd
endif


include $(shell cocotb-config --makefiles)/Makefile.sim

clean::
	rm -rf modelsim.ini transcript __pycache__ results.xml *.wlf sim_build *.vcd

