create table if not exists aemet.pd (
fid varchar(6),
"year" int2,
"month" int2,
v int2 [],
primary key (fid, "year", "month")
);

copy aemet.pd from 'path2\data.csv' with CSV header delimiter ',' encoding 'UTF-8';

select * from aemet.pd;

select fid, year, month, unnest(v) v
from aemet.pd
order by fid, year, month
;


-- select for the case that the months have an array of data of length equal to the days of the month
with v as (
select fid, year, month, unnest(v) v
from pd
order by fid, year, month
),
x as (
select v.fid, 
    concat(v.year, '-', to_char(v.month, 'fm00'), '-', to_char( row_number() over (partition by (v.fid, v.year, v.month)), 'fm00')) sfecha,
    v.v
from v 
order by v.fid, v.year, v.month
)
select x.fid, to_date(x.sfecha, 'YYYY-MM-DD') fecha, x.v
from x 
where x.v is not null
order by x.fid, fecha
;

-- select for the case that all months have a data array of length 31
with v as (
select fid, year, month, unnest(v) v
from pd
order by fid, year, month
),
x as (
select v.fid, 
    case when v is null
    then 
        null
    else
        concat(v.year, '-', to_char(v.month, 'fm00'), '-', to_char( row_number() over (partition by (v.fid, v.year, v.month)), 'fm00'))
    end fecha
    ,v.v
from v 
)
select x.fid, to_date(x.fecha, 'YYYY-MM-DD') fecha, x.v
from x 
where x.v is not null
order by x.fid, x.fecha
;




