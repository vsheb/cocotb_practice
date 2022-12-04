# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0

PWD=$(shell pwd)

TOPLEVEL_LANG ?= vhdl

VHDL_SOURCES = $(PWD)/mem.vhd 

SIM = ghdl
COCOTB_ANSI_OUTPUT = 1
WAVES = 1

MODULE = test_fifo 
TOPLEVEL = fifo_cc 

include $(shell cocotb-config --makefiles)/Makefile.sim

clean::
	  rm -rf modelsim.ini transcript __pycache__ results.xml vsim.wlf 

