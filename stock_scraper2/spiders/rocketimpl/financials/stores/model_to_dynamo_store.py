import boto3
from decimal import Decimal

class ModelToDynamoStore:
  def __init__(self):
    self._dynamodb = boto3.resource('dynamodb')
    self._table = self._dynamodb.Table('rocket_quarterly_income_statements')

  def put_all(self, company, items):
    with self._table.batch_writer() as batch:
      for item in items:
        data = {
          'company': company,
          'year_quarter': str(item.year) + '_' + str(item.quarter),
          'year': item.year,
          'quarter': item.quarter,
          'revenues': item.revenues,
          'total_revenues': item.total_revenues,
          'goods_sold': item.goods_sold,
          'gross_profit': item.gross_profit,
          'sales_and_marketing': item.sm,
          'research_and_development': item.rd,
          'general_and_administrative': item.ga,
          'ebitda': item.ebitda,
          'depreciation': item.depreciation,
          'ebita': item.ebita,
          'amortization': item.amortization,
          'ebit': item.ebit,
          'pretax_income': item.pretax_income,
          'income_taxes': item.income_taxes,
          'net_income': item.net_income,
          'basic_shares': item.basic_shares,
          'diluted_shares': item.diluted_shares,
          'basic_eps': item.basic_eps,
          'diluted_eps': item.diluted_eps,
          'dividend_per_share': item.dps
        }
        data = self.__replace_float(data)
        batch.put_item(Item=data)

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