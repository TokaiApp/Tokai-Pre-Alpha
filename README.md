<div align="center">
  <img src="artifacts/tokai/public/tokai_logo.png" alt="Tokai Logo" width="120" />

  <h1>
    <span>TOK</span><span>AI</span>
  </h1>

  <p><strong>Neurosupportive Productivity · ADHD Management · Real-Time EEG Dashboard</strong></p>
  <p><strong>神經支持型生產力 · ADHD 管理 · 即時 EEG 儀表板</strong></p>

  <p>
    <a href="https://tokai-pre-alpha-tokai.vercel.app/"><img src="https://img.shields.io/badge/Live%20Demo-Pre--Alpha-c084fc?style=flat-square&logo=vercel" alt="Live Demo" /></a>
    <a href="https://tokai.app"><img src="https://img.shields.io/badge/Website-tokai.app-7c3aed?style=flat-square" alt="Website" /></a>
    <a href="https://github.com/TokaiApp/Tokai-Pre-Alpha/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-blue?style=flat-square" alt="License" /></a>
    <img src="https://img.shields.io/badge/Status-Pre--Alpha-f472b6?style=flat-square" alt="Status" />
    <img src="https://img.shields.io/badge/AI-Claude%20(Anthropic)-orange?style=flat-square" alt="AI" />
  </p>

  <p>
    <a href="https://tokai-pre-alpha-tokai.vercel.app/">Try it live →</a>
  </p>
</div>

---

## Overview 概述

**Tokai** is an open-source neurosupportive productivity application built for neurodivergent brains — especially people with ADHD. It provides a real-time neural dashboard that reads your cognitive state and helps you plan your day around how your brain is *actually* performing, not how you wish it were.

**Tokai** 是一款專為神經多樣性大腦（尤其是 ADHD 患者）打造的開源、神經支持型生產力應用程式。它提供即時神經數據儀表板，能讀取您的認知狀態，並協助您根據大腦的「實際」表現來規劃一天，而非盲目硬撐。

> To the best of our knowledge, **Tokai is the first app in the world** to propose an AI task planner and agentic to-do list — TokAgent and TokTodo — driven by the user's own brain data.
>
> 據我們所知，**Tokai 是全球首款**提議根據使用者大腦數據來驅動 AI 任務規劃器與代理型待辦清單（TokAgent 與 TokTodo）的應用程式。

Neural data is **simulated** in this pre-alpha release. Integration with [Muse 2](https://choosemuse.com/) and other consumer EEG headsets is planned for future versions.

目前的 Pre-Alpha 版本中，神經數據為**模擬狀態**。計劃在未來版本中整合 [Muse 2](https://choosemuse.com/) 及其他消費級 EEG 設備。

---

## Features 核心功能

| | English | 中文 |
|---|---|---|
| 🧠 | **Real-time neural dashboard** — visualizes EEG and biometric data in a cyberpunk-style interface | **即時神經儀表板** — 在賽博朋克風介面中將 EEG 與生物識別數據具現化 |
| 🤖 | **TokAgent** — AI assistant powered by Claude. Reads your brain data and helps you build and prioritize your to-do list based on your current cognitive state | **TokAgent** — 由 Claude 驅動的 AI 助手，讀取腦部數據並依認知狀態協助建立與排序待辦事項 |
| 📝 | **TokTodo** — manage tasks directly alongside your live neural metrics | **TokTodo** — 直接在即時神經指標旁管理各項任務 |
| 📊 | **Focus Stream** — real-time line chart tracking your focus index over time | **專注串流** — 即時追蹤專注指數變化的折線圖 |
| 🌊 | **Neural Insights** — adaptive text recommendations based on your current focus, energy, and noise levels | **神經洞察** — 依據當前專注度、能量與噪訊水平生成的自適應建議 |
| 🀄 | **Bilingual** — full English and Traditional Chinese support | **雙語支援** — 完整支援英文與繁體中文 |
| 📱 | **Responsive** — works on desktop and mobile | **響應式設計** — 支援桌機與行動裝置 |

---

## Live Demo 立即體驗

**[https://tokai-pre-alpha-tokai.vercel.app/](https://tokai-pre-alpha-tokai.vercel.app/)**

> **TokAgent requires your own Anthropic API key.** You can get one free at [console.anthropic.com](https://console.anthropic.com). Your key is stored locally in your browser and never saved on our servers.
>
> **TokAgent 需要您自備 Anthropic API 金鑰**，可至 [console.anthropic.com](https://console.anthropic.com) 免費獲取。金鑰僅儲存在您的瀏覽器本機，不會被我們的伺服器儲存。

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, TypeScript, Vite |
| Charts | Recharts |
| Icons | Lucide React |
| Fonts | Share Tech Mono, Rajdhani, Inter (Google Fonts) |
| AI | [Anthropic Claude](https://anthropic.com) (`claude-sonnet-4-5`) |
| API Server | Node.js, Express 5 |
| Monorepo | pnpm workspaces |
| Deployment | Vercel (frontend + serverless API) |

---

## Architecture

```
Tokai-Pre-Alpha/
├── artifacts/
│   ├── tokai/                  # React/Vite frontend
│   │   ├── src/
│   │   │   ├── pages/
│   │   │   │   └── dashboard.tsx   # Main dashboard
│   │   │   └── components/
│   │   │       └── agent-chat.tsx  # TokAgent chat UI
│   │   ├── public/
│   │   │   └── tokai_logo.png
│   │   └── vite.config.ts
│   └── api-server/             # Express.js API (serverless on Vercel)
│       └── api/
│           └── index.js        # /api/chat endpoint
├── pnpm-workspace.yaml
└── README.md
```

The frontend proxies `/api` requests to the API server in development. In production, `VITE_API_BASE_URL` points to the deployed Vercel serverless function.

---

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) v18+
- [pnpm](https://pnpm.io/) v10+
- An [Anthropic API key](https://console.anthropic.com) (for TokAgent)

### 1. Clone the repository

```bash
git clone https://github.com/TokaiApp/Tokai-Pre-Alpha.git
cd Tokai-Pre-Alpha
```

### 2. Install dependencies

```bash
pnpm install
```

### 3. Configure environment variables

**Frontend** — create `artifacts/tokai/.env.local`:
```env
# Leave empty for local dev (Vite proxy handles /api routing)
VITE_API_BASE_URL=
```

**API server** — create `artifacts/api-server/.env`:
```env
# Optional fallback if users don't provide their own key
ANTHROPIC_API_KEY=sk-ant-...
```

### 4. Run the development servers

In two separate terminals:

```bash
# Terminal 1 — API server (port 3000)
PORT=3000 pnpm --filter @workspace/api-server dev

# Terminal 2 — Frontend (port 5173)
pnpm --filter @workspace/tokai dev
```

Open [http://localhost:5173](http://localhost:5173).

---

## Deployment

The project deploys as two separate Vercel projects.

### Frontend (`artifacts/tokai/`)

1. Import `artifacts/tokai/` as a Vercel project
2. Framework preset: **Vite**
3. Add environment variable: `VITE_API_BASE_URL` → your API server URL (e.g. `https://your-api.vercel.app`)

### API Server (`artifacts/api-server/`)

1. Import `artifacts/api-server/` as a separate Vercel project
2. No framework preset needed — the `vercel.json` configures it as a serverless function
3. Optionally add `ANTHROPIC_API_KEY` as a fallback (users can also provide their own key in the UI)

---

## Neural Metrics Explained

| Metric | Description |
|---|---|
| **Focus Index** | Composite score (0–100) derived from EEG alpha/beta wave patterns |
| **Bio Energy** | Simulated biological energy level (%) — will reflect HRV and other signals in future versions |
| **Neural Noise** | Background EEG signal noise in μV² — lower is cleaner |
| **A/B Wave Ratio** | Alpha-to-beta wave ratio; higher values correlate with relaxed alertness |
| **Focus Window** | Predicted time remaining in your current focus state |
| **Wave Breakdown** | Visual comparison of raw alpha and beta wave power |

TokAgent uses these values in its system prompt to tailor task planning recommendations:
- **High focus (>70):** deep work, complex problem-solving
- **Moderate focus (40–70):** structured tasks, planning, communication
- **Low focus (<40):** easy wins, breaks, administrative tasks

---

## Roadmap

- [ ] **Real EEG integration** — Muse 2, OpenBCI, Neurosity
- [ ] **User accounts** — persistent sessions, task history, focus analytics
- [ ] **ADHD-specific profiles** — personalized thresholds and recommendations
- [ ] **Mobile app** — native iOS/Android with EEG Bluetooth pairing
- [ ] **HRV and biometric integration** — Apple Watch, Fitbit, Garmin
- [ ] **Focus session analytics** — daily/weekly cognitive performance reports
- [ ] **Team/classroom mode** — aggregate anonymous neural state for collaborative environments
- [ ] **LUNA integration** — binary classification model for ADHD detection (research phase)

---

## Research Context

Tokai originated as a master's degree thesis project exploring the intersection of real-time neurofeedback, agentic AI, and ADHD management. The core hypothesis: **if an AI assistant has access to a user's live cognitive state, it can dramatically improve task planning outcomes for people with executive function challenges.**

This repository represents the first public prototype. We are actively seeking collaborators, researchers, and neurodivergent users willing to provide feedback.

---

## Contributing

We welcome contributions — especially from people with ADHD or neurodiversity research backgrounds.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes
4. Open a pull request

For significant changes, please open an issue first to discuss the approach.

**Feedback and bug reports:** [GitHub Issues](https://github.com/TokaiApp/Tokai-Pre-Alpha/issues)

We especially want to hear from people who have tried the app. If you have ADHD, your experience matters most — this is built for you.
我們特別期待 ADHD 使用者的回饋，這款產品正是為你們而打造的。

---

## About 關於

**Tokai — Theory of Knowledge, Amplified Intelligence.**
**Tokai — 知識理論，增強智能。**

Learn more about the project and team at **[tokai.app](https://tokai.app)**.

---

## License

Copyright © 2025 TokaiApp

Licensed under the [Apache License, Version 2.0](LICENSE).

You may use, modify, and distribute this software freely under the terms of the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [Anthropic](https://anthropic.com) — Claude AI powering TokAgent
- [Recharts](https://recharts.org) — charting library
- [Lucide](https://lucide.dev) — icons
- The ADHD and neurodiversity community — for inspiring this work
