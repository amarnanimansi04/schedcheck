import os
import json
from groq import Groq
from src.validation import SchedulingProblemModel
from json import JSONDecodeError
from pydantic import ValidationError

client = Groq(api_key=os.environ["GROQ_API_KEY"])

SYSTEM_PROMPT = """
You convert scheduling descriptions into STRICT JSON.

CRITICAL RULES:

1. If the text mentions workers WITHOUT skills:
   → create ONE capacity constraint.
   → If max_per_resource is not mentioned, assume max_per_resource = 1.

2. If the text mentions workers WITH skills (e.g., senior, junior, manager):
   → create ONE skill_coverage constraint.
   → DO NOT create separate capacity constraints for each skill.

3. If shifts require specific skills (e.g., "Morning needs 1 senior and 2 juniors"):
   → use skill_coverage.

4. If shifts only require total workers (e.g., "Morning needs 4 nurses"):
   → use shift_coverage.

5. If the text says workers cannot work too many consecutive shifts
   (e.g., "No worker can work more than 1 consecutive shift")
   → create a rest_constraint.

6. If the text mentions shift times (e.g., "runs from 8 to 12") AND mentions
   total workers:
   → ALWAYS create BOTH a capacity constraint AND a shift_coverage constraint.
   → NEVER skip capacity even when shift times are mentioned.

7. ALWAYS use the exact shift names the user provides as keys in "shifts".
   NEVER default to morning/evening/night unless the user explicitly says those words.
   e.g., "Shift A", "Shift B" → use "shift_a", "shift_b" as keys.   

---

Allowed constraint types and EXACT schema:

capacity:
{
  "type": "capacity",
  "params": {
    "resource_count": int,
    "max_per_resource": int  // If not specified, default to 1
  }
}

shift_coverage:
{
  "type": "shift_coverage",
  "params": {
    "shifts": {"<exact_shift_name_from_user>": int},
    "shift_length": int
  }
}

skill_coverage:
{
  "type": "skill_coverage",
  "params": {
    "shifts": {
      "<exact_shift_name_from_user>": {"<skill_name>": int}
    },
    "shift_length": int,
    "available": {"<skill_name>": int}
  }
}

rest_constraint:
{
  "type": "rest_constraint",
  "params": {
    "max_consecutive": int
  }
}

---

Example:

Input:
"We have 4 senior nurses and 8 junior nurses.
Each works 8 hours.
Morning needs 1 senior and 2 juniors.
Evening needs 1 senior and 2 juniors.
Night needs 1 senior and 2 juniors."

Output:
{
  "constraints": [
    {
      "type": "skill_coverage",
      "params": {
        "available": {"senior": 4, "junior": 8},
        "shift_length": 8,
        "shifts": {
          "morning": {"senior": 1, "junior": 2},
          "evening": {"senior": 1, "junior": 2},
          "night": {"senior": 1, "junior": 2}
        }
      }
    }
  ]
}

Example 2:

Input:
We have 4 workers.
There are 3 shifts: morning, evening, night.
Each shift needs 1 worker.
No worker can work more than 1 consecutive shift.

Output:
{
  "constraints": [
    {
      "type": "capacity",
      "params": {
        "resource_count": 4,
        "max_per_resource": 1
      }
    },
    {
      "type": "shift_coverage",
      "params": {
        "shifts": {
          "morning": 1,
          "evening": 1,
          "night": 1
        },
        "shift_length": 8
      }
    },
    {
      "type": "rest_constraint",
      "params": {
        "max_consecutive": 1
      }
    }
  ]
}

Example 3:

Input:
We have 2 workers.
Shift A runs from 8 to 12.
Shift B runs from 10 to 14.
Each shift needs 1 worker.

Output:
{
  "constraints": [
    {
      "type": "capacity",
      "params": {
        "resource_count": 2,
        "max_per_resource": 1
      }
    },
    {
      "type": "shift_coverage",
      "params": {
        "shifts": {
          "shift_a": 1,
          "shift_b": 1
        },
        "shift_length": 4
      }
    }
  ]
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
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
    )

    content = resp.choices[0].message.content.strip()

    try:
        parsed = json.loads(content)

        validated = SchedulingProblemModel(**parsed)

        return validated.dict()
    except json.JSONDecodeError:
     
        retry_prompt = SYSTEM_PROMPT + "\nRemember: OUTPUT ONLY VALID JSON."
        resp2 = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            temperature=0,
            messages=[
                {"role": "system", "content": retry_prompt},
                {"role": "user", "content": text},
            ],
        )

        content2 = resp2.choices[0].message.content.strip()

        try:
            parsed = json.loads(content2)

            validated = SchedulingProblemModel(**parsed)

            return validated.dict()

        except JSONDecodeError:
            print("❌ LLM did not return valid JSON format.")
            return None

        except ValidationError as e:
            print("❌ LLM returned invalid structured data.")
            print("Details:", e)
            return None