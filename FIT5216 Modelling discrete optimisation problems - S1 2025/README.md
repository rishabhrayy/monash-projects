# FIT5216 — Modelling Discrete Optimisation Problems

**Semester:** Semester 1, 2025
**Program:** Master of Artificial Intelligence, Monash University
**Author:** Rishabh Ray

---

## Overview

Constraint programming as a practical tool for tackling real-world combinatorial optimisation problems — scheduling, resource allocation, and multi-objective decision-making. The unit develops the skill of translating an ambiguous problem specification into a precise declarative model: choosing the right decision variables, encoding constraints faithfully, and designing objective functions that capture competing goals. Both assignments target scheduling domains with non-trivial structural complexity, implemented in MiniZinc.

---

## What I Worked On

- Modelled a vaccine resource allocation and treatment scheduling problem using enum-typed decision variables for vaccines, treatments, and biological strains
- Encoded treatment frequency requirements, precedence ordering constraints, and a hard expenditure budget cap within a single constraint model
- Modelled a vehicle service and maintenance scheduling problem with overlapping resource windows and explicit interval overlap detection
- Designed a dual-objective function minimising maintenance overlap while maximising completed service events
- Iteratively refined constraint models to ensure satisfiability without over-constraining the solution space

---

## Methods and Approaches

- **Constraint programming (CP)** with declarative variable and constraint specification in MiniZinc
- **Enum-based type modelling** for structured, domain-specific decision variables
- **Precedence and frequency constraints** for temporal ordering in scheduling problems
- **Interval overlap detection** via arithmetic constraints on start time and duration variables
- **Multi-objective optimisation** with a combined objective balancing competing goals
- **Hard vs. soft constraint stratification** — expenditure cap as a hard constraint; service maximisation as a soft objective

---

## Work Breakdown

**Ass 1** → Vaccine and treatment scheduling: enum types, frequency and precedence constraints, hard expenditure limit, satisfaction objective over valid treatment plans

**Ass 2** → Vehicle maintenance and service scheduling: resource assignment constraints, interval overlap management, dual objective minimising conflict while maximising service throughput

---

## Key Skills Demonstrated

- Translating informal problem specifications into precise declarative constraint models
- Designing structured decision variable types using enumerations
- Encoding temporal, resource, and budget constraints in a unified model
- Formulating and balancing multi-objective optimisation problems
- Debugging unsatisfiable models by isolating conflicting constraints

---

## Key Insights

- The hardest part of constraint programming is not the solver — it is the modelling: under-constraining produces meaningless solutions; over-constraining produces unsatisfiability
- Multi-objective problems rarely have a single correct answer — the objective weighting encodes a value judgement that must be made explicit
- MiniZinc's solver-agnostic architecture makes it an effective prototyping layer for combinatorial problems that may later be ported to industrial solvers (OR-Tools, Gecode, Chuffed)

---

## Relevance to Industry

- **Operations Research:** Constraint programming is the backbone of logistics optimisation, workforce scheduling, and supply chain planning at scale
- **AI Planning Systems:** CP models naturally complement AI planning frameworks for problems with hard resource constraints
- **Algorithmic Product Design:** Precise combinatorial modelling is a differentiating skill for engineers working on scheduling infrastructure or resource allocation engines

---

## Tools and Technologies

- MiniZinc 2.x — constraint modelling language and solver interface
- MiniZinc IDE or `minizinc` CLI

---

## Getting Started

```bash
minizinc "Ass 1/rift.mzn"
minizinc "Ass 2/service.mzn"
```

---

## Notes

Academic coursework submitted for assessment at Monash University. Shared for portfolio and reference purposes only. Do not reproduce or submit any part of this work as your own.

---

## Author

**Rishabh Ray**
Master of Artificial Intelligence — Monash University
rishabh.aust@gmail.com | [github.com/rishabhrayy](https://github.com/rishabhrayy) | [linkedin.com/in/rishabhrayy](https://linkedin.com/in/rishabhrayy)
