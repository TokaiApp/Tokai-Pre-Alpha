import { Router } from "express";
import Anthropic from "@anthropic-ai/sdk";

const router = Router();

let client: Anthropic | null = null;
if (process.env.ANTHROPIC_API_KEY) {
  client = new Anthropic();
}

router.post("/chat", async (req, res) => {
  try {
    const { messages, neuralState, moodAssessment } = req.body as {
      messages: { role: "user" | "assistant"; content: string }[];
      neuralState: { focusIndex: number; bioEnergy: number; neuralNoise: number; abRatio: number };
      moodAssessment?: { mood: string; energy: string; stress: string; suggestion: string };
    };

    if (!client) {
      res.json({
        content:
          "ANTHROPIC_API_KEY is not configured. Set it in your environment to enable LUNA's cognitive recommendations.",
      });
      return;
    }

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

Task planning guidelines based on cognitive state:
- Focus HIGH (>70): Suggest tackling the hardest, most cognitively demanding tasks first
- Focus MODERATE (40-70): Suggest structured tasks, planning, communication, reviewing
- Focus LOW (<40): Suggest easy wins, breaks, physical movement, or administrative tasks

Your behavior:
- Help the user decide what to add to their to-do list and in what order to tackle it
- Ask what they need to get done today if they haven't said
- Recommend task sequencing based on their brain data
- Keep responses concise — 2-4 sentences unless the user asks for more detail
- Be direct and actionable
- Use a calm, focused tone
- Do not use emojis${moodAssessment ? `

Mood check-in (AI vision scan of user's selfie taken at session start):
- Apparent mood: ${moodAssessment.mood}
- Apparent energy: ${moodAssessment.energy}
- Apparent stress: ${moodAssessment.stress}
- Recommendation: ${moodAssessment.suggestion}` : ""}`;

    const response = await client.messages.create({
      model: "claude-sonnet-4-6",
      max_tokens: 512,
      system,
      messages,
    });

    const block = response.content[0];
    if (block.type !== "text") throw new Error("Unexpected content type");

    res.json({ content: block.text });
  } catch (err) {
    console.error("Chat route error:", err);
    res.status(500).json({ content: "Neural link failure. Please retry." });
  }
});

router.post("/mood-check", async (req, res) => {
  try {
    const { imageBase64, mimeType = "image/jpeg", userApiKey } = req.body as {
      imageBase64: string;
      mimeType?: "image/jpeg" | "image/png" | "image/webp";
      userApiKey?: string;
    };

    const anthropic = client ?? (userApiKey ? new Anthropic({ apiKey: userApiKey }) : null);
    if (!anthropic) {
      res.status(503).json({ error: "No API key configured." });
      return;
    }

    const response = await anthropic.messages.create({
      model: "claude-sonnet-4-6",
      max_tokens: 256,
      system: `You are a wellness assistant in Tokai, a productivity app for people with ADHD.
Analyze the person's apparent emotional and energy state from their selfie.
Reply ONLY with a valid JSON object — no prose, no markdown fences — in this exact shape:
{"mood":"positive","energy":"high","stress":"calm","suggestion":"one short actionable sentence"}
Valid values: mood = positive|neutral|low, energy = high|moderate|low, stress = calm|mild|elevated`,
      messages: [
        {
          role: "user",
          content: [
            {
              type: "image",
              source: {
                type: "base64",
                media_type: mimeType as "image/jpeg" | "image/png" | "image/webp",
                data: imageBase64,
              },
            },
            { type: "text", text: "Here is my selfie. Please assess my state." },
          ],
        },
      ],
    });

    const block = response.content[0];
    if (block.type !== "text") throw new Error("Unexpected content type");
    const assessment = JSON.parse(block.text);
    res.json(assessment);
  } catch (err) {
    console.error("Mood check error:", err);
    res.status(500).json({ error: "Mood check failed." });
  }
});

export default router;
