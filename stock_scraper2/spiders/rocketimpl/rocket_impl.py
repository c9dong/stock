import scrapy
import itertools
import os

from financials.income_statement import IncomeStatement

class Rocket:
  login_user = os.environ['ROCKET_USR']
  login_pass = os.environ['ROCKET_PASS']

  def __init__(self, company_name, fid, pw, dry_run=0):
    self._company_name = company_name
    self._fid = fid
    self._pw = pw
    self._dry_run = dry_run

  def parse(self, response):
    def _getInput(response, input_id):
      return response.css('input#'+input_id+'::attr(value)').extract_first();

    ctrl_header_toolkit = _getInput(response, 'ctrlHeader_toolkitScriptManager_HiddenField')
    view_state = _getInput(response, '__VIEWSTATE')
    event_target = _getInput(response, '__EVENTTARGET')
    event_argument = _getInput(response, '__EVENTARGUMENT')
    view_state_generator = _getInput(response, '__VIEWSTATEGENERATOR')
    event_validation = _getInput(response, '__EVENTVALIDATION')
    ctrl_header_searchBar_watermark = _getInput(response, 'ctrlHeader_searchBar_watermarkExtender_ClientState')
    ctrl_header_searchBar_txtSearch = _getInput(response, 'ctrlHeader_searchBar_txtSearch')
    ctrl_header_searchBar_hiddenControl = _getInput(response, 'ctrlHeader_searchBar_hiddenControl')

    form_data = {
      'ctrlHeader_toolkitScriptManager_HiddenField': ctrl_header_toolkit,
      '__EVENTTARGET': event_target,
      '__EVENTARGUMENT': event_argument,
      '__VIEWSTATE': view_state,
      '__VIEWSTATEGENERATOR': view_state_generator,
      '__EVENTVALIDATION': event_validation,
      'ctrlHeader$searchBar$watermarkExtender_ClientState': ctrl_header_searchBar_watermark,
      'ctrlHeader$searchBar$txtSearch': ctrl_header_searchBar_txtSearch,
      'ctrlHeader$searchBar$hiddenControl': ctrl_header_searchBar_hiddenControl,
      'username': self.login_user,
      'password': self.login_pass,
      'chkRememberMe': 'on',
      'btnLogin': 'Sign In',
      'hiddenInputToUpdateATBuffer_CommonToolkitScripts': '1'
    }

    return scrapy.FormRequest.from_response(response, formdata=form_data, callback=self._scrape)

  def _scrape(self, response):
    if not self.__isOk(response.status):
      return

    income_statement = IncomeStatement(scrapy, self._dry_run)
    return itertools.chain(income_statement.scrape(self._company_name, self._fid, self._pw))

  def __isOk(self, status):
    return status >= 200 and status < 300
    