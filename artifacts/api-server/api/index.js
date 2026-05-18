const express = require("express");
const cors = require("cors");
const Anthropic = require("@anthropic-ai/sdk").default;

const app = express();
app.use(cors());
app.use(express.json());

// Claude Sonnet 4.5 pricing
const INPUT_COST_PER_TOKEN  = 3.00  / 1_000_000; // $3.00 per million input tokens
const OUTPUT_COST_PER_TOKEN = 15.00 / 1_000_000; // $15.00 per million output tokens
const BUDGET_LIMIT = 0.50; // $ per user (by IP)

function ipKey(req) {
  const ip = (req.headers["x-forwarded-for"] || req.socket.remoteAddress || "unknown")
    .split(",")[0].trim().replace(/[^a-zA-Z0-9._-]/g, "_");
  return `tokai:usage:${ip}`;
}

async function getSpend(key) {
  const url = process.env.UPSTASH_REDIS_REST_URL;
  const token = process.env.UPSTASH_REDIS_REST_TOKEN;
  if (!url) return 0;
  const r = await fetch(`${url}/get/${key}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const data = await r.json();
  return parseFloat(data.result) || 0;
}

async function addSpend(key, amount) {
  const url = process.env.UPSTASH_REDIS_REST_URL;
  const token = process.env.UPSTASH_REDIS_REST_TOKEN;
  if (!url) return;
  await fetch(`${url}/incrbyfloat/${key}/${amount.toFixed(8)}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

app.get("/api/health", (_req, res) => {
  res.json({ status: "ok" });
});

app.post("/api/chat", async (req, res) => {
  try {
    const { messages, neuralState, tasks, lang } = req.body;

    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) {
      res.json({ content: "ANTHROPIC_API_KEY is not configured." });
      return;
    }

    // Check per-user budget
    const key = ipKey(req);
    const spent = await getSpend(key);
    if (spent >= BUDGET_LIMIT) {
      const msg = lang === "zh"
        ? "您已達到本次預覽版的 $0.50 使用額度。感謝體驗 Tokai！"
        : "You've reached the $0.50 usage limit for this pre-alpha. Thanks for trying Tokai!";
      res.json({ content: msg });
      return;
    }

    const client = new Anthropic({ apiKey });
    const { focusIndex, bioEnergy, neuralNoise, abRatio } = neuralState;
    const focusLabel = focusIndex > 70 ? "HIGH" : focusIndex > 40 ? "MODERATE" : "LOW";
    const energyLabel = bioEnergy > 70 ? "high" : bioEnergy > 40 ? "moderate" : "low";
    const noiseLabel = neuralNoise < 20 ? "clean" : neuralNoise < 40 ? "nominal" : "elevated";

    const system = `You are TokAgent, an AI task planning assistant embedded in Tokai — a neurosupportive productivity suite designed for people with ADHD. You use real-time EEG and biological data to help users build and prioritize their to-do list based on their current cognitive state.

Current neural and biological state:
- Focus Index: ${focusIndex.toFixed(1)}/100 (${focusLabel})
- Biological Energy: ${Math.round(bioEnergy)}% (${energyLabel})
- Neural Noise: ${Math.round(neuralNoise)} μV² (${noiseLabel})
- Alpha/Beta Wave Ratio: ${abRatio}

Current TokTodo task list:
${Array.isArray(tasks) && tasks.length > 0
  ? tasks.map(t => `- [${t.done ? "DONE" : "TODO"}] ${t.text}`).join("\n")
  : "- (no tasks added yet)"}

Task planning guidelines based on cognitive state:
- Focus HIGH (>70): Suggest tackling the hardest, most cognitively demanding tasks first
- Focus MODERATE (40-70): Suggest structured tasks, planning, communication, reviewing
- Focus LOW (<40): Suggest easy wins, breaks, physical movement, or administrative tasks

Your behavior:
- You can see the user's current TokTodo task list above — reference it directly when answering questions about their tasks
- Help the user decide what to add to their to-do list and in what order to tackle it
- If the task list is empty, ask what they need to get done today
- Recommend task sequencing based on their brain data and the actual tasks listed
- Keep responses concise — 2-4 sentences unless the user asks for more detail
- Be direct and actionable
- Use a calm, focused tone
- Do not use emojis
${lang === "zh" ? "- Respond in Traditional Chinese (繁體中文)" : "- Respond in English"}`;

    const response = await client.messages.create({
      model: "claude-sonnet-4-5",
      max_tokens: 512,
      system,
      messages,
    });

    const block = response.content[0];
    if (block.type !== "text") throw new Error("Unexpected content type");

    // Track cost from actual token usage
    const cost = response.usage.input_tokens * INPUT_COST_PER_TOKEN
               + response.usage.output_tokens * OUTPUT_COST_PER_TOKEN;
    await addSpend(key, cost);

    res.json({ content: block.text });
  } catch (err) {
    console.error("Chat route error:", err);
    res.status(500).json({ content: "Neural link failure. Please retry." });
  }
});

module.exports = app;
