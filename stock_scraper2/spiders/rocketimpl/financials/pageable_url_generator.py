class PageableUrlGenerator:
  def __init__(self, base_url, params_map, page_key, count, total):
    self._base_url = base_url
    self._params_map = params_map
    self._page_key = page_key
    self._count = count
    self._total = total

  def generate_all(self):
    # for i in range(0, 1):
    for i in range(0, self._total+1, self._count):
      yield '{}{}={}'.format(self.__generate_single_page(), self._page_key, i)

  def __generate_single_page(self):
    return '{}?{}'.format(self._base_url, self.__generate_params())

  def __generate_params(self):
    params = ''
    for k, v in self._params_map.iteritems():
      params += '{}={}&'.format(k, v)

    return params