select 
    "fd" as "id",
    "fd_url" as "url",
    "n" as "number_of_nights",
    "dt" as "departure_date",
    "d" as "departs_from",
    "e" as "ends_at",
    "ls" as "cruise_line_ship",
    "r" as "ship_rating",
    "br" as "normal_price",
    "our" as "current_price",
    "p" as "percentage_off",
    "st" as "status",
    "region" as "region"
from {{ source('postgres', 'deals') }}