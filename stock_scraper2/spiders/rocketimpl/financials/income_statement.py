import itertools

import const
from scraper import Scraper
from pageable_url_generator import PageableUrlGenerator
from formatters.panda_formatter import PandaFormatter
from combiners.row_combiner import RowCombiner
from stores.dynamo_store import DynamoStore
from stores.dry_store import DryStore
from formatters.income_statement_formatter import IncomeStatementFormatter
from combiners.array_combiner import ArrayCombiner
from stores.model_to_dynamo_store import ModelToDynamoStore

class IncomeStatement:
  def __init__(self, scrapy, dry_run=0):
    self._scrapy = scrapy
    self._dry_run = dry_run

  def scrape(self, company_name, company_fid, company_pw):
    base_url = '{}/{}'.format(const.BASE_URL, const.DIRECTORY)
    params_map = {
      const.COMPANY_FID: company_fid,
      const.COMPANY_PW: company_pw,
      const.TIME_SPAN: const.TIME_QUARTERLY,
      const.REPORT_TYPE: const.REPORT_STANDARDIZED,
      const.STAT_TYPE: const.STAT_BUSINESS
    }

    url_generator = PageableUrlGenerator(base_url, params_map, const.PAGE_KEY, const.PAGE_COUNT, const.PAGE_TOTAL_QUARTERLY)
    formatter = IncomeStatementFormatter()
    combiner = ArrayCombiner()

    store = ModelToDynamoStore()
    if self._dry_run == 1:
      store = DryStore()
      
    scraper = Scraper(self._scrapy, company_name, url_generator, formatter, combiner, store)
    
    return itertools.chain(scraper.scrape_all())