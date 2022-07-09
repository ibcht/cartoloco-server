drop table if exists stop_times;
drop table if exists routes;
drop table if exists calendar_dates;
drop table if exists feed_info;
drop table if exists agency;
drop table if exists stops;
drop table if exists trips;
drop table if exists transfers;
drop table if exists times;

create table stop_times (trip_id, arrival_time, departure_time, stop_id, stop_sequence, stop_headsign, pickup_type, drop_off_type, shape_dist_traveled);
create table routes (route_id, agency_id, route_short_name, route_long_name, route_desc, route_type, route_url, route_color, route_text_color);
create table calendar_dates (service_id, date, exception_type);
create table feed_info (feed_id, feed_publisher_name, feed_publisher_url, feed_lang, feed_start_date, feed_end_date, feed_version, conv_rev, plan_rev);
create table agency (agency_id, agency_name, agency_url, agency_timezone, agency_lang);
create table stops (stop_id, stop_name, stop_desc, stop_lat, stop_lon, zone_id, stop_url, location_type, parent_station);
create table trips (route_id, service_id, trip_id, trip_headsign, direction_id, block_id, shape_id);
create table transfers (from_stop_id, to_stop_id, transfer_type, min_transfer_time, from_route_id, to_route_id);
-- table calculée
create table times (type, src_id, tgt_id, src_name, tgt_name, min_time, max_time, min_stops, max_stops, total_trips);