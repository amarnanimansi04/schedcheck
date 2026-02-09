import os
import json
from groq import Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])

SYSTEM_PROMPT = """
You convert scheduling descriptions into STRICT JSON.
If the text mentions number of workers and max hours, ALWAYS create a capacity constraint.
Example:

Input:
"We have 12 nurses. Each works 8 hours."

Output:
{
 "constraints":[
  {"type":"capacity","params":{"resource_count":12,"max_per_resource":8}}
 ]
}

Allowed constraint types and exact schema:

capacity:
{
  "type": "capacity",
  "params": {
    "resource_count": int,
    "max_per_resource": int
  }
}

shift_coverage:
{
  "type": "shift_coverage",
  "params": {
    "shifts": {"morning": int, "evening": int, "night": int},
    "shift_length": int
  }
}

skill_coverage:
{
  "type": "skill_coverage",
  "params": {
    "shifts": {"shift_name": {"skill": int}},
    "shift_length": int,
    "available": {"skill": int}
  }
}

time_overlap:
{
  "type": "time_overlap",
  "params": {
    "shifts": [{"name": str, "start": int, "end": int}],
    "max_workers": {"shift_name": int},
    "total_workers": int
  }
}

Return ONLY JSON:

{
  "constraints": [...]
}

DO NOT invent new parameter names.
Use EXACT keys from schema.
"""

def parse_constraints(text: str) -> dict:
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
    )

    content = resp.choices[0].message.content.strip()

    # Basic safety: ensure it's JSON
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Retry once with stronger instruction
        retry_prompt = SYSTEM_PROMPT + "\nRemember: OUTPUT ONLY VALID JSON."
        resp2 = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            temperature=0,
            messages=[
                {"role": "system", "content": retry_prompt},
                {"role": "user", "content": text},
            ],
        )
        return json.loads(resp2.choices[0].message.content.strip())