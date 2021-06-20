select timediff(
    (select create_time from information_schema.tables where table_schema='bus_info' and table_name='bus_info')
) as data_load_time_diff;

