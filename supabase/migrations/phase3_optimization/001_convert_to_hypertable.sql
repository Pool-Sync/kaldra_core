-- Migration: Convert tables to TimescaleDB hypertables
-- Phase: 3.1 - Database Optimization
-- Date: 2025-12-06

-- Enable TimescaleDB extension if not already enabled
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- Convert signals table to hypertable
-- Partitions by created_at timestamp for efficient time-series queries
SELECT create_hypertable(
    'signals',
    'created_at',
    if_not_exists => TRUE,
    chunk_time_interval => INTERVAL '1 day'
);

-- Convert story_events table to hypertable
SELECT create_hypertable(
    'story_events',
    'created_at',
    if_not_exists => TRUE,
    chunk_time_interval => INTERVAL '1 day'
);

-- Add retention policy (optional - keeps data for 1 year)
-- Automatically drops chunks older than 1 year
SELECT add_retention_policy(
    'signals',
    INTERVAL '1 year',
    if_not_exists => TRUE
);

SELECT add_retention_policy(
    'story_events',
    INTERVAL '1 year',
    if_not_exists => TRUE
);

-- Add compression policy for older data (optional)
-- Compresses chunks older than 7 days for storage efficiency
ALTER TABLE signals SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'domain',
    timescaledb.compress_orderby = 'created_at DESC'
);

ALTER TABLE story_events SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'stream_id',
    timescaledb.compress_orderby = 'created_at DESC'
);

SELECT add_compression_policy(
    'signals',
    INTERVAL '7 days',
    if_not_exists => TRUE
);

SELECT add_compression_policy(
    'story_events',
    INTERVAL '7 days',
    if_not_exists => TRUE
);

-- Create continuous aggregates for real-time analytics (optional)
-- This pre-computes aggregations for fast queries
CREATE MATERIALIZED VIEW IF NOT EXISTS signals_hourly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', created_at) AS hour,
    domain,
    COUNT(*) as signal_count,
    AVG(importance) as avg_importance
FROM signals
GROUP BY hour, domain
WITH NO DATA;

-- Refresh policy for continuous aggregate
SELECT add_continuous_aggregate_policy(
    'signals_hourly',
    start_offset => INTERVAL '3 hours',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour',
    if_not_exists => TRUE
);

-- Verification queries
-- Check hypertable status
SELECT * FROM timescaledb_information.hypertables 
WHERE hypertable_name IN ('signals', 'story_events');

-- Check retention policies
SELECT * FROM timescaledb_information.jobs 
WHERE proc_name = 'policy_retention';

-- Check compression policies
SELECT * FROM timescaledb_information.jobs 
WHERE proc_name = 'policy_compression';
