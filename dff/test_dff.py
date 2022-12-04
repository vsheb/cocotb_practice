import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge

@cocotb.test()
async def test_dff(dut):
    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())  # Start the clock

    dut.d.value = 0  
    await FallingEdge(dut.clk)  # Synchronize with the clock
    dut.d.value = 1  
    await FallingEdge(dut.clk)
    assert dut.q.value == 1, f"output q was incorrect on the {i}th cycle"

