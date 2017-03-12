from apyture import RegexRule, ping

from raspi import dut, monitor


def test_boot_log(dut, monitor):
    monitor.add_rule(
        RegexRule(
            part='message',
            regex=r"^MEMORY (\d+ MB)$"
            validate=lambda m: m.groupdict['memory'] == dut.memory_size,
            required=True))

    # Reboot and check the boot logs
    monitor.start()
    dut.reset()

def test_responds_to_ping(dut):
    ping(dut.ip_address)
 
