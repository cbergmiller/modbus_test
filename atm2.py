# -*- coding: utf-8 -*-
"""
Modbus test for S+S ATM2

Usage:
	atm2 <host> <slave_id>

"""

from docopt import docopt
from modbus_test import ModbusTest


class Test(ModbusTest):
	"""
	Modbus Test für S+S ATM2
	"""
	def __init__(self, host=None, slave_id=None):
		super(Test, self).__init__(
			register_addr=0,
			function_code=4,
			data_type='16bit_int',
			host=host,
			slave_id=slave_id
		)

	def print_value(self, value):
		print u'Temperatur: {}°C'.format(value*0.1)


if __name__ == '__main__':
	arguments = docopt(__doc__)
	test = Test(
		host=arguments['<host>'],
		slave_id=int(arguments['<slave_id>'])
	)
	test.run()
