# This file is a part of ThreatMatrix https://github.com/khulnasoft/ThreatMatrix
# See the file 'LICENSE' for copying permission.

import logging
from ipaddress import AddressValueError, IPv4Address
from unittest.mock import patch
from urllib.parse import urlparse

# prints generated by import warnings are normal for this package
import dnstwist
from django.conf import settings

from api_app.analyzers_manager import classes
from api_app.analyzers_manager.exceptions import AnalyzerRunException
from tests.mock_utils import if_mock_connections

logger = logging.getLogger(__name__)


class DNStwist(classes.ObservableAnalyzer):
    DNS_TWIST_PATH = settings.BASE_DIR / "dnstwist-dictionaries"

    tld_dict: str
    language_dict: str
    fuzzy_hash: str
    fuzzy_hash_url: str
    mxcheck: bool
    user_agent: str
    nameservers: str

    def run(self):
        domain = self.observable_name
        if self.observable_classification == self.ObservableTypes.URL:
            domain = urlparse(self.observable_name).hostname
            try:
                IPv4Address(domain)
            except AddressValueError:
                pass
            else:
                raise AnalyzerRunException(
                    "URL with an IP address instead of a domain cannot be analyzed"
                )

        params = {"domain": domain, "registered": True, "format": "json"}

        if self.fuzzy_hash:
            params["lsh"] = self.fuzzy_hash
            if self.fuzzy_hash_url:
                params["lsh-url"] = self.fuzzy_hash_url
        if self.mxcheck:
            params["mxcheck"] = True
        if self.tld_dict:
            params["tld"] = self.DNS_TWIST_PATH / self.tld_dict
        if self.language_dict:
            params["dictionary"] = self.DNS_TWIST_PATH / self.language_dict
        if self.nameservers:
            params["nameservers"] = self.nameservers
        if self.user_agent:
            params["useragent"] = self.user_agent

        report = dnstwist.run(**params)

        return report

    @classmethod
    def _monkeypatch(cls):
        patches = [
            if_mock_connections(
                patch(
                    "dnstwist.run",
                    return_value={},
                ),
            )
        ]
        return super()._monkeypatch(patches=patches)
