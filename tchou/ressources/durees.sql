-- SQLite
delete from times;

insert into times 
select
    replace(replace(s_src.stop_id,substr(s_src.stop_id,instr(s_src.stop_id,'-')),''),'StopPoint:',''),
    a_src.stop_id as 'from',
    a_trg.stop_id as 'to',
    a_src.stop_name as 'from_name',
    a_trg.stop_name as 'to_name',
    min((strftime('%s',st_trg.departure_time) - strftime('%s',st_src.arrival_time)) / 60) as 'min_time',
    max((strftime('%s',st_trg.departure_time) - strftime('%s',st_src.arrival_time)) / 60) as 'max_time',
    min(st_trg.stop_sequence - st_src.stop_sequence) as 'min_stops',
    max(st_trg.stop_sequence - st_src.stop_sequence) as 'max_stops',
    count(1) as 'total_trips'
from stop_times st_src
join stop_times st_trg on (st_src.trip_id = st_trg.trip_id and st_src.stop_id <> st_trg.stop_id and st_src.departure_time < st_trg.arrival_time)
join stops s_src on st_src.stop_id = s_src.stop_id
join stops s_trg on st_trg.stop_id = s_trg.stop_id
join stops a_src on s_src.parent_station = a_src.stop_id
join stops a_trg on s_trg.parent_station = a_trg.stop_id
where s_src.location_type = '0' and st_src.stop_id not like 'StopPoint:OCECar TER%' -- exclure les trajets en CAR
group by st_src.stop_id, st_trg.stop_id;

