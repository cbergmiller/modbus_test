# -*- coding: utf-8 -*-
"""
Modbus test for CS Instruments VA520

Usage:
	va520 <host> <slave_id>

"""

from docopt import docopt
from modbus_test import ModbusTest


class Test(ModbusTest):
	"""
	Modbus Test für Thermokon AGS54
	"""
	def __init__(self, host=None, slave_id=None):
		super(Test, self).__init__(
			register_addr=1418,
			function_code=3,
			data_type='32bit_float',
			host=host,
			slave_id=slave_id
		)

	def print_value(self, value):
		print u'Temperatur: {:.2f}°C'.format(value)


if __name__ == '__main__':
	arguments = docopt(__doc__)
	test = Test(
		host=arguments['<host>'],
		slave_id=int(arguments['<slave_id>'])
	)
	test.run()
