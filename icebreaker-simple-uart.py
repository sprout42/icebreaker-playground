from nmigen import Elaboratable, Module
from nmigen.build import Resource, Attrs, Pins, Subsignal
from nmigen_boards.icebreaker import ICEBreakerPlatform


class Top(Elaboratable):
    def __init__(self, pins, baud_rate=115200):
        self._pins = pins

    def elaborate(self, platform):
        # External IO pins
        ext_pins = platform.request(self._pins)

        # Host UART (USB CDC ACM) device
        uart_pins = platform.request('uart')

        m = Module()

        # Rx signals are input, have to read always from Rx and write to Tx.
        #   uart Rx ->  ext Tx
        #    ext Rx -> uart Tx
        m.d.comb += [
            ext_pins.tx.eq(uart_pins.rx),
            uart_pins.tx.eq(ext_pins.rx),
        ]

        return m


if __name__ == '__main__':
    plat = ICEBreakerPlatform()
    plat.add_resources(plat.break_off_pmod)

    # The external IO pins to use
    ext_io = [
        Resource('ext_io', 0,
            # External Input
            Subsignal('rx',
                Pins('4', dir='i', conn=('pmod', 0)),
                Attrs(IO_STANDARD="LVCMOS33", PULLUP=1)),
            # External Output
            Subsignal('tx',
                Pins('3', dir='o', conn=('pmod', 0)),
                Attrs(IO_STANDARD="LVCMOS33", PULLUP=1)),
        ),
    ]
    plat.add_resources(ext_io)

    plat.build(Top(pins='ext_io'), do_program=True)

