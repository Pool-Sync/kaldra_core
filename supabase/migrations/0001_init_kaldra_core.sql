-- 0001_init_kaldra_core.sql
-- Schema inicial do KALDRA Dashboard no Supabase

-- 1) Tabela de perfis básicos (usuários, orgs, etc.)
create table if not exists public.profiles (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz default now(),
  email text,
  display_name text,
  role text,              -- ex: "admin", "viewer", "beta"
  notes text
);

-- 2) Tabela principal de sinais agregados (vista "pronta pra dashboard")
create table if not exists public.signals (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz default now(),

  -- Domínio do sinal (alpha, geo, product, safeguard)
  domain text not null,

  -- Identidade narrativa
  title text not null,
  summary text,
  source_anchor text,         -- ex: "nyt", "twitter", "bloomberg"
  source_url text,

  -- Núcleo KALDRA
  delta144_state text,        -- ex: "threshold", "eruption"
  dominant_archetype text,    -- ex: "hero", "rebel"
  dominant_polarity text,     -- ex: "order", "chaos"
  tw_regime text,             -- ex: "STABLE", "CRITICAL"
  journey_stage text,         -- ex: "call_to_adventure"

  -- Métricas
  importance numeric,         -- 0–1 ou 0–100
  confidence numeric,         -- 0–1 (explicabilidade)
  divergence numeric,         -- 0–1 (multi-stream divergence)

  -- Payload bruto para futuras análises
  raw_payload jsonb
);

-- 3) Eventos narrativos por sinal (opcional, mas útil)
create table if not exists public.story_events (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz default now(),

  signal_id uuid references public.signals(id) on delete cascade,

  stream_id text,             -- "nyt", "twitter", etc.
  text text,

  delta144_state text,
  polarities jsonb,           -- {"order": 0.7, "chaos": 0.3}
  meta jsonb
);

-- 4) Índices simples de performance
create index if not exists idx_signals_domain_created
  on public.signals(domain, created_at desc);

create index if not exists idx_signals_delta144_state
  on public.signals(delta144_state);

create index if not exists idx_story_events_signal_id
  on public.story_events(signal_id);
