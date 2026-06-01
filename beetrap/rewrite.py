from urllib.parse import urlparse


class ResponseRewriter:
    def __init__(self, target_domain, proxy_origin, extra_domains=None):
        self.target_domain = target_domain
        self.proxy_origin = proxy_origin
        self.extra_domains = extra_domains or []
        self._target_host = urlparse(target_domain).hostname

    def rewrite_location_header(self, location):
        if self._target_host in location:
            return location.replace(self._target_host, urlparse(self.proxy_origin).hostname or self._target_host)
        for extra in self.extra_domains:
            if extra in location:
                return location.replace(extra, self.proxy_origin)
        return location
