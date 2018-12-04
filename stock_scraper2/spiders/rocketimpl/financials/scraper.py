class Scraper:
  def __init__(self, scrapy, company_name, url_generator, data_formatter, data_combiner, data_storage):
    self._scrapy = scrapy
    self._company_name = company_name
    self._url_generator = url_generator
    self._data_formatter = data_formatter
    self._data_combiner = data_combiner
    self._data_storage = data_storage

    self._expected_items = 0
    self._current_items = 0

  def scrape_all(self):
    for url in self._url_generator.generate_all():
      # print url
      self._expected_items += 1
      
      meta = {'dont_redirect': True, 'handle_httpstatus_list': [302]}
      yield self._scrapy.Request(url=url, callback=self.__scrape_callback, meta=meta)

  def __scrape_callback(self, response):
    self._current_items += 1
    if not self.__is_status_success(response.status):
      return

    data = self._data_formatter.format(response)
    self._data_combiner.combine(data)
    
    if self._expected_items == self._current_items:
      all_data = self._data_combiner.get()
      self._data_storage.put_all(self._company_name, all_data)

  def __is_status_success(self, status):
    return status >= 200 and status < 300