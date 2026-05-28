# AI Financial Research Copilot

Built this project to properly understand how real AI systems are structured instead of just wrapping an LLM with a UI.

This project started as a simple finance API experiment and slowly became a full async AI backend with orchestration, LangGraph workflows, validation loops, and AI analysis.

---

# What I Learned

## Async Programming Finally Clicked

Before this project, async always felt magical.

While building this, I understood:
- event loops
- coroutines
- `await`
- `asyncio.gather`
- concurrent execution
- why async is mainly about waiting efficiency

One big realization was:

> async is not “make code faster magically”

It’s about handling multiple waiting operations efficiently.

---

## Real APIs Are Messy

I hit:
- rate limits
- invalid responses
- schema mismatches
- response validation errors
- weird API structures

This taught me:
- normalization matters
- services should return clean internal schemas
- external APIs should not leak directly into the system

---

## Backend Architecture Matters A LOT

This was probably the biggest lesson.

I learned how to separate:
- service layer
- orchestration layer
- API layer
- AI reasoning layer

Instead of throwing everything into one file.

---

## LangGraph Makes More Sense Now

Earlier I knew how to use LangGraph.

Now I understand WHY orchestration exists.

Built:
- formatter nodes
- prompt builder nodes
- evaluator/validator loops
- retry logic
- conditional routing

Which made LangGraph feel like an actual workflow engine instead of “just nodes.”

---

## AI Systems Are Mostly Context Engineering

A huge realization from this project:

> LLM calls are usually the easiest part.

The harder part is:
- getting clean data
- formatting context properly
- validating outputs
- orchestrating workflows
- handling failures

---

## Validation Is Extremely Important

I added:
- structured outputs
- evaluator nodes
- retry logic
- output scoring

And realized:

> good AI systems do not blindly trust model outputs.

---

## FastAPI + Async Backend Development

Built:
- async FastAPI routes
- concurrent financial data fetching
- structured JSON responses
- orchestration pipelines

This was the first time backend engineering started feeling “real” instead of tutorial-level.

---

# Stack Used

- FastAPI
- AsyncIO
- AioHTTP
- LangGraph
- LangChain
- Groq
- Pydantic
- Financial Modeling Prep API

---


And honestly, that was probably the most valuable thing I learned from building this.
