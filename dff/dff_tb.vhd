library IEEE;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;

entity dff_tb is
end dff_tb;

architecture simulate of dff_tb is

   signal s_clk : std_logic;
   signal s_d : std_logic;
   signal s_q : std_logic;

constant clk_period : time := 10.0 ns;

begin

uut : entity work.dff
	Port map(
		clk => s_clk,
		d => s_d,
		q => s_q
	);

--Stimulus process
stimulus : process
	begin
		wait for 20.0 ns;
		s_clk <= '0';
		s_d <= '0';
		wait for 20.0 ns;
		--Code here
      s_d <= '1'; 
      wait for clk_period;
      s_d <= '0';

		wait;
	end process;

--Clock process definiton
clk_process : process
	begin
		s_clk <= '0';
		wait for clk_period/2;
		s_clk <= '1';
		wait for clk_period/2;
	end process;

end;
