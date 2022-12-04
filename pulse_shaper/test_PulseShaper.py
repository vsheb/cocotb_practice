import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge
from cocotb.triggers import RisingEdge, Timer, First, Event
from cocotb.decorators import coroutine
from cocotb.utils import get_sim_time


@coroutine
async def TimerClk(clk, cnt):
  for _ in range(cnt):
    await RisingEdge(clk)

@coroutine
async def waitClockedCond(clk, cond):
    i = 0
    while(True):
        await RisingEdge(clk)
        i = i + 1
        if cond():
            break
    return i

@coroutine
async def CountClockCycles(clk):
  global clk_cnt
  while (True):
    await RisingEdge(clk)
    clk_cnt += 1

@coroutine
async def set_input(dut, din_length):
  dut.din.value = 1
  await TimerClk(dut.clk, din_length)
  dut.din.value = 0


@coroutine
async def test_single_pulse(dut, din_length, signal_length, signal_delay):

  dut.len.value = signal_length 
  dut.dly.value = signal_delay

  await TimerClk(dut.clk, 10)

  din_length = 2

  await RisingEdge(dut.clk)
  input_task = cocotb.start_soon(set_input(dut, din_length))
  dut._log.debug('input 1 at')
  clock_cnt_in = clk_cnt + 1

  dut.din.value = 0

  # wait until output goes high
  await waitClockedCond(dut.clk, lambda : dut.dou.value == 1)
  clock_cnt_out = clk_cnt
  dut._log.debug('output signal detected')

  # wait until output goes low
  await waitClockedCond(dut.clk, lambda : dut.dou.value == 0)
  clock_cnt_stop = clk_cnt


  out_signal_length  = clock_cnt_stop - clock_cnt_out
  out_signal_delay   = clock_cnt_out  - clock_cnt_in

  await TimerClk(dut.clk, 10)

  dut._log.info(f'*** actual delay : {out_signal_delay}, actual length : {out_signal_length}')

  assert out_signal_delay == signal_delay, f"delay mismatch {out_signal_delay} != {signal_delay}"
  assert out_signal_length == signal_length, f"length mismatch {out_signal_length} != {signal_length}"

@cocotb.test()
async def test_pulse_shaper(dut):
  """ test pulse shaper"""

  clock = Clock(dut.clk, 10, units="ns")  # Create a 10us period clock on port clk
  cocotb.start_soon(CountClockCycles(dut.clk))
  cocotb.start_soon(clock.start())  # Start the clock

  dut.rst.value = 0
  dut.din.value = 0

  global clk_cnt 
  clk_cnt = 0

  for i in range(100):
    length = random.randint(1,10)
    delay  = random.randint(1,100)
    din_length = random.randint(0,100)

    test = cocotb.start_soon(test_single_pulse(dut, din_length, length, delay))
    print("running test",i,"input length =", din_length, "length =", length, "delay =", delay)
    
    await test

