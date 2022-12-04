#!/usr/bin/env python3
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge
from cocotb.triggers import RisingEdge, Timer, First, Event, Combine
from cocotb.decorators import coroutine

from cocotb_test.simulator import run
import pytest
import os

tests_dir = os.path.dirname(__file__)

################################################################
# Wait until condition
################################################################
@coroutine
async def waitClockedCond(clk, cond):
    while True:                       
        await RisingEdge(clk)          
        if cond():                     
            break                      
################################################################


################################################################
# write N samples to the FIFO
################################################################
@coroutine
async def writeStream(dut, samples = []):

  for smp in samples:
    await waitClockedCond(dut.clk, lambda : dut.full == 0)
    dut.din.value = smp
    dut.wen.value = 1
    print(f'write sample {smp}')

  await RisingEdge(dut.clk)
  dut.wen.value = 0
################################################################

################################################################
# FIFO read
################################################################
@coroutine
async def readStream(dut, n_expected):
  rd_samples = []
  n_read = 0
  while True : 
    await RisingEdge(dut.clk)

    if n_read == n_expected : 
      assert dut.empty.value == 1, "Already read out all samples but FIFO isn't empty"
      break
    
    if dut.ren.value == 1:
      n_read += 1
      dat = int(dut.dout.value)
      print('read value:',dat)
      rd_samples.append(dat)

    if dut.empty == 0:
      dut.ren.value = 1
    else:
      dut.ren.value = 0
  return rd_samples
################################################################


################################################################
################################################################
@coroutine
async def testSingle(dut):
  write_samples = [x for x in range(1000)]
  write_stream = cocotb.start_soon(writeStream(dut,write_samples)) 
  await Timer(100,'ns')
  # await write_stream
  read_stream  = cocotb.start_soon(readStream(dut, len(write_samples)))
  read_samples = await read_stream
  await write_stream

  assert write_samples == read_samples, "read != write"
  # await Combine(write_stream, read_stream)
################################################################

################################################################
# Perform tests
################################################################
@cocotb.test()
async def test_fifo(dut):
  """ test """

  clock = Clock(dut.clk, 10, units="ns")  # Create a 10us period clock on port clk
  cocotb.start_soon(clock.start())  # Start the clock

  dut.wen.value = 0
  dut.ren.value = 0
  dut.din.value = 0

  await RisingEdge(dut.clk)
  dut.rst.value = 1
  await RisingEdge(dut.clk)
  dut.rst.value = 0
  await RisingEdge(dut.clk)

  await testSingle(dut)
################################################################

def run_test_fifo():
  run(
      vhdl_sources  = [os.path.join(tests_dir, "mem.vhd")], 
      toplevel      = "fifo_cc",
      module        = "test_fifo",
      toplevel_lang = "vhdl",
      waves         = 1,
      force_compile = True )

if __name__ == "__main__":
  run_test_fifo()




