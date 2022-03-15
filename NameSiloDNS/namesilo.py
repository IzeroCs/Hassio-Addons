import xmltodict
import os
import requests

from models import DomainInfo
from models import DnsRecords
from exceptions import exception_codes

class NameSilo:
    def __init__(self, token, sandbox: bool = True):
        self._token = token
        if sandbox:
            self._base_url = "http://sandbox.namesilo.com/api/"
        else:
            self._base_url = "https://www.namesilo.com/api/"

    def _process_data(self, url_extend):
        parsed_context = self._get_content_xml(url_extend)
        self.check_error_code(self._get_error_code(parsed_context))
        return parsed_context

    @staticmethod
    def _get_error_code(data):
        return int(data['namesilo']['reply']['code']), \
            data['namesilo']['reply']['detail']

    @staticmethod
    def check_error_code(error_code: tuple):
        if error_code[0] in [300, 301, 302]:
            return exception_codes[error_code[0]]
        else:
            raise exception_codes[error_code[0]](error_code[1])

    def _get_content_xml(self, url):
        api_request = requests.get(os.path.join(self._base_url, url))
        if api_request.status_code != 200:
            raise Exception(
                f"API responded with status code: {api_request.status_code}")

        content = xmltodict.parse(api_request.content.decode())
        return content

    def get_domain_info(self, domain_name):
        url_extend = f"getDomainInfo?version=1&type=xml&key={self._token}&" \
                     f"domain={domain_name}"
        parsed_content = self._process_data(url_extend)
        return DomainInfo(parsed_content)

    def dns_list_records(self, domain_name):
        url_extend = f"dnsListRecords?version=1&type=xml&key={self._token}&" \
                     f"domain={domain_name}"
        parse_content = self._process_data(url_extend)
        return DnsRecords(parse_content)

    def dns_update_record(self, domain_name, id, host, value, ttl):
        url_extend = f"dnsUpdateRecord?version=1&type=xml&key={self._token}&" \
                     f"domain={domain_name}&rrid={id}&rrhost={host}&" \
                     f"rrvalue={value}&rrttl={ttl}"
        self._process_data(url_extend)
        return True

    def dns_add_record(self, domain_name, type, host, value, ttl):
        url_extend = f"dnsAddRecord?version=1&type=xml&key={self._token}&" \
                     f"domain={domain_name}&rrtype={type}&rrhost={host}&" \
                     f"rrvalue={value}&rrttl={ttl}"
        self._process_data(url_extend)
        return True
