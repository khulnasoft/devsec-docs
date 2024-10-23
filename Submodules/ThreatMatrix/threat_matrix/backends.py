# This file is a part of ThreatMatrix https://github.com/khulnasoft/ThreatMatrix
# See the file 'LICENSE' for copying permission.

from radiusauth.backends import RADIUSRealmBackend

from configuration.radius_config import GET_SERVER_CUSTOMISED, custom_get_server


class CustomRADIUSBackend(RADIUSRealmBackend):
    def get_server(self, realm):
        if GET_SERVER_CUSTOMISED:
            return custom_get_server(self, realm)
        else:
            return super().get_server(realm)
