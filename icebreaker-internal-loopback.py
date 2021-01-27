from nmigen import Elaboratable, Module
from nmigen_boards.icebreaker import ICEBreakerPlatform


class Top(Elaboratable):
    def elaborate(self, platform):
        clk_freq = platform.default_clk_frequency
        uart_pins = platform.request('uart')

        m = Module()

        # Ok, this is pretty simple, I was trying to overcomplicate this for 
        # ages
        m.d.comb += [
            uart_pins.tx.o.eq(uart_pins.rx.i),
        ]

        return m


if __name__ == '__main__':
    plat = ICEBreakerPlatform()
    plat.add_resources(plat.break_off_pmod)
    plat.build(Top(), do_program=True)

