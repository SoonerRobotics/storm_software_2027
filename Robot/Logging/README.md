# Robot logging

`RobotLogger` writes one JSON object per line to a logfile. JSON Lines keeps
events easy to inspect while allowing any event payload to be represented.

```python
from Robot.Logging import RobotLogger

logger = RobotLogger("logs/robot.log")
logger.input(
    "Controller axis changed",
    source="driver_controller",
    data={"axis": "left_x", "value": 0.75},
)
logger.info("Robot initialized")
logger.warning("Battery voltage is low", data={"voltage": 11.2})
logger.error("Motor controller unavailable", source="drive")
logger.stats("Loop statistics", data={"loop_hz": 50, "cycle_ms": 20})
logger.log("CUSTOM", "A subsystem-specific event", data={"state": "ready"})
```

Each event includes an ISO-8601 UTC timestamp, event type, message, optional
source, and optional structured data. Standard event types are `INPUT`,
`INFO`, `WARNING`, `ERROR`, `STATS`, `DEBUG`, and `SYSTEM`; custom strings are
also supported.

To run the example from this directory:

```bash
python3 example.py
```

This writes `example.log` next to the script. Logfiles are ignored by Git.

## Dashboard example

Open `dashboard.html` in a browser and click **Use sample data**, or choose
`example.log` with **Load logfile**. The dashboard reads the logger's
JSON Lines format and provides event counts, search, type filtering, and a
timeline with event data.
