# SchedCheck

SchedCheck converts natural language scheduling descriptions into optimized workforce schedules using constraint programming.

Describe your staffing problem in plain English. The system extracts constraints, validates them, and generates a feasible schedule automatically — no manual modeling required.

---

## Demo

Input:

> "We have 4 workers. There are 3 shifts: morning, evening, night. Each shift needs 1 worker."

Output:

| Shift   | Assigned Worker |
|---------|----------------|
| Morning | Worker 0       |
| Evening | Worker 2       |
| Night   | Worker 1       |

**Utilization: 75%** — 3 of 4 workers assigned, 1 unassigned (correct given 3 shifts).

If a schedule is infeasible, the system explains the conflict rather than silently failing.

---

## Motivation

Scheduling problems appear in many real-world settings such as hospital staffing, workforce shift planning, warehouse operations, and academic timetabling.

These schedules are often created manually using spreadsheets, making it difficult to balance worker distribution and satisfy constraints like shift coverage or rest requirements.

SchedCheck explores whether natural-language descriptions can be translated into structured constraint optimization models that automatically generate feasible schedules.

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
├── README.md
└── src/
    ├── main.py                 # Pipeline orchestration
    ├── solver.py               # OR-Tools CP-SAT model
    ├── schema.py               # Data models
    ├── validation.py           # Pydantic validation schemas
    ├── llm_interface.py        # Groq LLM constraint extraction
    ├── llm_mock.py             # Mock LLM for testing
    ├── llm_parser.py           # LLM response parsing
    ├── constraint_handlers.py  # Constraint application logic
    ├── constraint_validator.py # Validation and missing detection
    ├── classifier.py           # Problem type classification
    ├── clarifier.py            # Clarification question generation
    ├── explainer.py            # Feasibility explanations
    └── verifier.py             # Schedule verification
```

---

## Supported Constraint Types

| Constraint | Description |
|---|---|
| `capacity` | Total workers and max shifts per worker |
| `shift_coverage` | Workers required per shift |
| `skill_coverage` | Skill-based staffing (e.g. senior/junior) |
| `rest_constraint` | Maximum consecutive shifts per worker |

---

## Tech Stack

| Component | Technology |
|---|---|
| Constraint Solver | Google OR-Tools CP-SAT |
| Language Model | Groq API — LLaMA 3.3 70B |
| Backend | Python |
| Validation | Pydantic |
| Frontend | Streamlit |
| Containerization | Docker |

---

## Running Locally
```bash
git clone <repository-url>
cd schedcheck

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_api_key_here
```

Start the app:
```bash
python -m streamlit run app.py
```

Open `http://localhost:8501`

---

## Running with Docker
```bash
docker build -t schedcheck .
docker run --env-file .env -p 8501:8501 schedcheck
```

Open `http://localhost:8501`

---

## Known Limitations

- Single-day scheduling only
- Shift durations are extracted but not used in the optimization model
- Worker preferences are not modeled

---

## Roadmap

- Multi-day scheduling
- Worker preference modeling
- Fair workload distribution
- Schedule visualization dashboard
- Additional constraint types

---

## License

MIT

---

## Author

Mansi  
