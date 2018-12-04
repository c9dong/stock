# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.response import open_in_browser
from rocketimpl.rocket_impl import Rocket
  
class RocketSpider(scrapy.Spider):
  name = 'rocket'
  allowed_domains = ['rocketfinancial.com']

  start_urls = ['https://rocketfinancial.com/Login.aspx']

  def __init__(self, company_name=None, fid=None, pw=None, dry_run=0, *args, **kwargs):
    if company_name is None or fid is None or pw is None:
      raise Exception('incomplete arguments')

    self._company_name = company_name
    self._fid = fid
    self._pw = pw
    self._dry_run = int(dry_run)

  def parse(self, response):
    rocket = Rocket(self._company_name, self._fid, self._pw, self._dry_run)
    return rocket.parse(response)
