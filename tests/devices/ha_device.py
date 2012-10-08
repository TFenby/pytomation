import time
from unittest import TestCase, main
from mock import Mock
from datetime import datetime

from pytomation.devices import HADevice

class HADevice_Tests(TestCase):
    
    def setUp(self):
        self.interface = Mock()
        self.device = HADevice(interface=self.interface, address='D1')
        
    def test_instantiation(self):
        self.assertIsNotNone(self.device,
                             'HADevice could not be instantiated')

    def test_on(self):
        self.assertEqual(self.device.state, self.device.UNKNOWN)
        self.device.on()
        self.assertEqual(self.device.state, self.device.ON)
        self.interface.on.called_with('D1')
        
    def test_on_off(self):
        callback_obj = Mock()
        self.device.on_off(callback_obj.callback)
        self.device.off()
        self.assertTrue(callback_obj.callback.called)
        callback_obj.callback.assert_called_once_with(state=self.device.OFF, previous_state=self.device.UNKNOWN, source=self.device)
        
    def test_time_on(self):
        now = datetime.now()
        hours, mins, secs = now.timetuple()[3:6]
        secs = (secs + 2) % 60
        mins += (secs + 2) / 60
        trigger_time = '{h}:{m}:{s}'.format(
                                             h=hours,
                                             m=mins,
                                             s=secs,
                                                 )
        self.device.time_on(trigger_time)
        time.sleep(3)
        self.assertTrue( self.interface.on.called)

if __name__ == '__main__':
    main() 