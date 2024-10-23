# This file is a part of ThreatMatrix https://github.com/khulnasoft/ThreatMatrix
# See the file 'LICENSE' for copying permission.

from threat_matrix import secrets

# AWS settings
AWS_IAM_ACCESS = secrets.get_secret("AWS_IAM_ACCESS", False) == "True"
if not AWS_IAM_ACCESS:
    AWS_ACCESS_KEY_ID = secrets.get_secret("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = secrets.get_secret("AWS_SECRET_ACCESS_KEY")
AWS_SECRETS = secrets.get_secret("AWS_SECRETS", False) == "True"
AWS_SQS = secrets.get_secret("AWS_SQS", False) == "True"
AWS_REGION = secrets.get_secret("AWS_REGION", "eu-central-1")
AWS_USER_NUMBER = secrets.get_secret("AWS_USER_NUMBER")

AWS_RDS_IAM_ROLE = secrets.get_secret("AWS_RDS_IAM_ROLE", False) == "True"
