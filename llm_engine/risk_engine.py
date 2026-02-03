import openai
from typing import List, Tuple
import os
from dotenv import load_dotenv

load_dotenv()  # .env yükle


class LLMRiskEngine:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def analyze(self, logs: List[dict]) -> Tuple[int, str]:
        log_text = "\n".join(
            [f"{log['timestamp']} - {log['source_ip']} - {log['event_type']} ({'OK' if log['success'] else 'FAILED'})"
             for log in logs[-10:]])

        prompt = f"""
        Analyze DID verification logs for anomalies:

        {log_text}

        Rules: Multiple FAILED = HIGH RISK, Different IPs = HIGH RISK
        Return ONLY: "SCORE, EXPLANATION" (max 20 words)
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=50
            )

            result = response.choices[0].message.content.strip()
            score_str, explanation = result.split(", ", 1)
            return int(score_str), explanation

        except Exception as e:
            failed = sum(1 for log in logs if log["event_type"] == "verification" and not log["success"])
            return 50 if failed >= 2 else 10, f"Fallback: {failed} failed attempts"
