from nmigen import *
from nmigen_boards.icebreaker import *

class FSMBlinker(Elaboratable):
    def __init__(self, maxperiod):
        self.maxperiod = maxperiod
    
    def elaborate(self, platform):
        clk12 = platform.request("clk12")
        leds = [
            platform.request("led_g", 1),
            platform.request("led_g", 2),
            platform.request("led_g", 3),
            platform.request("led_g", 4),
            platform.request("led_r", 1),
        ]
        
        m = Module()
        m.domains.sync = ClockDomain()
        m.d.comb += ClockSignal().eq(clk12)

        counter = Signal(range(0, self.maxperiod + 1))

        with m.If(counter == 0):
            m.d.sync += counter.eq(self.maxperiod)
            with m.FSM() as fsm:
                with m.State("00000"):
                    m.next = "00001"
                    m.d.sync += [
                        leds[0].eq(0), leds[1].eq(0), leds[2].eq(0), leds[3].eq(0), leds[4].eq(0),
                    ]
                with m.State("00001"):
                    m.next = "00011"
                    m.d.sync += [
                        leds[0].eq(0), leds[1].eq(0), leds[2].eq(0), leds[3].eq(0), leds[4].eq(1),
                    ]
                with m.State("00011"):
                    m.next = "00111"
                    m.d.sync += [
                        leds[0].eq(0), leds[1].eq(0), leds[2].eq(0), leds[3].eq(1), leds[4].eq(1),
                    ]
                with m.State("00111"):
                    m.next = "01111"
                    m.d.sync += [
                        leds[0].eq(0), leds[1].eq(0), leds[2].eq(1), leds[3].eq(1), leds[4].eq(1),
                    ]
                with m.State("01111"):
                    m.next = "11111"
                    m.d.sync += [
                        leds[0].eq(0), leds[1].eq(1), leds[2].eq(1), leds[3].eq(1), leds[4].eq(1),
                    ]
                with m.State("11111"):
                    m.next = "11110"
                    m.d.sync += [
                        leds[0].eq(1), leds[1].eq(1), leds[2].eq(1), leds[3].eq(1), leds[4].eq(1),
                    ]
                with m.State("11110"):
                    m.next = "11100"
                    m.d.sync += [
                        leds[0].eq(1), leds[1].eq(1), leds[2].eq(1), leds[3].eq(1), leds[4].eq(0),
                    ]
                with m.State("11100"):
                    m.next = "11000"
                    m.d.sync += [
                        leds[0].eq(1), leds[1].eq(1), leds[2].eq(1), leds[3].eq(0), leds[4].eq(0),
                    ]
                with m.State("11000"):
                    m.next = "10000"
                    m.d.sync += [
                        leds[0].eq(1), leds[1].eq(1), leds[2].eq(0), leds[3].eq(0), leds[4].eq(0),
                    ]
                with m.State("10000"):
                    m.next = "00000"
                    m.d.sync += [
                        leds[0].eq(1), leds[1].eq(0), leds[2].eq(0), leds[3].eq(0), leds[4].eq(0),
                    ]
        with m.Else():
            m.d.sync += counter.eq(counter - 1)

        return m

plat = ICEBreakerPlatform()
plat.add_resources(plat.break_off_pmod)
plat.build(FSMBlinker(0x003FFFFF), do_program=True)
