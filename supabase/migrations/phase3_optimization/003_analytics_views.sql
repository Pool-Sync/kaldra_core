-- Migration: Create materialized views for analytics
-- Phase: 3.3 - Database Optimization
-- Date: 2025-12-06

-- ==============================================
-- SIGNALS ANALYTICS VIEWS
-- ==============================================

-- View 1: Signals by Day
-- Aggregates signal count and importance by day and domain
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_signals_by_day AS
SELECT 
    date_trunc('day', created_at) as day,
    domain,
    COUNT(*) as signal_count,
    AVG(importance) as avg_importance,
    MAX(importance) as max_importance,
    MIN(importance) as min_importance
FROM signals
GROUP BY date_trunc('day', created_at), domain
ORDER BY day DESC, domain;

-- Index for fast lookups
CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_signals_by_day 
ON mv_signals_by_day (day DESC, domain);

-- View 2: Delta144 State Distribution
-- Shows distribution of Delta144 states
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_delta144_distribution AS
SELECT 
    raw_payload->>'delta144_state' as delta144_state,
    domain,
    COUNT(*) as count,
    AVG(importance) as avg_importance
FROM signals
WHERE raw_payload->>'delta144_state' IS NOT NULL
GROUP BY raw_payload->>'delta144_state', domain
ORDER BY count DESC;

-- Index for fast lookups
CREATE INDEX IF NOT EXISTS idx_mv_delta144_dist 
ON mv_delta144_distribution (delta144_state, domain);

-- View 3: TW Regime Distribution
-- Shows distribution of TW369 regimes
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_tw_regime_distribution AS
SELECT 
    raw_payload->>'tw_regime' as tw_regime,
    domain,
    COUNT(*) as count,
    AVG(importance) as avg_importance
FROM signals
WHERE raw_payload->>'tw_regime' IS NOT NULL
GROUP BY raw_payload->>'tw_regime', domain
ORDER BY count DESC;

-- Index for fast lookups
CREATE INDEX IF NOT EXISTS idx_mv_tw_regime_dist 
ON mv_tw_regime_distribution (tw_regime, domain);

-- View 4: Hourly Signal Trends
-- Real-time trending of signals per hour
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_signals_hourly AS
SELECT 
    date_trunc('hour', created_at) as hour,
    domain,
    COUNT(*) as signal_count,
    AVG(importance) as avg_importance,
    COUNT(DISTINCT raw_payload->>'delta144_state') as unique_states
FROM signals
GROUP BY date_trunc('hour', created_at), domain
ORDER BY hour DESC;

-- Index for fast time-based queries
CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_signals_hourly 
ON mv_signals_hourly (hour DESC, domain);

-- View 5: Polarity Averages by Time
-- Shows polarity trends over time
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_polarity_trends AS
SELECT 
    date_trunc('day', s.created_at) as day,
    s.domain,
    AVG((se.polarity)::numeric) as avg_polarity,
    COUNT(DISTINCT se.id) as event_count
FROM signals s
LEFT JOIN story_events se ON s.id = se.signal_id
WHERE se.polarity IS NOT NULL
GROUP BY date_trunc('day', s.created_at), s.domain
ORDER BY day DESC;

-- Index for fast lookups
CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_polarity_trends 
ON mv_polarity_trends (day DESC, domain);

-- View 6: Kindra Radar Aggregate
-- Aggregates Kindra layer scores
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_kindra_aggregate AS
SELECT 
    domain,
    date_trunc('day', created_at) as day,
    raw_payload->'kindra_l1_scores' as l1_scores,
    raw_payload->'kindra_l2_scores' as l2_scores,
    raw_payload->'kindra_l3_scores' as l3_scores,
    COUNT(*) as signal_count
FROM signals
WHERE raw_payload ? 'kindra_l1_scores'
GROUP BY domain, date_trunc('day', created_at), 
         raw_payload->'kindra_l1_scores',
         raw_payload->'kindra_l2_scores',
         raw_payload->'kindra_l3_scores'
ORDER BY day DESC;

-- Index for fast lookups
CREATE INDEX IF NOT EXISTS idx_mv_kindra_agg 
ON mv_kindra_aggregate (day DESC, domain);

-- ==============================================
-- STORY EVENTS ANALYTICS VIEWS
-- ==============================================

-- View 7: Story Events by Stream
-- Aggregates events by narrative stream
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_story_events_by_stream AS
SELECT 
    stream_id,
    COUNT(*) as event_count,
    AVG((polarity)::numeric) as avg_polarity,
    MIN(created_at) as first_event,
    MAX(created_at) as last_event,
    COUNT(DISTINCT event_state) as unique_states
FROM story_events
WHERE stream_id IS NOT NULL
GROUP BY stream_id
ORDER BY event_count DESC;

-- Index for fast lookups
CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_events_by_stream 
ON mv_story_events_by_stream (stream_id);

-- ==============================================
-- REFRESH FUNCTIONS
-- ==============================================

-- Function to refresh all materialized views
CREATE OR REPLACE FUNCTION refresh_all_analytics_views()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_signals_by_day;
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_delta144_distribution;
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_tw_regime_distribution;
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_signals_hourly;
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_polarity_trends;
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_kindra_aggregate;
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_story_events_by_stream;
    
    RAISE NOTICE 'All analytics views refreshed successfully';
END;
$$ LANGUAGE plpgsql;

-- Function to refresh views on schedule (called by pg_cron or manually)
CREATE OR REPLACE FUNCTION schedule_analytics_refresh()
RETURNS void AS $$
BEGIN
    PERFORM refresh_all_analytics_views();
    RAISE NOTICE 'Scheduled refresh completed at %', NOW();
END;
$$ LANGUAGE plpgsql;

-- ==============================================
-- INITIAL REFRESH
-- ==============================================

-- Refresh all views with data
REFRESH MATERIALIZED VIEW mv_signals_by_day;
REFRESH MATERIALIZED VIEW mv_delta144_distribution;
REFRESH MATERIALIZED VIEW mv_tw_regime_distribution;
REFRESH MATERIALIZED VIEW mv_signals_hourly;
REFRESH MATERIALIZED VIEW mv_polarity_trends;
REFRESH MATERIALIZED VIEW mv_kindra_aggregate;
REFRESH MATERIALIZED VIEW mv_story_events_by_stream;

-- ==============================================
-- VERIFICATION QUERIES
-- ==============================================

-- Check view sizes
SELECT
    schemaname,
    matviewname,
    pg_size_pretty(pg_relation_size(matviewname::regclass)) AS view_size
FROM pg_matviews
WHERE schemaname = 'public'
ORDER BY pg_relation_size(matviewname::regclass) DESC;

-- Sample queries to test views
SELECT * FROM mv_signals_by_day LIMIT 10;
SELECT * FROM mv_delta144_distribution LIMIT 10;
SELECT * FROM mv_tw_regime_distribution LIMIT 10;
SELECT * FROM mv_signals_hourly WHERE hour > NOW() - INTERVAL '24 hours';
