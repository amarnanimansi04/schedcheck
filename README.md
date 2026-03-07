# SchedCheck

SchedCheck converts natural language scheduling descriptions into optimized, constraint-based schedules. Describe your staffing problem in plain English — the system extracts constraints, validates them, and generates a feasible schedule automatically.

Built with Google OR-Tools CP-SAT, Groq LLM, and Streamlit.

---

## What it does

You write this:

> "We have 4 workers. There are 3 shifts: morning, evening, night. Each shift needs 1 worker."

SchedCheck produces this:

| Shift   | Assigned Worker |
|---------|----------------|
| Morning | Worker 0       |
| Evening | Worker 2       |
| Night   | Worker 1       |

**Utilization: 75%** — 3 of 4 workers assigned, 1 unassigned (mathematically correct given 3 shifts).

If a schedule is impossible, the system explains why rather than silently failing.

---

## Motivation

Scheduling problems are everywhere — hospital staffing, retail shifts, warehouse operations. Formulating these as optimization problems traditionally requires manual constraint modeling, which is inaccessible to most users.

SchedCheck explores whether a language model can bridge that gap: translating natural language descriptions into structured constraint models, making scheduling tools usable without technical expertise.

---

## Architecture
```
Natural Language Input
        │
        ▼
Constraint Extraction (Groq LLM)
        │
        ▼
Constraint Validation + Clarification
        │
        ▼
CP-SAT Optimization Model (OR-Tools)
        │
        ▼
Schedule Generation + Feasibility Check
        │
        ▼
Explanation Engine
        │
        ▼
Streamlit Web Interface
```

---

## Project Structure
```
schedcheck/
├── app.py                      # Streamlit frontend
├── Dockerfile
├── requirements.txt
└── src/
    ├── main.py                 # Pipeline orchestration
    ├── solver.py               # OR-Tools CP-SAT model
    ├── llm_interface.py        # Groq LLM constraint extraction
    ├── constraint_handlers.py  # Constraint application logic
    ├── constraint_validator.py # Validation + missing detection
    ├── classifier.py           # Problem type classification
    ├── clarifier.py            # Clarification question generation
    └── explainer.py            # Feasibility explanations
```

---

## Supported Constraint Types

| Constraint | Description |
|---|---|
| `capacity` | Total workers and max shifts per worker |
| `shift_coverage` | How many workers each shift requires |
| `skill_coverage` | Skill-based staffing requirements (senior/junior) |
| `rest_constraint` | Maximum consecutive shifts per worker |

---

## Running Locally
```bash
git clone <repository-url>
cd schedcheck

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file:
```
GROQ_API_KEY=your_api_key_here
```

Run:
```bash
python -m streamlit run app.py
```

---

## Running with Docker
```bash
docker build -t schedcheck .
docker run --env-file .env -p 8501:8501 schedcheck
```

Open `http://localhost:8501`

---

## Tech Stack

| Component | Technology |
|---|---|
| Language Model | Groq API — `llama-3.3-70b-versatile` |
| Solver | Google OR-Tools CP-SAT |
| Frontend | Streamlit |
| Validation | Pydantic |
| Deployment | Docker |

---

## Known Limitations

- Scheduling is single-day only
- Worker preferences are not modeled
- Shift times are not used in the optimization (only shift names and coverage counts)

---

## Planned Improvements

- Multi-day scheduling
- Fair workload distribution across workers
- Worker preference modeling
- Schedule visualization

---

## Author

Mansi  