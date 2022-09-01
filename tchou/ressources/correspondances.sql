-- SQLite

select 
    count(*)
    st_first.arrival_time,
    st_first.drop_off_type as 'st_first.drop_off_type',
    st_first.stop_id,
    st_second.departure_time,
    st_second.stop_id,
    st_second.pickup_type as 'st_second.pickup_type'
from stop_times st_first
    join stop_times st_second on st_first.stop_id = st_second.stop_id and ( ( strftime('%s',st_second.arrival_time) - strftime('%s',st_first.arrival_time) ) / 60 ) between 3 and 15
    join trips t_first on t_first.trip_id = st_first.trip_id
    join trips t_second on t_second.trip_id = st_second.trip_id
where t_first.route_id <> t_second.route_id 
    and st_first.drop_off_type = '0' -- le stop n'est pas un départ du premier trip
    and st_second.pickup_type = '0' -- le stop n'est pas un terminus du second trip
;


select pivots.vtrip_id, pivot_stop_id, arrival_time, stop_id, stop_sequence as 'original_stop_sequence',
iif(trip_id = second_trip_id,stop_sequence + first_stop_sequence,stop_sequence) as 'news_stop_seq'
from (
    select 
        st_first.stop_id as 'pivot_stop_id',
        substr(st_first.trip_id,0,16) || ':' || substr(st_second.trip_id,0,16) as 'vtrip_id',
        st_first.stop_sequence as 'first_stop_sequence',
        st_first.trip_id as 'first_trip_id',
        st_second.stop_sequence as 'second_stop_sequence',
        st_second.trip_id as 'second_trip_id'
    from stop_times st_first
        join stop_times st_second on st_first.stop_id = st_second.stop_id and ( ( strftime('%s',st_second.arrival_time) - strftime('%s',st_first.arrival_time) ) / 60 ) between 3 and 15
        join trips t_first on t_first.trip_id = st_first.trip_id
        join trips t_second on t_second.trip_id = st_second.trip_id
    where t_first.route_id <> t_second.route_id
        and st_first.drop_off_type = '0' 
        and st_second.pickup_type = '0'
        limit 1000
) as pivots
join stop_times 
    on ( trip_id = first_trip_id and stop_sequence <= first_stop_sequence )
    or ( trip_id = second_trip_id and stop_sequence >= second_stop_sequence )
;


-- le TER 13195 a roulé le 05/03 de Paris St Lazare (06:09) à Rouen Rive Droite (07:46)
-- select * from trips where service_id like '%13195%'; 