# FIT5222 — Planning and Automated Reasoning

**Semester:** Semester 2, 2025
**Program:** Master of Artificial Intelligence, Monash University
**Author:** Rishabh Ray

---

## Overview

A hands-on unit spanning the full spectrum of AI planning — from deterministic single-agent pathfinding through to competitive multi-agent environments with hidden state and adversarial opponents. Assignments require building working planning systems in Python, not just understanding algorithms theoretically. The work culminates in a hybrid intelligent agent combining symbolic reasoning, probabilistic state tracking, and risk-aware search — a combination that mirrors real deployed AI systems.

---

## What I Worked On

- Implemented A\* search with a Manhattan distance heuristic for single-agent pathfinding on a rail-grid (Flatland environment), managing a priority queue over an open set with correct tie-breaking
- Extended to multi-agent settings by adding vertex conflict (two agents occupying the same cell) and edge conflict (agents swapping positions) detection
- Developed a local path repair heuristic to resolve detected conflicts without full replanning, reducing computational overhead in dense agent scenarios
- Built a competitive Pacman agent team (`myTeam.py`) using a three-component hybrid architecture:
  - PDDL-inspired symbolic reasoning for high-level strategic action selection (e.g. attack, retreat, defend)
  - Particle filter for probabilistic tracking of hidden opponents using Bayesian resampling
  - Risk-sensitive A\* for real-time tactical navigation under positional uncertainty

---

## Methods and Approaches

- **A\* search** with admissible heuristic and priority queue management via `heapq`
- **Conflict detection** for both vertex and edge conflicts in multi-agent path planning
- **Local search / path repair** for post-hoc conflict resolution without global replanning
- **PDDL-inspired symbolic reasoning** for discrete, interpretable high-level decisions
- **Particle filter** with Bayesian resampling for tracking hidden opponent positions
- **Diversity maintenance** via threshold-based resampling to prevent particle deprivation
- **Risk-sensitive A\*** incorporating positional uncertainty into movement cost calculations

---

## Work Breakdown

**Ass 1** → Single and multi-agent pathfinding in Flatland: A\* with Manhattan heuristic, then extended with vertex/edge conflict detection and local repair for collision-free multi-agent navigation

**Ass 2** → Competitive Pacman agent (`myTeam.py`): hybrid architecture combining symbolic strategic reasoning, particle filter opponent tracking, and risk-sensitive tactical navigation

---

## Key Skills Demonstrated

- Implementing and extending A\* search for non-trivial structured environments
- Multi-agent conflict detection and resolution without global replanning
- Probabilistic state estimation using particle filters with Bayesian resampling
- Hybrid agent design combining symbolic and probabilistic reasoning layers
- Building autonomous agents that operate under partial observability and adversarial pressure

---

## Key Insights

- Local path repair is significantly cheaper than global replanning for sparse conflict scenarios, but breaks down when conflicts are dense — the right choice depends on environment density
- Particle deprivation is a real failure mode in particle filters operating in sparse observation environments; maintaining diversity through forced resampling is essential for tracking persistence
- Separating strategic decision-making (symbolic) from tactical execution (search-based) produces agents that are both more interpretable and easier to debug than monolithic policy networks

---

## Relevance to Industry

- **Robotics & Autonomous Systems:** Multi-agent pathfinding with conflict resolution is directly applicable to warehouse robotics (Amazon Robotics, Kiva) and autonomous vehicle fleets
- **Game AI / Simulation:** Competitive agent design with hidden state tracking mirrors challenges in game AI research and adversarial simulation environments
- **AI Planning Systems:** Hybrid symbolic-probabilistic architectures are increasingly common in production AI systems requiring both explainability and robustness to uncertainty

---

## Tools and Technologies

- Python 3
- Flatland environment (rail-grid simulation framework)
- NumPy
- `heapq` (standard library priority queue)

---

## Getting Started

```bash
pip install numpy
python "Ass 1/Ray_34525416_flatland/Ray_34525416_flatland/src/question1.py"
python "Ass 1/Ray_34525416_flatland/Ray_34525416_flatland/src/question2.py"
```

---

## Notes

Academic coursework submitted for assessment at Monash University. Shared for portfolio and reference purposes only. Do not reproduce or submit any part of this work as your own.

---

## Author

**Rishabh Ray**
Master of Artificial Intelligence — Monash University
rishabh.aust@gmail.com | [github.com/rishabhrayy](https://github.com/rishabhrayy) | [linkedin.com/in/rishabhrayy](https://linkedin.com/in/rishabhrayy)
