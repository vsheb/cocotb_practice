#!/usr/bin/env python3

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Join, ClockCycles
from cocotb.decorators import coroutine


from cocotb_test.simulator import run
import os


@coroutine                     
async def dff_driver(dut):     
  dut.d.value = 0            
  await RisingEdge(dut.clk)  
  for _ in range(100) :      
    dut.d.value = 1            
    await RisingEdge(dut.clk)
    dut.d.value = 0            
    await ClockCycles(dut.clk, 10)

@coroutine                              
async def dff_monitor(dut):             
  while True:                           
    await RisingEdge(dut.clk)           
    if int(dut.d.value) == 1 :                
      await RisingEdge(dut.clk)         
      assert int(dut.q.value) == 1, f"Error!"


@cocotb.test()
async def test_dff(dut):
  clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
  cocotb.start_soon(clock.start())  # Start the clock

# start clock                                 
  clk = Clock(dut.clk, 10, units="ns")          
  cocotb.start_soon(clk.start())  

# start monitoring
  mon = cocotb.start_soon(dff_monitor(dut))
# start driver
  drv = cocotb.start_soon(dff_driver(dut))      

  await Join(drv)                               



def run_test_dff():
  os.environ["SIM"] = "ghdl"

  run(
      vhdl_sources  = ['dff.vhd'],
      toplevel      = 'dff',
      module        = 'run_test_dff_coro',
      toplevel_lang = 'vhdl',
      sim_args      = ['--vcd=dff.vcd'],
      waves         = 1)
if __name__ == "__main__" :
  run_test_dff()
