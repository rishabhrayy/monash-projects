# FIT9136 — Algorithms and Programming Foundations in Python

**Semester:** Semester 2, 2024
**Program:** Master of Artificial Intelligence, Monash University
**Author:** Rishabh Ray

---

## Overview

Algorithmic problem-solving and object-oriented software design in Python, progressing from state machines and graph traversal through to inheritance-based system architecture. Assignments build working software systems that address authentication, genealogical reasoning, and inventory management — not contrived exercises. The constraint of using only the Python standard library forces deliberate algorithm and data structure choices at each step.

---

## What I Worked On

- Implemented a finite state machine for user authentication with configurable retry limits and a robot-verification challenge step
- Computed minimum movement cost for a typing robot navigating multiple keyboard layout configurations, optimising keystroke path across layout variants
- Modelled a genealogical family database using nested dictionaries as a graph structure
- Implemented graph traversal logic to identify cousin relationships between entities at arbitrary genealogical depths, handling variable-depth kinship queries correctly
- Designed an object-oriented container inventory system with a base class and three specialised subclasses (standard, multi-compartment, weight-ignoring)
- Implemented CSV parsing and data-driven object instantiation to populate the inventory from flat files

---

## Methods and Approaches

- **Finite state machine (FSM)** design for authentication flow with configurable state transitions
- **Graph representation** using nested dictionaries for genealogical relationships
- **Graph traversal** (BFS/DFS) for arbitrary-depth kinship queries
- **Inheritance-based OOP** — base container class extended with specialised behaviour via subclassing and method overriding
- **CSV parsing** with data-driven object instantiation for dynamic inventory population
- **Standard library only** — no external dependencies across all three assignments

---

## Work Breakdown

**Ass 1** → Authentication state machine with retry limits and robot-check verification; plus a movement cost optimiser for a typing robot across multiple keyboard layout configurations

**Ass 2** → Genealogical database modelled as a nested-dictionary graph; graph traversal to identify cousin relationships at arbitrary family distances

**Ass 3** → Object-oriented container inventory system: base and subclass hierarchy (standard, multi-compartment, magic weight-ignoring), CSV-driven object instantiation

---

## Key Skills Demonstrated

- Finite state machine design and implementation
- Graph representation and traversal without external libraries
- Object-oriented design with principled use of inheritance and polymorphism
- Data-driven system design via CSV parsing and runtime object construction
- Algorithmic thinking under standard-library constraints

---

## Key Insights

- Modelling state machines explicitly (rather than relying on conditionals) makes authentication flow logic easier to reason about, test, and extend — a lesson that transfers directly to workflow engines and chatbot design
- Nested dictionaries as graphs are flexible but expose the cost of lacking a typed schema — the tradeoff between flexibility and correctness is visible at every traversal step
- Inheritance hierarchies are most valuable when subclasses override behaviour, not just add fields — the magic container design makes this distinction concrete

---

## Relevance to Industry

- **Software Engineering:** FSM design, OOP, and graph traversal are foundational patterns across backend systems, game engines, and compiler design
- **AI/ML Engineering:** State machines underpin dialogue systems and workflow orchestrators; graph traversal is central to knowledge graph querying
- **Data Engineering:** CSV-driven object instantiation mirrors the pattern of configuration-driven pipeline construction used in ETL systems

---

## Tools and Technologies

- Python 3
- Standard library only (`csv`, `collections`, built-in data structures)

---

## Getting Started

```bash
python "Ass 1/A1_34525416/A1_34525416/login_match_robot.py"
python "Ass 1/A1_34525416/A1_34525416/typing_robot_many_configs.py"
python "Ass 2/A2_34525416_35135239/A2_34525416_35135239/family_database_cousins.py"
python "Ass 3/A3_34525416_35135239/A3_34525416_35135239/magic_containers.py"
```

---

## Notes

Academic coursework submitted for assessment at Monash University. Shared for portfolio and reference purposes only. Do not reproduce or submit any part of this work as your own.

---

## Author

**Rishabh Ray**
Master of Artificial Intelligence — Monash University
rishabh.aust@gmail.com | [github.com/rishabhrayy](https://github.com/rishabhrayy) | [linkedin.com/in/rishabhrayy](https://linkedin.com/in/rishabhrayy)
