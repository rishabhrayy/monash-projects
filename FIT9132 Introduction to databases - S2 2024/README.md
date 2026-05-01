# FIT9132 — Introduction to Databases

**Semester:** Semester 2, 2024
**Program:** Master of Artificial Intelligence, Monash University
**Author:** Rishabh Ray

---

## Overview

Relational database design, SQL programming, and NoSQL document storage — applied to real administrative domains rather than toy examples. The unit covers the full design-to-implementation pipeline: entity-relationship modelling, normalisation to 3NF, Oracle SQL schema construction, complex query authoring, and MongoDB document operations. Two assignments implement distinct systems for library management and Olympic logistics, with the latter requiring schema translation between relational and document models.

---

## What I Worked On

- Designed entity-relationship diagrams for library management and Olympic vehicle logistics domains, identifying entities, attributes, cardinalities, and participation constraints
- Normalised relational schemas to third normal form (3NF) to eliminate transitive dependencies
- Implemented Oracle SQL DDL including table creation, primary/foreign key constraints, and sequence-based surrogate ID generation
- Wrote Oracle SQL DML (insert, update, delete) operations for both domains
- Authored complex SQL queries using `JSON_OBJECT` and `JSON_ARRAYAGG` to generate hierarchical JSON output from relational data — bridging the relational and document paradigms
- Designed a MongoDB document schema with nested subdocuments for driver and trip data
- Implemented MongoDB `insertMany` with embedded arrays and nested pickup/dropoff subdocuments
- Queried MongoDB using `find` with `$in` for multi-value field matching and `updateOne` using `$push` and `$set` in a single atomic operation

---

## Methods and Approaches

- **Entity-Relationship (ER) modelling** for conceptual schema design
- **Third normal form (3NF) normalisation** applied to real-world datasets to eliminate redundancy
- **Oracle SQL DDL/DML** for schema creation and data manipulation with referential integrity
- **JSON generation from relational data** using `JSON_OBJECT` / `JSON_ARRAYAGG` aggregate functions
- **MongoDB document modelling** with nested subdocuments and embedded arrays
- **Atomic MongoDB updates** combining `$push` and `$set` in a single operation

---

## Work Breakdown

**Ass 2** → Library management system in Oracle SQL: ER design, 3NF normalisation, full DDL with referential integrity (tables for books, authors, borrowers, loans, branches), and DML for data population and manipulation

**Ass 3** → Olympic vehicle trip management: Oracle SQL sequences, DDL/DML, JSON generation from relational data; then the same domain modelled as a MongoDB collection with nested subdocuments, atomic update operations, and multi-value queries

---

## Key Skills Demonstrated

- Conceptual-to-physical database design across the full pipeline
- 3NF normalisation and referential integrity enforcement
- Oracle SQL including advanced JSON generation from relational data
- MongoDB schema design with embedded documents and arrays
- Translating between relational and document data models for the same domain

---

## Key Insights

- The decision between normalisation and denormalisation is not purely academic — it directly impacts query complexity, write performance, and data consistency guarantees in production systems
- Generating JSON from relational data with `JSON_ARRAYAGG` reveals the impedance mismatch between SQL's flat tuple model and hierarchical API responses — a problem every backend engineer encounters
- MongoDB's embedding model trades query simplicity for update complexity; the right choice depends on access patterns, not just data shape

---

## Relevance to Industry

- **Backend Engineering:** Direct application to production database schema design, API data modelling, and ORM-level decisions
- **Data Engineering:** ER modelling, normalisation, and cross-paradigm schema translation are foundational skills for data pipeline design
- **AI/ML Infrastructure:** Understanding relational vs. document storage trade-offs is essential for designing feature stores, training data pipelines, and experiment tracking systems

---

## Tools and Technologies

- Oracle SQL (DDL, DML, `JSON_OBJECT`, `JSON_ARRAYAGG`)
- MongoDB (MongoDB Playground / mongosh)
- SQL\*Plus or compatible Oracle client

---

## Notes

Academic coursework submitted for assessment at Monash University. Shared for portfolio and reference purposes only. Do not reproduce or submit any part of this work as your own.

---

## Author

**Rishabh Ray**
Master of Artificial Intelligence — Monash University
rishabh.aust@gmail.com | [github.com/rishabhrayy](https://github.com/rishabhrayy) | [linkedin.com/in/rishabhrayy](https://linkedin.com/in/rishabhrayy)
