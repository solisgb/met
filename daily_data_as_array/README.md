From a daily data file (with nulls) containing id, date, value, write another file with the daily data stored in an array that can be imported into a Postgres DB and containing id, year, month, daily data in an array (int2).
In the original format each daily data is a row; in the new format each year/month is a row.
The new format is interesting when the station has data almost every day of the month, because it saves a lot of disk space.

