from cheminfra.containers import parse_apache_log_line
from datetime import datetime

def test_apache_parse_log_line():
  log_line = "127.0.0.1 - - [01/Aug/2025:12:00:00 +0000] \"GET / HTTP/1.1\" 200 1234"
  parsed = parse_apache_log_line(log_line)
  assert parsed is not None
  assert parsed.status == 200
  assert parsed.source_ip == "127.0.0.1"
  assert parsed.method == "GET"
  assert parsed.path == "/"
  assert parsed.timestamp == datetime(2025, 8, 1, 12, 0, 0)

def test_apache_parse_log_line_docker_startup_message():
  log_line = "/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh"
  parsed = parse_apache_log_line(log_line)
  assert parsed is None