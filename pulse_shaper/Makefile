# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0

TOPLEVEL_LANG ?= vhdl

VHDL_SOURCES = $(shell pwd)/PulseShaper.vhd

SIM = ghdl
COCOTB_ANSI_OUTPUT = 1
WAVES = 1
SIM_ARGS ?= --vcd=waveform.vcd

MODULE = test_PulseShaper 
TOPLEVEL = pulseshaper 

include $(shell cocotb-config --makefiles)/Makefile.sim

clean::
	rm -rf modelsim.ini transcript __pycache__ results.xml vsim.wlf

