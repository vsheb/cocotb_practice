#!/usr/bin/env python3

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge

from cocotb_test.simulator import run
import os


@cocotb.test()
async def test_dff(dut):
    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())  # Start the clock

    dut.d.value = 0  
    await FallingEdge(dut.clk)  # Synchronize with the clock
    dut.d.value = 1  
    await FallingEdge(dut.clk)
    assert dut.q.value == 1, f"output q was incorrect on the {i}th cycle"


def run_test_dff():
  os.environ["SIM"] = "ghdl"

  run(
      vhdl_sources  = ['dff.vhd'],
      toplevel      = 'dff',
      module        = 'run_test_dff',
      toplevel_lang = 'vhdl',
      sim_args      = ['--vcd=dff.vcd'],
      waves         = 1)
if __name__ == "__main__" :
  run_test_dff()
