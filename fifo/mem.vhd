------------------------------------------------------------------------
---- SIMPLE DUAL PORT BRAM WITH COMMON CLOCK ---------------------------
------------------------------------------------------------------------
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
 
entity bram_sdp_cc is
generic (
    DATA     : integer := 16;
    ADDR     : integer := 10
);
port (
    -- Port A
    clk   : in  std_logic;
    wea    : in  std_logic;
    addra  : in  std_logic_vector(ADDR-1 downto 0);
    dina   : in  std_logic_vector(DATA-1 downto 0);
    -- Port B
    addrb  : in  std_logic_vector(ADDR-1 downto 0);
    doutb  : out std_logic_vector(DATA-1 downto 0)
);
end bram_sdp_cc;
 
architecture read_first of bram_sdp_cc is
    -- Shared memory
    type mem_type is array ( (2**ADDR)-1 downto 0 ) of std_logic_vector(DATA-1 downto 0);
    signal mem : mem_type := (others => (others => '0'));
begin
 
  process(clk)
  begin
    if(clk'event and clk='1') then
        if(wea='1') then
            mem(to_integer(unsigned(addra))) <= dina;
        end if;
    end if;
  end process;
  doutb <= mem(to_integer(unsigned(addrb)));
 
end read_first;
------------------------------------------------------------------------


------------------------------------------------------------------------
---- FIFO with common clock
------------------------------------------------------------------------
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity fifo_cc is
generic(
   DATA_WIDTH : natural := 16;
   DEPTH : natural := 4 
);

port(
   clk   : in  std_logic;
   rst   : in  std_logic;
   din   : in  std_logic_vector(DATA_WIDTH-1 downto 0); 
   wen   : in  std_logic;
   ren   : in  std_logic;
   dout  : out std_logic_vector(DATA_WIDTH-1 downto 0);
   full  : out std_logic;
   empty : out std_logic
);
end fifo_cc;

architecture fifo_cc_arch of fifo_cc is
   
   signal i_full      : std_logic;
   signal i_empty     : std_logic;
   signal aempty      : std_logic;
                     
   signal waddr     : std_logic_vector(DEPTH-1 downto 0) := (others => '0');
   signal raddr     : std_logic_vector(DEPTH-1 downto 0) := (others => '0');
   signal cnt       : unsigned(DEPTH-1 downto 0) := (others => '0');

begin

   bram_i : entity work.bram_sdp_cc 
   generic map(
      DATA => DATA_WIDTH,
      ADDR => DEPTH
   )
   port map (
      clk   => clk,
      wea   => wen,
      addra => waddr,
      dina  => din,
      addrb => raddr,
      doutb => dout 
   );

   i_full   <= '1' when cnt = (cnt'range => '1')  else '0';
   i_empty  <= '1' when cnt = (cnt'range => '0') else '0';
   aempty   <= '1' when cnt = to_unsigned(1,DEPTH) else '0';

   full     <= i_full;

   empty    <= i_empty or (aempty and (not wen));
   ----


   ---- count number of words in FIFO
   FIFO_CNT_PROC : process(clk)
   begin
      if rising_edge(clk) then
         if rst = '1' then 
            cnt <= (others => '0');
         else
            if wen = '1' and ren = '0' and i_full = '0' then
               cnt <= cnt + 1;
            elsif wen = '0' and ren = '1' and i_empty = '0' then
               cnt <= cnt - 1;
            end if;
         end if;
      end if;
   end process FIFO_CNT_PROC;
   ----

   ---- manage read/write addresses for BRAM
   RW_ADDR_PROC : process(clk)
   begin
      if rising_edge(clk) then
         if rst = '1' then 
            waddr <= (others => '0');
            raddr <= (others => '0'); 
         else
            if (wen = '1' and i_full = '0') then
               if waddr = (waddr'range => '1') then
                  waddr <= (others => '0');
               else
                  waddr <= std_logic_vector(unsigned(waddr) + 1);
               end if;
            end if;

            if (ren = '1' and i_empty = '0') then
               if raddr = (raddr'range => '1') then
                  raddr <= (others => '0');
               else
                  raddr <= std_logic_vector(unsigned(raddr) + 1);
               end if;
            end if;

         end if;
      end if;
   end process RW_ADDR_PROC;
   ----

end fifo_cc_arch;
------------------------------------------------------------------------



