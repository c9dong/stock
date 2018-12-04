class IncomeStatement:
  year = None
  quarter = None
  revenues = {}
  total_revenues = None
  goods_sold = None
  gross_profit = None
  sm = None # sales and marketing
  rd = None # research and development
  ga = None # general and administrative
  ebitda = None
  depreciation = None
  ebita = None
  amortization = None
  ebit = None
  pretax_income = None
  income_taxes = None
  net_income = None
  basic_shares = None
  diluted_shares = None
  basic_eps = None
  diluted_eps = None
  dps = None # dividend per share

class IncomeStatementFormatter:
  def format(self, response):
    table = response.css('table#gridReport tr')
    if len(table) == 0:
      return None

    main_heading = table[0].css('th ::text').extract()
    main_heading = self.__headers_to_quarter(main_heading[1:])

    # get raw texts
    table_data = map(lambda data: map(self.__text, data.css('td')), table[1:])

    contents = []
    for i in range(len(main_heading)):
      content = self.__format_body(main_heading[i], table_data, i)
      contents.append(content)

    # self.__print(contents)

    return contents

  def __text(self, cell):
    text = ''
    cell_data = cell.css('::text').extract()
    for data in cell_data:
      text+=data

    return text

  def __headers_to_quarter(self, headers):
    years = map(lambda header: header.split('-')[2], headers)
    initial_quarter = 1
    for i in range(len(years)-1):
      if years[i] == years[i+1]:
        initial_quarter += 1
      else:
        break

    quarter = initial_quarter
    new_headers = []
    for year in years:
      if int(year) > 50:
        y = int('19' + year)
      else:
        y = int('20' + year)
      q = quarter
      quarter -= 1
      if quarter == 0:
        quarter = 4

      new_headers.append((y, q))

    return new_headers

  def __format_body(self, heading, body, body_index):
    actual_body_index = body_index + 1
    content = IncomeStatement()
    content.year = heading[0]
    content.quarter = heading[1]
    content.revenues = self.__format_revenues(body, body_index)
    content.total_revenues = self.__find_content(body, body_index, 'total revenues')
    content.goods_sold = self.__find_content(body, body_index, 'goods sold')
    content.gross_profit = self.__find_content(body, body_index, 'gross profit')
    content.sm = self.__find_content(body, body_index, 'sales and marketing')
    content.rd = self.__find_content(body, body_index, 'research and development')
    content.ga = self.__find_content(body, body_index, 'general and administrative')
    content.ebitda = self.__find_content(body, body_index, 'ebitda')
    content.depreciation = self.__find_content(body, body_index, 'depreciation')
    content.ebita = self.__find_content(body, body_index, 'ebita')
    content.amortization = self.__find_content(body, body_index, 'amortization')
    content.ebit = self.__find_content(body, body_index, 'ebit', ['ebita', 'ebitda'])
    content.pretax_income = self.__find_content(body, body_index, 'pre-tax income')
    content.income_taxes = self.__find_content(body, body_index, 'income taxes')
    content.net_income = self.__find_content(body, body_index, 'net income')
    content.basic_shares = self.__find_content(body, body_index, 'shares outstanding (basic)')
    content.diluted_shares = self.__find_content(body, body_index, 'shares outstanding (diluted)')
    content.basic_eps = self.__find_content(body, body_index, 'basic eps')
    content.diluted_eps = self.__find_content(body, body_index, 'diluted eps')
    content.dps = self.__find_content(body, body_index, 'dividends per share')

    return content

  def __format_revenues(self, body, body_index):
    actual_body_index = body_index + 1
    iterator = iter(body)
    while True:
      data = iterator.next()
      if 'revenues' in data[0].lower():
        break

    revenues = {}
    while True:
      data = iterator.next()
      if 'total revenues' in data[0].lower():
        break

      title = self.__clean_title(data[0])
      content = self.__clean_content(data[actual_body_index])
      revenues[title] = content

    return revenues

  def __find_content(self, body, body_index, title, neg=[]):
    actual_body_index = body_index + 1
    for row in body:
      if title in row[0].lower():
        has_neg = False
        for n in neg:
          if n in row[0].lower():
            has_neg = True
            break
        if not has_neg:
          return self.__clean_content(row[actual_body_index])

    return None

  def __clean_title(self, title):
    TAB = u'\xa0'
    PLUS_BOX = '[+]'
    SPACE = ' '
    COLON = ':'
    title = title.replace(PLUS_BOX, '') \
      .replace(TAB, '') \
      .replace(COLON, '') \
      .replace('(', '') \
      .replace(')', '') \
      .replace(' .', '.') \
      .strip()
    return title

  def __clean_content(self, content):
    PERCENT = '%'
    DOLLAR = '$'
    COMMA = ','
    LEFT_BRACKET = '('
    RIGHT_BRACKET = ')'
    multiplier = 1000000
    if DOLLAR in content or PERCENT in content:
      multiplier = 1
    if LEFT_BRACKET in content and RIGHT_BRACKET in content:
      multiplier = multiplier * -1

    content = content.replace(PERCENT, '') \
      .replace(DOLLAR, '') \
      .replace(COMMA, '') \
      .replace(LEFT_BRACKET, '') \
      .replace(RIGHT_BRACKET, '') \

    try:
      content = float(content)
      return content * multiplier
    except ValueError:
      return None

  def __print(self, contents):
    for content in contents:
      print content.year
      print content.quarter
      print content.revenues
      print content.total_revenues
      print content.goods_sold
      print content.gross_profit
      print content.sm
      print content.rd
      print content.ga
      print content.ebitda
      print content.depreciation
      print content.ebita
      print content.amortization
      print content.ebit
      print content.pretax_income
      print content.income_taxes
      print content.net_income
      print content.basic_shares
      print content.diluted_shares
      print content.basic_eps
      print content.diluted_eps
      print content.dps

    
