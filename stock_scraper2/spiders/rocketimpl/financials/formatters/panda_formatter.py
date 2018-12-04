import pandas as pd
import numpy as np
from scrapy.utils.response import open_in_browser

TAB = u'\xa0'
PLUS_BOX = '[+]'
SPACE = ' '
COLON = ':'
PERCENT = '%'
DOLLAR = '$'

class PandaFormatter:
  def format(self, response):
    table = response.css('table#gridReport tr')
    if len(table) == 0:
      return None

    main_heading = table[0].css('th ::text').extract()
    # convert format to year-month-day
    main_heading = map(self.__date_to_ymd, main_heading)

    # get raw texts
    table_data = map(lambda data: map(self.__text, data.css('td')), table[1:])
    # add (+) to proper headers
    table_data = map(self.__add_expansion, table_data)
    # filter empty headings
    table_data = filter(self.__filter_no_heading, table_data)
    # expand namespace
    table_data = self.__reduce_heading_two_levels(table_data)
    # strip characters
    table_data = map(self.__clean_text, table_data)
    # to snake case
    table_data = map(self.__heading_to_snake_case, table_data)
    # remove heading with no data
    table_data = filter(self.__filter_only_heading, table_data)
    # change percentage to numbers
    table_data = map(self.__format_percentage, table_data)
    # change dollar to numbers
    table_data = map(self.__format_dollar, table_data)

    # self.__print_table(table_data)

    data = np.array([main_heading] + table_data)
    pd_data = pd.DataFrame(data=data[1:, 1:], index=data[1:, 0], columns=data[0, 1:])
    return pd_data

  def __date_to_ymd(self, date):
    def format_month(month):
      month_list = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
      return month_list.index(str(month).lower()) + 1

    date_list = date.split('-')
    if len(date_list) != 3:
      return date

    month = str(format_month(date_list[0])).zfill(2)
    year = str(date_list[2]).zfill(2)
    day = str(date_list[1]).zfill(2)
    return '{}-{}-{}'.format(year, month, day)

  def __text(self, cell):
    text = ''
    cell_data = cell.css('::text').extract()
    for data in cell_data:
      text+=data

    return text

  def __add_expansion(self, row):
    heading = row[0]
    if len(row) == 1 and not (PLUS_BOX in row[0]):
      row[0] = row[0] + ' ' + PLUS_BOX
    return row

  def __clean_text(self, row):
    new_row = []
    for data in row:
      data = data.replace(PLUS_BOX, '') \
        .replace(TAB, '') \
        .replace(COLON, '') \
        .replace('(', '') \
          .replace(')', '') \
          .replace(' .', '.') \
          .strip()
      new_row.append(data)
    return new_row

  def __heading_to_snake_case(self, row):
    heading = row[0].lower().replace(' ', '_').replace('-', '_')
    row[0] = heading
    return row

  def __filter_no_heading(self, row):
    heading = row[0]
    return heading.strip() != ''

  def __reduce_heading_two_levels(self, table_data):
    new_table_data = []
    parent_heading = ''
    for row in table_data:
      heading = row[0]
      if PLUS_BOX in heading:
        parent_heading = (heading)
      elif heading[0] == TAB:
        heading = (parent_heading) + '.' + (heading)

      heading = (heading)
      new_table_data.append([heading] + row[1:])

    return new_table_data

  def __filter_only_heading(self, row):
    return len(row) > 1

  def __format_percentage(self, row):
    new_row = []
    new_row.append(row[0])
    isPercent = False
    for cell in row[1:]:
      new_cell = cell
      if cell[-1:] == PERCENT:
        isPercent = True
        new_cell = cell[0:-1]
      new_row.append(new_cell)

    if isPercent:
      new_row[0] += '$percentage'

    return new_row

  def __format_dollar(self, row):
    new_row = []
    new_row.append(row[0])
    isPercent = False
    for cell in row[1:]:
      new_cell = cell
      if cell[0:1] == DOLLAR:
        isPercent = True
        new_cell = cell[1:]
      new_row.append(new_cell)

    if isPercent:
      new_row[0] += '$dollar'

    return new_row

  def __print_table(self, table):
    for row in table:
      print row
