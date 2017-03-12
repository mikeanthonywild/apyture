from apyture import Device, StateMachineMixin, LogParser, Uart


class RaspiParser(LogParser):
    def __init__(self):
        self.


class RasberryPi(StateMachineMixin, Device):
    DEFAULT_TIMEOUT = 30 # seconds
    UART_BAUD_RATE = 115700

    def __init__(self, mac_address, serial_port):
        super().__init__()
    
        self._uart = Uart(device=serial_port, baud_rate=self.UART_BAUD_RATE) 
        
        # Setup states
        self.add_state('IDLE', self._do_idle)

        # Callbacks
        self.register_callback('UBOOT_STARTED_KERNEL', self._kernel_started_cb)
        self.register_callback('BOOTED', self._booted_cb)

        # Flags
        self._kernel_started = Flag()
        self._booted = Flag()

    def _do_idle(self):
        self.cpu.start()

    def _execute_serial_cmd(self, cmd):
        self._uart.write(cmd)
        try:
            out = self._uart.read()
        except SerialTimeout:
            out = ''
        
        return out

    def kernel_started_cb(self):
        self._kernel_started.set()

    def booted_cb(self):
        self._booted.set()

    def reset(self):
        super().reset()
 
        if not self._kernel_started():
            self._execute_serial_cmd('reboot')
        else:
            self.wait_until_booted()
            self._execute_serial_cmd('sudo reboot')

    def wait_until_booted(self):
        self._booted.wait(timeout=DEFAULT_TIMEOUT)

    def wait_until_ip_address_assigned(self):
        self._ip_address_assigned.wait(timeout=DEFAULT_TIMEOUT)

    @property
    def ip_address(self):
        self.wait_until_ip_address_assigned(self):
        return self._ip_address


class ModelB(RaspberryPi):
    memory_size = CharField(default='1024 MB')


class PiZero(RaspberryPi):
    memory_size = CharField(default='512 MB')
    

@apyture.testutils.fixture
def dut():
    # Some logic to figure out which device to use
    dut = #....
    dut.start()
 
    yield dut

    dut.stop()

@apyture.testutils.fixture
def monitor():
    return SerialMonitor(parser=RaspiParser)

