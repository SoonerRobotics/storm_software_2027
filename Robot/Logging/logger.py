"""Structured file logging for robot events."""

from __future__ import annotations

import json
import threading
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path
from typing import Any, Mapping


class EventType(StrEnum):
    """Standard event categories used by the robot."""

    INPUT = "INPUT"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    STATS = "STATS"
    DEBUG = "DEBUG"
    SYSTEM = "SYSTEM"


@dataclass(frozen=True, slots=True)
class LogEvent:
    """A serializable event written as one JSON object per log line."""

    event_type: str
    message: str
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    source: str | None = None
    data: dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> str:
        """Return the event in JSON Lines format."""
        return json.dumps(asdict(self), separators=(",", ":"), default=str)


class RobotLogger:
    """Thread-safe JSON Lines logger with convenience methods for common events."""

    def __init__(self, logfile: str | Path = "logs/robot.log") -> None:
        self.logfile = Path(logfile)
        self.logfile.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def log(
        self,
        event_type: EventType | str,
        message: str,
        *,
        source: str | None = None,
        data: Mapping[str, Any] | None = None,
    ) -> LogEvent:
        """Write an event and return the event that was written.

        ``event_type`` accepts either an ``EventType`` or a custom string so
        new event categories do not require a library change.
        """
        event = LogEvent(
            event_type=str(event_type),
            message=message,
            source=source,
            data=dict(data or {}),
        )
        with self._lock:
            with self.logfile.open("a", encoding="utf-8") as file:
                file.write(event.to_json())
                file.write("\n")
        return event

    def input(
        self,
        message: str,
        *,
        source: str | None = None,
        data: Mapping[str, Any] | None = None,
    ) -> LogEvent:
        return self.log(EventType.INPUT, message, source=source, data=data)

    def info(
        self,
        message: str,
        *,
        source: str | None = None,
        data: Mapping[str, Any] | None = None,
    ) -> LogEvent:
        return self.log(EventType.INFO, message, source=source, data=data)

    def warning(
        self,
        message: str,
        *,
        source: str | None = None,
        data: Mapping[str, Any] | None = None,
    ) -> LogEvent:
        return self.log(EventType.WARNING, message, source=source, data=data)

    def error(
        self,
        message: str,
        *,
        source: str | None = None,
        data: Mapping[str, Any] | None = None,
    ) -> LogEvent:
        return self.log(EventType.ERROR, message, source=source, data=data)

    def stats(
        self,
        message: str,
        *,
        source: str | None = None,
        data: Mapping[str, Any] | None = None,
    ) -> LogEvent:
        return self.log(EventType.STATS, message, source=source, data=data)

    def debug(
        self,
        message: str,
        *,
        source: str | None = None,
        data: Mapping[str, Any] | None = None,
    ) -> LogEvent:
        return self.log(EventType.DEBUG, message, source=source, data=data)

    def system(
        self,
        message: str,
        *,
        source: str | None = None,
        data: Mapping[str, Any] | None = None,
    ) -> LogEvent:
        return self.log(EventType.SYSTEM, message, source=source, data=data)
