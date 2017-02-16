import json
from urllib import urlopen, urlencode
import unittest

class AccuWeatherApi(object):

	def __init__(self, apikey):
		self.apikey = apikey
		self.base_url = 'http://dataservice.accuweather.com'
		self.version = 'v1'
	

	def url_builder(self, endpoint, params, *args):
		url_details = '/'.join(args)
		encoded_params = self.encode_params(params)

		full_url = '%s/%s/%s/%s?%s' % (self.base_url, endpoint, self.version, url_details, encoded_params)

		return full_url

	def encode_params(self, params=None):
		params_dict = {}
		params_dict['apikey'] = self.apikey

		if params is not None:
			params_dict.update(params)

		encoded_params = urlencode(params_dict)
		
		return encoded_params


'''
	AccuWeather API Url builder
'''

class AccuWeatherCondition(object):
	
	def __init__(self, accu_id, api):
		self.accu_id = accu_id
		self.endpoint = 'currentconditions'
		self.api = api

	def currentconditions(self):
		full_url = self.api.url_builder(self.endpoint, None, self.accu_id)
		accu_data  = urlopen(full_url)
		
		return json.loads(accu_data.read())



'''
	AccuWeather Object Factory
'''

class AccuWeatherFactory(object):

	accu_types = {'currentcondition':AccuWeatherCondition}
	# def __init__(self, accu_type):
	# 	self.accu_type = accu_type
	# 	self.accu_id = accu_id

	@classmethod
	def create_object(cls, accu_type, accu_id, api):
		return cls.accu_types[accu_type](accu_id, api)



'''
	AccuWeather CurrentConditions Manager
'''

class CurrentConditions(object):

	def __init__(self):
		self.conditions = []

	def __current_factory(self, accu_id, api):
		currentcondition = AccuWeatherFactory.create_object('currentcondition', accu_id, api)
		return currentcondition

	def add_condition(self, accu_id, api):
		currentcondition = self.__current_factory(accu_id, api)
		self.conditions.append(currentcondition)

	def get_temperatures(self,unit_type=None):
		temperatures = []
		
		for condition in self.conditions:

			condition_dict = condition.currentconditions()[0]
			condition_dict['TemperatureMetric'] = condition_dict['Temperature']['Metric']['Value']
			condition_dict['TemperatureImperial'] = condition_dict['Temperature']['Imperial']['Value']
			condition_dict.pop('Temperature', None)

			temperatures.append(condition_dict)

		return temperatures



if __name__ == '__main__':
	# unittest.main()
	api = AccuWeatherApi('l2wAkfYTeei3nibA0rqqPTozyLQavG5h')
	# peru = AccuWeatherCondition('264120', api)
	# print peru.currentconditions()
	temps = CurrentConditions()
	temps.add_condition('26420', api)
	temps.add_condition('7894', api)
	temps.add_condition('60449', api)
	print(temps.get_temperatures())
	# AccuWeatherFactory.create_object('currentcondition','264120',api)


