# Contributing to Charge & Chew

This is a hackathon project with a 2-person team, so we're keeping process light — just enough to avoid stepping on each other.

## Branching

- `main` — always demo-able. Don't push directly.
- `backend` — Member 1's working branch.
- `frontend` — Member 2's working branch.
- Open a PR into `main` when a chunk of work is ready; the other teammate does a quick review/merge.

## Workflow

```bash
git checkout -b backend/routing-engine   # or frontend/map-markers
# ... do work ...
git add .
git commit -m "Add OSRM route fetching"
git push origin backend/routing-engine
# open a PR into main
```

## Commit messages

Keep them short and imperative: `Add charger cost calculator`, not `added stuff for cost`.

## Before merging to main

- [ ] Code runs locally without errors
- [ ] No API keys or `.env` committed
- [ ] If you changed the shape of `plan_trip()`'s return value, update `docs/data_contract.md` and ping the other teammate — this is the one thing that breaks the other side's work silently.
