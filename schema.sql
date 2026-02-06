-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- Enable pgvector extension for embeddings
create extension if not exists vector;

-- 1. Users Table
create table public.users (
  id uuid primary key,
  email text unique not null,
  username text unique,
  first_name text,
  last_name text,
  phone_no text,
  gemini_api_key text, -- User-specific Gemini API Key (Encrypted/Stored as text for now)
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 2. PDF Files Table
create table public.pdf_files (
  id uuid default uuid_generate_v4() primary key,
  user_id uuid references public.users(id) on delete cascade not null,
  filename text not null,          -- Unique storage filename (e.g., "uuid_file.pdf")
  original_filename text not null, -- Original user filename
  storage_path text not null,      -- Supabase Storage path
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 3. PDF Chunks (Vector Store)
create table public.pdf_chunks (
  id bigint generated always as identity primary key,
  pdf_id uuid references public.pdf_files(id) on delete cascade not null,
  user_id uuid references public.users(id) on delete cascade not null,
  content text not null,                -- The text chunk content
  embedding vector(768),                -- Gemini text-embedding-004 returns 768 dimensions
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Index for vector similarity search (IVFFlat or HNSW)
-- Using HNSW for better performance/recall balance
create index on public.pdf_chunks using hnsw (embedding vector_cosine_ops);

-- 4. Chat History
create table public.chat_history (
  id uuid default uuid_generate_v4() primary key,
  pdf_id uuid references public.pdf_files(id) on delete cascade not null,
  user_id uuid references public.users(id) on delete cascade not null,
  question text not null,
  answer text not null,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- RPC Function for Similarity Search
-- Usage: supabase.rpc("match_pdf_chunks", { ... })
create or replace function match_pdf_chunks (
  query_embedding vector(768),
  match_pdf_id uuid,
  match_count int DEFAULT 5
) returns table (
  id bigint,
  content text,
  similarity float
)
language plpgsql
as $$
begin
  return query
  select
    pdf_chunks.id,
    pdf_chunks.content,
    1 - (pdf_chunks.embedding <=> query_embedding) as similarity
  from pdf_chunks
  where pdf_chunks.pdf_id = match_pdf_id
  order by pdf_chunks.embedding <=> query_embedding
  limit match_count;
end;
$$;
