select *
from 
{{ metrics.calculate(metric('base_average_metric'), 
    grain='day', 
    dimensions=['had_discount']) 
}}