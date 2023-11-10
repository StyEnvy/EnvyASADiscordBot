Timezone Reference for pytz

When setting the BOT_TIMEZONE variable in your .env file, use one of the following timezone strings. These strings are compatible with the pytz library and cover major US and EU timezones.
United States Timezones:

    Eastern Standard Time: America/New_York
    Central Standard Time: America/Chicago
    Mountain Standard Time: America/Denver
    Pacific Standard Time: America/Los_Angeles
    Alaska Standard Time: America/Anchorage
    Hawaii-Aleutian Standard Time: Pacific/Honolulu

European Timezones:

    Western European Time (UK/Ireland/Portugal): Europe/Lisbon
    Central European Time (Spain, France, Germany, etc.): Europe/Berlin
    Eastern European Time (Finland, Greece, Romania, etc.): Europe/Helsinki

Notes:

    These timezones consider Daylight Saving Time (DST) changes where applicable.
    Ensure you use the exact string as shown for compatibility.
    You can find a comprehensive list of timezones supported by pytz at https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568