#UserRateThrottle automatically tracks the IP

from rest_framework.throttling import (
    UserRateThrottle
)


class SuggestRateThrottle(
    UserRateThrottle
):
    rate = "20/min"