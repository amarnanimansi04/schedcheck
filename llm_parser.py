from src.llm_interface import parse_constraints

text = """
We have 12 nurses. Each can work up to 8 hours.
Morning needs 4 nurses, evening needs 4, night needs 2.
"""

parsed = parse_constraints(text)
print(parsed)