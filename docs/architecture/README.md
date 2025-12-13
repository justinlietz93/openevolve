# OpenEvolve Architecture Documentation

**System:** OpenEvolve - Evolutionary Coding Agent Framework  
**Repository:** justinlietz93/openevolve  
**Commit:** 1c88c4a3df6032aae4052bb543f44ece15f03901  
**Generated:** 2025-11-09

---

## 📋 Overview

This directory contains a comprehensive architectural review and documentation of the OpenEvolve system. The documentation follows the C4 model and provides multiple views of the system architecture.

**Documentation Status:** ✅ Complete  
**Architecture Score:** 7.0/10 (GOOD - Production Ready)  
**Security Status:** ⚠️ Requires sandboxing for untrusted environments

---

## 📚 Document Index

### Core Documents

| # | Document | Description | Audience |
|---|----------|-------------|----------|
| 00 | [Executive Summary](00_executive_summary.md) | High-level overview, key findings, scores | Executives, Stakeholders |
| 04 | [Code Map](04_code_map.md) | Detailed module inventory, responsibilities | Developers, Architects |
| 10 | [Quality Gates](10_quality_gates.md) | Code quality metrics, test coverage, debt | Tech Leads, QA |
| 11 | [Non-Functionals](11_non_functionals.md) | Performance, reliability, security analysis | Architects, SREs |
| 12 | [Operability](12_operability.md) | Operations manual, runbooks, troubleshooting | DevOps, SREs |
| 13 | [Refactor Plan](13_refactor_plan.md) | Improvement roadmap, priorities, estimates | Product, Engineering |
| 14 | [Architectural Alignment](14_arch_alignment.md) | Pattern compliance, gaps, violations | Architects |

### Visual Documentation

| # | Document | Type | Description |
|---|----------|------|-------------|
| 01 | [Context C4](01_context_c4.mmd) | Mermaid | System context, users, external systems |
| 02 | [Containers C4](02_containers_c4.mmd) | Mermaid | Internal architecture, components |
| 03 | [Components (Controller/DB)](03_components_controller_database.mmd) | Mermaid | Detailed component view |
| 03 | [Components (LLM/Eval)](03_components_llm_evaluator.mmd) | Mermaid | LLM and evaluation components |
| 05 | [Dependency Graph](05_dependency_graph.dot) | Graphviz | Module dependencies, layers |
| 06 | [Dependency Matrix](06_dependency_matrix.csv) | CSV | Adjacency matrix, metrics |
| 07 | [Evolution Loop Sequence](07_runtime_sequence_evolution_loop.mmd) | Mermaid | Main iteration flow |
| 07 | [LLM Generation Sequence](07_runtime_sequence_llm_generation.mmd) | Mermaid | LLM call flow with retry |
| 07 | [Cascade Evaluation Sequence](07_runtime_sequence_cascade_evaluation.mmd) | Mermaid | 3-stage evaluation |
| 08 | [Dataflow](08_dataflow_storage_persistence.mmd) | Mermaid | Data storage and persistence |
| 09 | [Domain Model](09_domain_model.mmd) | Mermaid | Entities, aggregates, value objects |

### Machine-Readable

| File | Format | Description |
|------|--------|-------------|
| [architecture-map.json](architecture-map.json) | JSON | Complete system model (queryable) |

---

## 🎯 Quick Start Guides

### For Developers
**Start here:** [Code Map](04_code_map.md) → [Dependency Graph](05_dependency_graph.dot) → [Sequence Diagrams](07_runtime_sequence_evolution_loop.mmd)

**Key questions answered:**
- Where is functionality X implemented?
- What modules depend on module Y?
- How does the evolution loop work?

### For Architects
**Start here:** [Executive Summary](00_executive_summary.md) → [Architectural Alignment](14_arch_alignment.md) → [C4 Models](01_context_c4.mmd)

**Key questions answered:**
- Does the architecture follow best practices?
- What are the architectural gaps?
- How does the system scale?

### For Operations
**Start here:** [Operability](12_operability.md) → [Non-Functionals](11_non_functionals.md)

**Key questions answered:**
- How do I deploy this?
- How do I monitor it?
- What do I do when it fails?

### For Security
**Start here:** [Non-Functionals § Security](11_non_functionals.md#3-security) → [Quality Gates § Security](10_quality_gates.md#security-analysis)

**Key questions answered:**
- What are the security risks?
- How is code execution isolated?
- How are secrets managed?

---

## 📊 Key Metrics Summary

### Code Quality
- **Total LOC:** 6,633 (effective)
- **Modules:** 28
- **Test Coverage:** ~75%
- **Cyclomatic Complexity:** Moderate
- **Circular Dependencies:** 0 ✅

### Architecture Scores

| Dimension | Score | Status |
|-----------|-------|--------|
| Clean Architecture | 8.0/10 | ✅ Strong |
| SOLID Principles | 7.4/10 | ✅ Good |
| Domain-Driven Design | 7.2/10 | ✅ Good |
| Hexagonal Architecture | 3.7/10 | ⚠️ Weak |
| Modular Monolith | 8.5/10 | ✅ Excellent |
| **Overall** | **7.0/10** | **✅ Good** |

### Non-Functional Scores

| Dimension | Score | Status |
|-----------|-------|--------|
| Performance | 8/10 | ✅ Good |
| Reliability | 7/10 | ✅ Good |
| Security | 5/10 | ⚠️ Moderate |
| Reproducibility | 9/10 | ⭐ Exceptional |
| Operability | 9/10 | ✅ Excellent |

---

## 🔍 Key Findings

### ✅ Strengths
1. **Exceptional Reproducibility** - Comprehensive seeding ensures deterministic runs
2. **Clean Modular Design** - Well-separated concerns, low coupling
3. **Zero Circular Dependencies** - Clean acyclic dependency graph
4. **Excellent Documentation** - Comprehensive docstrings and examples
5. **Strong Domain Model** - Clear entities, aggregates, value objects

### ⚠️ Areas for Improvement
1. **Security** - Code execution needs sandboxing (HIGH priority)
2. **Observability** - Lacks structured metrics/tracing (MEDIUM priority)
3. **Hexagonal Architecture** - Missing ports/adapters pattern (MEDIUM priority)
4. **Module Size** - database.py at 1,765 LOC (LOW priority)

### 🔴 Top Risks
1. **RISK-001:** Arbitrary code execution without sandboxing (HIGH)
2. **RISK-003:** API keys in environment variables (MEDIUM)
3. **RISK-009:** Prompt injection via artifacts (MEDIUM)

**See:** [Quality Gates § Security](10_quality_gates.md#security-analysis) for details

---

## 🛠 Recommended Actions

### Immediate (Week 1)
1. Review [Refactor Plan § Quick Wins](13_refactor_plan.md#quick-wins-1-2-days-each)
2. Implement input sanitization (QW3)
3. Add Docker sandboxing example (QW5)
4. Document security considerations

### Short-term (Month 1-2)
1. Implement secrets management (MT2)
2. Add OpenTelemetry instrumentation (MT3)
3. Split database.py into sub-modules (MT1)
4. Add resource limits to evaluation (MT5)

### Long-term (Month 3-6)
1. Implement plugin system for LLM backends (ST1)
2. Add distributed execution support (ST2)
3. Build real-time monitoring dashboard (ST3)

**See:** [Refactor Plan](13_refactor_plan.md) for complete roadmap

---

## 📐 Rendering Diagrams

### Mermaid Diagrams (.mmd)

**Option 1: GitHub (automatic)**
- View .mmd files directly on GitHub
- Automatic rendering in markdown preview

**Option 2: Mermaid CLI**
```bash
npm install -g @mermaid-js/mermaid-cli

# Generate SVG
mmdc -i 01_context_c4.mmd -o assets/01_context_c4.svg

# Generate PNG
mmdc -i 01_context_c4.mmd -o assets/01_context_c4.png -w 2000 -H 1500
```

**Option 3: Online**
- Visit https://mermaid.live
- Paste diagram code
- Export SVG/PNG

### Graphviz Diagrams (.dot)

```bash
# Install graphviz
sudo apt-get install graphviz

# Generate SVG
dot -Tsvg 05_dependency_graph.dot -o assets/05_dependency_graph.svg

# Generate PNG
dot -Tpng 05_dependency_graph.dot -o assets/05_dependency_graph.png -Gdpi=150
```

---

## 🔗 External References

### Related Documentation
- [Main README](../../README.md) - System overview and quick start
- [CLAUDE.md](../../CLAUDE.md) - AI assistant guidance
- [CONTRIBUTING.md](../../CONTRIBUTING.md) - Contribution guidelines

### Standards & Patterns
- [C4 Model](https://c4model.com/) - Architecture visualization
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) - Robert C. Martin
- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html) - Eric Evans
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID) - Object-oriented design

### Tools Used
- Python AST - Static code analysis
- Mermaid - Diagram generation
- Graphviz - Dependency visualization
- JSON Schema - Machine-readable format

---

## 📝 Maintenance

### Updating Documentation

**When to update:**
- Major architectural changes
- New modules or components
- Significant refactoring
- Security improvements

**How to update:**
1. Update affected .mmd/.dot files
2. Regenerate images (see Rendering Diagrams)
3. Update architecture-map.json
4. Update metrics in executive summary
5. Commit changes with clear message

### Document Versioning

**Versioning scheme:** docs tied to commit SHA

**Current version:**
- Commit: 1c88c4a3df6032aae4052bb543f44ece15f03901
- Date: 2025-11-09

**To create new version:**
```bash
# Update all documents with new commit SHA
find docs/architecture -name "*.md" -o -name "*.mmd" -o -name "*.json" | \
  xargs sed -i 's/COMMIT_SHA_HERE/NEW_SHA_HERE/g'
```

---

## 🎓 Learning Resources

### Understanding the System
1. Start with [Executive Summary](00_executive_summary.md)
2. Review [Context Diagram](01_context_c4.mmd) for big picture
3. Read [Code Map](04_code_map.md) for module details
4. Study [Evolution Loop Sequence](07_runtime_sequence_evolution_loop.mmd) for flow

### Architecture Patterns
- Clean Architecture score: 8/10 - Study [Alignment doc](14_arch_alignment.md)
- MAP-Elites algorithm - Study [Database code](04_code_map.md#2-storage--evolution-layer)
- Process-based parallelism - Study [Process Parallel](04_code_map.md#openevolveparallel)

### Contribution Guidelines
1. Follow existing patterns (see [Code Map](04_code_map.md#file-organization-standards))
2. Add tests for new features (see [Quality Gates](10_quality_gates.md#test-coverage-analysis))
3. Update architecture docs for major changes
4. Run linters and tests before committing

---

## ❓ FAQ

**Q: Is OpenEvolve production-ready?**  
A: Yes, for trusted environments. Sandboxing recommended for untrusted code evolution.

**Q: What's the biggest architectural weakness?**  
A: Lack of ports/adapters pattern makes it hard to swap implementations. See [Architectural Alignment](14_arch_alignment.md#4-hexagonal-architecture-ports--adapters).

**Q: How much technical debt exists?**  
A: Low (~25-40 days estimated). See [Quality Gates § Technical Debt](10_quality_gates.md#technical-debt-assessment).

**Q: Can I use this for microservices?**  
A: Not without refactoring. Current design is modular monolith. See [Alignment § Microservices](14_arch_alignment.md#6-microservices-readiness).

**Q: How do I contribute architectural improvements?**  
A: Start with [Refactor Plan](13_refactor_plan.md), pick a task, create PR with updated docs.

---

## 📧 Contact

**Architecture Questions:** See GitHub Issues  
**Security Concerns:** See Security Policy  
**General Discussion:** See GitHub Discussions

---

## 📄 License

This documentation is part of OpenEvolve and follows the same Apache-2.0 license as the main project.

---

**Last Updated:** 2025-11-09  
**Document Version:** 1.0  
**Reviewed By:** Architectural Review Agent
