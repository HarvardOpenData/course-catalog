def time_to_military(time_string, meridian_string):
    """
    Usage: `time_to_military('0130','PM') => 1330
    """

    cleaned_time = int(time_string)

    # first off, 12:xx should actually be 0:xx
    if int(cleaned_time / 100) == 12:
        cleaned_time -= 1200

    # now add 1200 to PMs
    if meridian_string == "PM":
        # e.g. 1:30pm == 1330 hours
        cleaned_time += 1200

    return cleaned_time
