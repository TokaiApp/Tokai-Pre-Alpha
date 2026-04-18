# Workspace

## Overview

pnpm workspace monorepo using TypeScript. Each package manages its own dependencies.

## Stack

- **Monorepo tool**: pnpm workspaces
- **Node.js version**: 24
- **Package manager**: pnpm
- **TypeScript version**: 5.9
- **API framework**: Express 5
- **Database**: PostgreSQL + Drizzle ORM
- **Validation**: Zod (`zod/v4`), `drizzle-zod`
- **API codegen**: Orval (from OpenAPI spec)
- **Build**: esbuild (CJS bundle)

## Key Commands

- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- `pnpm --filter @workspace/api-server run dev` — run API server locally

See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details.

## Artifacts

### Tokai — Neuro Dashboard (`artifacts/tokai/`)
- **Type**: Streamlit (Python) web application
- **Port**: 20318 (artifact), served at `/`
- **Stack**: Python, Streamlit, Plotly, Pandas, NumPy
- **Entry point**: `artifacts/tokai/app.py`
- **Config**: `artifacts/tokai/.streamlit/config.toml`
- **Workflow**: `artifacts/tokai: web`
- **Features**:
  - Simulated EEG Focus Index (Alpha/Beta wave ratios)
  - Real-time Plotly line chart
  - Optimal Focus Window Predictor (bio-energy based)
  - Task/Todo list integration
  - LUNA AI insights panel
  - Dark mode cyber-medical theme

### API Server (`artifacts/api-server/`)
- Express 5 + TypeScript backend at `/api`
- Health check endpoint: `/api/healthz`
