import boto3
import math
from decimal import Decimal

class DynamoStore:
  def __init__(self):
    self._dynamodb = boto3.resource('dynamodb')
    self._table = self._dynamodb.Table('income_statement')

  def put_all(self, company, items):
    # for column in items:
    #   print(items[column])
    with self._table.batch_writer() as batch:
      for column in items:
        data = items[column].to_dict()
        data = self.__remove_empty_value(data)
        data = self.__remove_NaN(data)
        data = self.__replace_float(data)
        item = {
          'company_name': company, #primary key
          'date': column,   #sort key
          'data': data
        }
        batch.put_item(Item=item)

  def __remove_empty_value(self, data):
    return dict((k, v) for k, v in data.iteritems() if v)

  def __remove_NaN(self, data):
    return dict((k, v) for k, v in data.iteritems() if v == v)

  def __replace_float(self, data):
    if isinstance(data, list):
      for i in xrange(len(data)):
        data[i] = self.__replace_float(data[i])
      return data
    elif isinstance(data, dict):
      for k in data.iterkeys():
        data[k] = self.__replace_float(data[k])
      return data
    elif isinstance(data, float):
      if data % 1 == 0:
        return int(data)
      else:
        return Decimal(str(data))
    else:
      return data