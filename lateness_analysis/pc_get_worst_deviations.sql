-- get percentile score 
CREATE OR REPLACE TEMP TABLE _percentile AS 
SELECT 
percentile_cont(0.75) within group (order by DELIVERY_DEVIATION_SCORE_SUM_L50_TBPM_max NULLS FIRST) sum_l50_75_perc
FROM (
SELECT dasher_id, max(DELIVERY_DEVIATION_SCORE_sum_L50_TBPM) AS DELIVERY_DEVIATION_SCORE_SUM_L50_TBPM_max
, percent_rank() over(ORDER BY DELIVERY_DEVIATION_SCORE_SUM_L50_TBPM_max)
FROM proddb.PUBLIC.fact_dx_fraud_pc_rolling_scores a
WHERE timebased_pay_model NOT IN ('order mode')
AND a.assignment_created_at >= dateadd(dd,-28,current_date())
GROUP BY 1
)
;



-- get the latest delivery where dasher met the percentile 
CREATE OR REPLACE TEMP TABLE _threshold_met AS 
SELECT 
a.dasher_id 
, a.delivery_assignment_composite_id 
, a.DELIVERY_DEVIATION_SCORE_sum_L50_TBPM
, a.assignment_created_at 
FROM proddb.PUBLIC.fact_dx_fraud_pc_rolling_scores a
JOIN _percentile b 
WHERE timebased_pay_model NOT IN ('order mode')
AND a.assignment_created_at >= dateadd(dd,-28,current_date())
AND a.DELIVERY_DEVIATION_SCORE_sum_L50_TBPM > b.sum_l50_75_perc
QUALIFY ROW_NUMBER() over(PARTITION BY dasher_id ORDER BY assignment_created_at DESC) = 1
;


-- get the 50 deliveries that contributed to the score 
SELECT a.dasher_id 
, a.DELIVERY_DEVIATION_SCORE_sum_L50_TBPM AS score
, a.assignment_created_at AS threshold_met_timestamp
, b.DELIVERY_ASSIGNMENT_COMPOSITE_ID,b.ASSIGNMENT_CREATED_AT,b.DELIVERY_ID,b.TIMEBASED_PAY_MODEL
, b.DELIVERY_DEVIATION_SCORE
, row_number() over(PARTITION BY a.dasher_id ORDER BY b.assignment_created_at DESC) AS L50_delivery_index
FROM _threshold_met a 
LEFT JOIN proddb.PUBLIC.fact_dx_fraud_pc_rolling_scores b 
	ON a.dasher_id = b.dasher_id 
	AND b.assignment_created_at < a.assignment_created_at
QUALIFY L50_delivery_index <= 50 
ORDER BY a.dasher_id, L50_delivery_index