// hitting pica but gpt4


import express from "express";
import { openai } from "@ai-sdk/openai";
import { generateText } from "ai";
import { Pica } from "@picahq/ai";
import * as dotenv from "dotenv";
import fetch from "node-fetch"; 

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

app.post("/api/ai", async (req, res) => {
  try {
    const { message } = req.body;

    if (!message) {
      return res.status(400).json({ error: "Missing 'message' in request body" });
    }

    if (!process.env.PICA_SECRET_KEY) {
      throw new Error("Missing PICA_SECRET_KEY in environment variables");
    }

    const pica = new Pica(process.env.PICA_SECRET_KEY);
    const systemPrompt = await pica.generateSystemPrompt();

    const { text } = await generateText({
      model: openai("gpt-4o"),
      system: systemPrompt,
      tools: { ...pica.oneTool },
      prompt: message,
      maxSteps: 5,
    });

    res.setHeader("Content-Type", "application/json");
    res.status(200).json({ text });
  } catch (error) {
    console.error("Error processing AI request:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

app.listen(port, async () => {
  console.log(`Server is running on port ${port}`);

  // creating a new branch in connection github of repository Pica and name new brach as test2
  try {
    const response = await fetch(`http://localhost:${port}/api/ai`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message:
          "create a new branch in connection github of repository Pica and name new brach as test2",
      }),
    });

    const data = await response.json();
    console.log("\n✅ Response from /api/ai:");
    console.log(data);
  } catch (err) {
    console.error(" Error making request:", err);
  }
});

export default app;
