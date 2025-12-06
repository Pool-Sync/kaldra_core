-- Migration: Add performance indexes
-- Phase: 3.2 - Database Optimization
-- Date: 2025-12-06

-- ==============================================
-- SIGNALS TABLE INDEXES
-- ==============================================

-- Index on created_at (descending) for recent signals queries
CREATE INDEX IF NOT EXISTS idx_signals_created_at_desc 
ON signals (created_at DESC);

-- Index on domain for filtering by signal source
CREATE INDEX IF NOT EXISTS idx_signals_domain 
ON signals (domain);

-- Composite index for domain + created_at (most common query pattern)
CREATE INDEX IF NOT EXISTS idx_signals_domain_created_at 
ON signals (domain, created_at DESC);

-- Index on importance for sorting/filtering high-priority signals
CREATE INDEX IF NOT EXISTS idx_signals_importance 
ON signals (importance DESC);

-- Indexes on JSON fields (using GIN for JSONB)
-- Delta144 state
CREATE INDEX IF NOT EXISTS idx_signals_delta144_state 
ON signals ((raw_payload->>'delta144_state'));

-- TW regime
CREATE INDEX IF NOT EXISTS idx_signals_tw_regime 
ON signals ((raw_payload->>'tw_regime'));

-- Kindra layer 1
CREATE INDEX IF NOT EXISTS idx_signals_kindra_l1 
ON signals USING GIN ((raw_payload->'kindra_l1_scores'));

-- Composite index for common analytics queries
CREATE INDEX IF NOT EXISTS idx_signals_analytics 
ON signals (domain, created_at DESC, importance DESC);

-- ==============================================
-- STORY_EVENTS TABLE INDEXES
-- ==============================================

-- Index on signal_id for joining with signals
CREATE INDEX IF NOT EXISTS idx_story_events_signal_id 
ON story_events (signal_id);

-- Index on stream_id for filtering by narrative stream
CREATE INDEX IF NOT EXISTS idx_story_events_stream_id 
ON story_events (stream_id);

-- Index on created_at (descending) for recent events
CREATE INDEX IF NOT EXISTS idx_story_events_created_at_desc 
ON story_events (created_at DESC);

-- Composite index for signal + created_at (timeline queries)
CREATE INDEX IF NOT EXISTS idx_story_events_signal_timeline 
ON story_events (signal_id, created_at DESC);

-- Composite index for stream + created_at
CREATE INDEX IF NOT EXISTS idx_story_events_stream_timeline 
ON story_events (stream_id, created_at DESC);

-- Index on polarity for polarity-based queries
CREATE INDEX IF NOT EXISTS idx_story_events_polarity 
ON story_events (polarity);

-- Index on event_state for filtering by narrative state
CREATE INDEX IF NOT EXISTS idx_story_events_state 
ON story_events (event_state);

-- Full-text search on event text (if needed)
-- Uncomment if text search is required
-- CREATE INDEX IF NOT EXISTS idx_story_events_text_search 
-- ON story_events USING GIN (to_tsvector('english', text));

-- ==============================================
-- VERIFICATION QUERIES
-- ==============================================

-- Check index sizes
SELECT
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
    AND tablename IN ('signals', 'story_events')
ORDER BY pg_relation_size(indexrelid) DESC;

-- Check index usage
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan as times_used,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
    AND tablename IN ('signals', 'story_events')
ORDER BY idx_scan DESC;

-- Analyze tables to update statistics
ANALYZE signals;
ANALYZE story_events;
