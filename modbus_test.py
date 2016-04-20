# -*- coding: utf-8 -*-
import time
import logging
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.pdu import ExceptionResponse
#from pymodbus.exceptions import


_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s - %(message)s")
ch.setFormatter(formatter)
_logger.addHandler(ch)

COUNTS = {
	'16bit_int': 1,
	'16bit_uint': 1,
	'32bit_int': 2,
	'32bit_uint': 2,
	'32bit_float': 2,
	'64bit_float': 4,
}

class ModbusTest(object):
	"""
	Modbus Test Basisklasse
	"""
	def __init__(self, host=None, slave_id=1, function_code=None, register_addr=None, data_type=None, endian='big'):
		self.client = None
		self.host = host
		self.slave_id = slave_id
		self.function_code = function_code
		self.register_addr = register_addr
		self.data_type = data_type
		if endian == 'big':
			self.endian = Endian.Big
		else:
			self.endian = Endian.Little

	def connect(self):
		_logger.debug('connect {}'.format(self.host))
		self.client = ModbusClient(self.host, port=502)
		self.client.connect()

	def run(self):
		self.connect()
		try:
			while True:
				try:
					value = self.read()
				except IOError as e:
					print e
				else:
					self.print_value(value)
				time.sleep(2)
		except KeyboardInterrupt:
			self.client.close()
			pass

	def read(self):
		count = COUNTS.get(self.data_type)
		if not count:
			raise ValueError('Unsupported data type {}'.format(self.data_type))

		_logger.debug('read register: {}, count: {}, slave: {}, function: {}'.format(self.register_addr, count, self.slave_id, self.function_code))
		if self.function_code == 3:
			result = self.client.read_holding_registers(self.register_addr, count, unit=self.slave_id)
		elif self.function_code == 4:
			result = self.client.read_input_registers(self.register_addr, count, unit=self.slave_id)
		else:
			raise ValueError('Unsupported function code {}'.format(self.function_code))
		if result is None:
			raise IOError('No modbus reponse')
		if isinstance(result, ExceptionResponse):
			raise IOError(str(result))

		d = BinaryPayloadDecoder.fromRegisters(result.registers, endian=self.endian)

		if self.data_type == '16bit_int':
			value = d.decode_16bit_int()
		elif self.data_type == '16bit_uint':
			value = d.decode_16bit_uint()
		elif self.data_type == '32bit_int':
			value = d.decode_32bit_int()
		elif self.data_type == '32bit_uint':
			value = d.decode_32bit_uint()
		elif self.data_type == '32bit_float':
			value = d.decode_32bit_float()
		elif self.data_type == '64bit_float':
			value = d.decode_64bit_float()
		else:
			raise ValueError('Unsupported data type {}'.format(self.data_type))
		return value

	def print_value(self, value):
		"""
		Methode zur Ausgabe des Messwertes muss von der erbenden Klasse implementiert werden.
		"""
		raise NotImplementedError