
import unittest
from SIM800L import Modem

# Mock execute_at_command function
def mock_execute_at_command(output):
    def execute_at_command(*argv,**kwargs):
        return output.decode('utf8')
    Modem.execute_at_command = execute_at_command


class test_command_functions(unittest.TestCase):

    def setUp(self):

        # Create a new modem (but do not initialize it, as there is no actual modem)
        self.modem = Modem(MODEM_PWKEY_PIN    = None,
                           MODEM_RST_PIN      = None,
                           MODEM_POWER_ON_PIN = None,
                           MODEM_TX_PIN       = None,
                           MODEM_RX_PIN       = None)

    def test_network_scan(self):

        # Mock the AT command response
        mocked_at_output = b'+COPS: (2,"vodafone","voda IT","22210"),(3,"TELECOM ITALIA MOBILE","TIM","22201"),(3,"Wind Telecom SpA","I WIND","22288"),,(0-4),(0-2)'
        mock_execute_at_command(mocked_at_output)

        # Get networks and compare
        networks = self.modem.scan_networks()
        self.assertEqual(networks, [{'id': '22210', 'name': 'vodafone', 'shortname': 'voda IT'}, {'id': '22201', 'name': 'TELECOM ITALIA MOBILE', 'shortname': 'TIM'}, {'id': '22288', 'name': 'Wind Telecom SpA', 'shortname': 'I WIND'}])

    def test_get_ip_addr(self):

        mocked_at_output = b'+SAPBR: 1,3,"0.0.0.0"'
        mock_execute_at_command(mocked_at_output)
        ip_addr = self.modem.get_ip_addr()
        self.assertEqual(ip_addr, None)

        mocked_at_output = b'+SAPBR: 1,3,"1.2.3.45"'
        mock_execute_at_command(mocked_at_output)
        ip_addr = self.modem.get_ip_addr()
        self.assertEqual(ip_addr, '1.2.3.45')

        # Edge case when a \r\n gets missing
        mocked_at_output = b'+HTTPACTION: 1,200,94+SAPBR: 1,1,"1.2.3.45"'
        mock_execute_at_command(mocked_at_output)
        ip_addr = self.modem.get_ip_addr()
        self.assertEqual(ip_addr, '1.2.3.45')
