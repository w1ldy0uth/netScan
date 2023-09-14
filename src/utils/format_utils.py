import time


def get_seconds_since_epoch(timestamp: int) -> int:
    """
    Takes a unix timestamp and returns the number of seconds since the unix epoch.

    Params:
        timestamp (int): The unix timestamp.

    Returns:
        int: The number of seconds since the unix epoch.
    """

    return int(time.time()) - timestamp


def format_duration(timestamp: int):
    """
    Takes a unix timestamp and returns a human-readable version of passed time.

    Params:
        seconds (int): The unix timestamp.

    Returns:
        str: A human-readable version of the passed time.
    """
    seconds = get_seconds_since_epoch(timestamp)

    units = [("year", 31536000), ("day", 86400), ("hour", 3600), ("minute", 60), ("second", 1)]
    result = []

    for unit, value in units:
        if seconds >= value:
            num_units = seconds // value
            seconds %= value
            if num_units > 1:
                unit += "s"
            result.append(f"{num_units} {unit}")

    if not result:
        return "0 seconds"

    if len(result) == 1:
        return result[0]

    last_unit = result.pop()
    return ", ".join(result) + f", {last_unit}"


def format_memory(total_bytes: int):
    gigabytes = total_bytes / (1024 ** 3)
    return f"{gigabytes:.2f}GB"


if __name__ == "__main__":
    print(format_duration(12365345))
