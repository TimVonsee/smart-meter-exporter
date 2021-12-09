# Smart meter exporter
A simpel Prometheus exporter that exposes Dutch smart meter metrics.

1. Install dependecies: `pip install -r requirements.txt`
2. Copy: `sudo cp ./smart-meter-exporter.service /etc/systemd/system/smart-meter-exporter.service`
3. `sudo systemctl daemon-reload`
4. Starting: `sudo systemctl start smart-meter-exporter.service`
5. `sudo systemctl enable smart-meter-exporter.service`
6. Check status: `sudo systemctl status smart-meter-exporter.service`
7. Check exporter: `curl localhost:8000`
