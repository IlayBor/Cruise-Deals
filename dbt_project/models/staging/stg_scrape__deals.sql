with source as (
    select 
        "fd",
        "fd_url",
        "n",
        "dt",
        "d",
        "e",
        "ls",
        "r",
        "br",
        "our",
        "st",
        "region"
    from {{ source('postgres', 'deals') }}
),
renamed as (
    select 
        REPLACE("fd", '#', '') as "id",
        "fd_url" as "url",
        "n"::INT as "number_of_nights",
        CASE 
            WHEN TO_DATE("dt" || ' ' || EXTRACT(YEAR FROM CURRENT_DATE), 'Mon DD YYYY') < CURRENT_DATE
            THEN TO_DATE("dt" || ' ' || EXTRACT(YEAR FROM CURRENT_DATE), 'Mon DD YYYY') + INTERVAL '1 year'
            ELSE TO_DATE("dt" || ' ' || EXTRACT(YEAR FROM CURRENT_DATE), 'Mon DD YYYY')
        END::DATE AS "departure_date",
        split_part("d", ',', 2) as "departs_from_state",
        split_part("d", ',', 1) as "departs_from_city",
        split_part("e", ',', 2) as "ends_at_state",
        split_part("e", ',', 1) as "ends_at_city",
        split_part("ls", '/', 1) as "cruise_line",
        split_part("ls", '/', 2) as "ship",
        "r"::FLOAT as "ship_rating",
        nullif(replace(replace("br", '$', ''), ',', ''), '-')::NUMERIC as "normal_price",
        nullif(replace(replace("our", '$', ''), ',', ''), '-')::NUMERIC as "current_price",
        "st" as "status",
        "region"
    from source
),
calculated as (
    select
        *,
        ("departure_date" + "number_of_nights" * INTERVAL '1 day')::DATE as "end_date",
        ROUND((1 - "current_price" / NULLIF("normal_price", 0)) * 100, 1) as "percentage_off"
    from renamed
)

select *
from calculated
i wan