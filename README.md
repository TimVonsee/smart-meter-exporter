# Smart meter exporter
A simpel Prometheus exporter that exposes Dutch smart meter metrics.

Edit: `sudo cp ./smart-meter-exporter.service /etc/systemd/system/smart-meter-exporter.service`

Starting: `sudo systemctl start smart-meter-exporter.service`

Check status: `sudo systemctl status smart-meter-exporter.service`

Reload after changes: `sudo systemctl daemon-reload`
