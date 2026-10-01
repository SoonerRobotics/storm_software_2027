"""Example usage of the robot logging system."""

from pathlib import Path

from logger import RobotLogger


def main() -> None:
    logfile = Path(__file__).parent / "example.log"
    logger = RobotLogger(logfile)

    logger.input(
        "Controller axis changed",
        source="driver_controller",
        data={"axis": "left_x", "value": 0.75},
    )
    logger.info("farty mc fart fart",
        source= "fart system"
                 )
    logger.info("Robot initialized", source="startup")
    logger.warning(
        "Battery voltage is low",
        source="power_monitor",
        data={"voltage": 11.2},
    )
    logger.error(
        "Motor controller unavailable",
        source="drive",
        data={"controller_id": 2},
    )
    logger.stats(
        "Loop statistics",
        source="main_loop",
        data={"loop_hz": 50, "cycle_ms": 20},
    )
    logger.debug("Debug diagnostic event", source="example")
    logger.system("Logging system test complete", source="example")
    logger.log(
        "CUSTOM",
        "Subsystem-specific event",
        source="example_subsystem",
        data={"state": "ready"},
    )

    print(f"Wrote example events to {logfile}")


if __name__ == "__main__":
    main()
