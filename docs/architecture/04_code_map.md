# Code Map: OpenEvolve Module Structure

**Commit:** 1c88c4a3df6032aae4052bb543f44ece15f03901  
**Generated:** 2025-11-09

---

## Module Inventory

**Total Modules:** 28 Python files  
**Total Effective LOC:** 6,633 (excluding comments/blanks)  
**Average Module Size:** 237 LOC  
**Largest Module:** database.py (1,765 LOC)  
**Package Structure:** Hierarchical with clear namespaces

---

## Core Modules (by responsibility)

### 1. Orchestration Layer

#### **openevolve/controller.py** (431 LOC)
**Class:** `OpenEvolve`  
**Responsibility:** Main orchestration of evolution loop  
**Key Functions:**
- `__init__()` - System initialization with config loading
- `run()` - Main evolution loop coordinator
- `_setup_logging()` - Configures structured logging
- `_load_initial_program()` - Parses and validates initial code
- `_run_checkpoint()` - Periodic state persistence

**Dependencies:** config, database, evaluator, llm.ensemble, prompt.sampler, process_parallel  
**Dependents:** cli, api  
**Complexity:** HIGH - Central coordination point

**Architecture Notes:**
- Manages global best program tracking (absolute best property)
- Coordinates checkpoint/resume functionality
- Handles graceful shutdown on SIGINT/SIGTERM
- Thread-safe metrics aggregation

---

#### **openevolve/process_parallel.py** (530 LOC)
**Classes:** `ProcessParallelController`, `SerializableResult`  
**Responsibility:** Process-based parallel execution of iterations  
**Key Functions:**
- `run_iteration_parallel()` - Distributes work across process pool
- `_run_iteration_worker()` - Worker function executed in subprocess
- `_serialize_config()` - Config marshalling for IPC
- `_lazy_init_worker_components()` - Worker initialization pattern

**Dependencies:** controller, database, llm, evaluator  
**Dependents:** controller  
**Complexity:** HIGH - Multiprocessing coordination

**Architecture Notes:**
- Uses ProcessPoolExecutor for true parallelism (bypasses GIL)
- Serializes database snapshots to workers (immutable read-only)
- Each worker gets fresh Python interpreter (memory isolation)
- Handles process crashes gracefully without killing parent

---

### 2. Storage & Evolution Layer

#### **openevolve/database.py** (1,765 LOC)
**Classes:** `Program`, `ProgramDatabase`  
**Responsibility:** MAP-Elites quality-diversity archive with island model  
**Key Functions:**
- `add_program()` - Inserts program into appropriate grid cell
- `sample_programs()` - Multi-strategy selection (elite/diverse/exploratory)
- `trigger_migration()` - Handles inter-island program transfer
- `_discretize_features()` - Maps continuous features to grid bins
- `_calculate_diversity()` - Edit distance from population

**Key Data Structures:**
- Islands: List of independent MAP-Elites grids
- Grid: Dict mapping (feature_tuple) → Program
- Migration: Ring topology with lazy triggering

**Dependencies:** config, utils.code_utils, utils.metrics_utils  
**Dependents:** controller, evaluator, prompt.sampler  
**Complexity:** VERY HIGH - Core algorithm implementation

**Architecture Notes:**
- Implements double-selection: different programs for perf vs inspiration
- Lazy migration based on generation counts (not iteration counts)
- Artifact threshold: <10KB in JSON, >10KB as files
- Feature dimensions dynamically determined from first program
- Grid stability through consistent binning (min/max tracking)

**Performance Characteristics:**
- Sample: O(n) where n = cells in grid
- Add: O(1) with feature computation overhead
- Migration: O(k) where k = programs to migrate

---

### 3. Evaluation Layer

#### **openevolve/evaluator.py** (537 LOC)
**Class:** `Evaluator`  
**Responsibility:** Three-stage cascade evaluation with parallel execution  
**Key Functions:**
- `evaluate_program()` - Orchestrates cascade
- `evaluate_parallel()` - Batches programs for concurrent eval
- `_process_evaluation_result()` - Normalizes user evaluator output
- `_validate_cascade_configuration()` - Checks stage definitions

**Dependencies:** config, database, llm.ensemble, prompt.sampler, utils.async_utils  
**Dependents:** controller, iteration  
**Complexity:** HIGH - Complex orchestration

**Architecture Notes:**
- Stage 1: Quick validation (syntax, imports) - ~100ms
- Stage 2: Basic testing (unit tests) - ~1-5s
- Stage 3: Comprehensive (benchmarks) - ~5-30s
- Early termination on stage failures (cascade property)
- Parallel evaluation via TaskPool (semaphore-based concurrency)
- Artifacts stored separately (side-channel feedback)

**Cascade Configuration:**
```yaml
evaluator:
  cascade_evaluation: true
  stage_1_timeout: 5s
  stage_2_timeout: 30s  
  stage_3_timeout: 300s
```

---

### 4. LLM Integration Layer

#### **openevolve/llm/ensemble.py** (70 LOC)
**Class:** `LLMEnsemble`  
**Responsibility:** Multi-model ensemble with weighted selection  
**Key Functions:**
- `generate()` - Orchestrates ensemble generation
- `_sample_model()` - Weighted random selection

**Dependencies:** llm.openai, llm.base, config  
**Dependents:** controller, iteration  
**Complexity:** MEDIUM

**Architecture Notes:**
- Supports multiple models with configurable weights
- Automatic fallback to next model on failure
- Temperature-based sampling for model diversity
- Async generation with timeout enforcement

---

#### **openevolve/llm/openai.py** (143 LOC)
**Class:** `OpenAILLM`  
**Responsibility:** OpenAI-compatible API client  
**Key Functions:**
- `generate()` - Async code generation with retry
- `_make_api_call()` - HTTP request with exponential backoff

**Dependencies:** openai (library), config  
**Dependents:** llm.ensemble  
**Complexity:** MEDIUM

**Architecture Notes:**
- Works with any OpenAI-compatible endpoint (Gemini, Ollama, etc.)
- Exponential backoff: 1s, 2s, 4s, 8s, 16s
- Streaming support (not currently used)
- Reasoning effort parameter for o-series models

---

### 5. Prompt Engineering Layer

#### **openevolve/prompt/sampler.py** (479 LOC)
**Class:** `PromptSampler`  
**Responsibility:** Context-aware prompt construction  
**Key Functions:**
- `build_prompt()` - Assembles full prompt from templates + context
- `_format_inspiration_programs()` - Includes example programs
- `_format_artifacts()` - Includes execution feedback
- `_identify_improvement_areas()` - Suggests optimization targets

**Dependencies:** database, prompt.templates, config  
**Dependents:** llm.ensemble, iteration  
**Complexity:** HIGH - Complex template logic

**Architecture Notes:**
- Samples inspiration programs from database (top + diverse)
- Includes artifacts from previous failures (feedback loop)
- Template stochasticity: randomizes prompt variations
- Diff-based vs full-rewrite strategies
- Evolution history tracking (parent → child → grandchild)

**Prompt Structure:**
```
1. System message (domain expertise)
2. Current program code
3. Inspiration programs (2-5 examples)
4. Artifacts (errors, warnings, profiling)
5. Improvement suggestions
6. Constraints (EVOLVE-BLOCK markers)
```

---

#### **openevolve/prompt/templates.py** (154 LOC)
**Class:** `TemplateManager`  
**Responsibility:** Template loading and fragment management  
**Key Functions:**
- `get_template()` - Retrieves full template
- `get_fragment()` - Retrieves template fragment
- `_load_from_directory()` - Scans template directories

**Dependencies:** None (pure utility)  
**Dependents:** prompt.sampler  
**Complexity:** LOW

**Architecture Notes:**
- Default templates in `openevolve/prompts/defaults/`
- Custom templates via `template_dir` config
- Supports Jinja-like placeholders: `{variable}`
- Fragment composition for modular prompts

---

### 6. Configuration Layer

#### **openevolve/config.py** (356 LOC)
**Classes:** `Config`, `LLMConfig`, `DatabaseConfig`, `EvaluatorConfig`, `PromptConfig`  
**Responsibility:** Hierarchical configuration with validation  
**Key Functions:**
- `load_config()` - Loads from YAML with defaults
- `from_yaml()` - Parses and validates YAML
- `update_model_params()` - Dynamic model parameter updates

**Dependencies:** None (pure configuration)  
**Dependents:** All modules  
**Complexity:** MEDIUM

**Architecture Notes:**
- Dataclass-based with automatic validation
- Hierarchical: system → component → sub-component
- Default values in `configs/default_config.yaml`
- CLI argument override support
- Environment variable support (e.g., OPENAI_API_KEY)

**Key Configuration Sections:**
```yaml
llm:          # LLM models, API settings
database:     # Islands, grid, migration
evaluator:    # Cascade stages, parallelism
prompt:       # Templates, sampling strategy
random_seed:  # Reproducibility
```

---

### 7. Evolution Tracing Layer

#### **openevolve/evolution_trace.py** (422 LOC)
**Classes:** `EvolutionTrace`, `EvolutionTracer`  
**Responsibility:** Lineage tracking and export  
**Key Functions:**
- `record_iteration()` - Logs iteration event
- `extract_full_lineage_traces()` - Reconstructs parent→child chains
- `export()` - Serializes to JSON/JSONL/HDF5

**Dependencies:** database, config  
**Dependents:** controller  
**Complexity:** MEDIUM

**Architecture Notes:**
- Tracks complete program genealogy
- Records improvement deltas (parent → child)
- Exports in multiple formats (JSON, JSONL, HDF5)
- Checkpoint integration for persistence
- Supports incremental trace building

---

### 8. Utility Modules

#### **openevolve/utils/code_utils.py** (148 LOC)
**Functions:**
- `parse_evolve_blocks()` - Extracts EVOLVE-BLOCK markers
- `apply_diff()` - Applies unified diff patches
- `extract_diffs()` - Computes code differences
- `calculate_edit_distance()` - Levenshtein distance

**Dependencies:** None  
**Dependents:** database, prompt.sampler  
**Complexity:** LOW - Pure functions

---

#### **openevolve/utils/async_utils.py** (181 LOC)
**Class:** `TaskPool`  
**Functions:** `run_in_executor()`

**Responsibility:** Async concurrency primitives  
**Key Features:**
- Semaphore-based concurrency limiting
- Executor-based blocking I/O handling
- Graceful task cancellation

**Dependencies:** None  
**Dependents:** evaluator  
**Complexity:** MEDIUM

---

#### **openevolve/utils/metrics_utils.py** (107 LOC)
**Functions:**
- `safe_numeric_average()` - Handles mixed-type metrics
- `get_fitness_score()` - Combined metric calculation
- `format_feature_coordinates()` - Grid coordinate formatting

**Dependencies:** None  
**Dependents:** database, controller  
**Complexity:** LOW

---

#### **openevolve/utils/trace_export_utils.py** (280 LOC)
**Functions:**
- `export_traces_jsonl()` - Line-delimited JSON export
- `export_traces_hdf5()` - HDF5 format export
- `append_trace_jsonl()` - Incremental trace writing

**Dependencies:** numpy, h5py (optional)  
**Dependents:** evolution_trace  
**Complexity:** MEDIUM

---

### 9. API Layer

#### **openevolve/api.py** (411 LOC)
**Class:** `EvolutionResult`  
**Functions:**
- `run_evolution()` - High-level evolution API
- `evolve_function()` - Function-level evolution
- `evolve_algorithm()` - Algorithm discovery

**Dependencies:** controller, config, utils  
**Dependents:** External users  
**Complexity:** MEDIUM - User-facing facade

**Architecture Notes:**
- Provides Pythonic API over CLI
- Supports inline code (no files required)
- Automatic temporary file management
- Returns structured results with best program, traces, metrics

**Usage Example:**
```python
from openevolve import run_evolution

result = run_evolution(
    initial_program="def sort(arr): ...",
    evaluator=lambda path: {"score": benchmark(path)},
    iterations=100
)
print(result.best_code)
```

---

#### **openevolve/cli.py** (134 LOC)
**Functions:**
- `parse_args()` - Argument parsing
- `main()` - CLI entry point

**Dependencies:** controller, config  
**Dependents:** openevolve-run.py  
**Complexity:** LOW

**Architecture Notes:**
- Thin wrapper over controller
- Handles argument validation
- Sets up logging and signal handlers
- Supports checkpoint resume via `--checkpoint` flag

---

### 10. Supporting Modules

#### **openevolve/iteration.py** (120 LOC)
**Class:** `Result`  
**Responsibility:** Single iteration execution logic  
**Architecture Notes:**
- Worker-level code (runs in subprocess)
- Samples → Mutates → Evaluates → Stores
- Returns serializable result to parent process

---

#### **openevolve/embedding.py** (76 LOC)
**Class:** `EmbeddingClient`  
**Responsibility:** Novelty detection via embeddings  
**Key Functions:**
- `get_embedding()` - Calls embedding API
- Computes cosine similarity for novelty scoring

**Architecture Notes:**
- Optional feature (enabled via config)
- Uses OpenAI embeddings API
- 768-dimensional vectors (text-embedding-ada-002)
- Filters overly similar programs (diversity maintenance)

---

#### **openevolve/evaluation_result.py** (62 LOC)
**Class:** `EvaluationResult`  
**Responsibility:** Structured evaluation output  
**Architecture Notes:**
- Normalizes user evaluator return values
- Supports dict, EvaluationResult, or scalar returns
- Handles artifacts (small: JSON, large: files)

---

## Module Dependency Graph Summary

**Layers (bottom-up):**

```
Layer 0 (No dependencies):
- utils/code_utils.py
- utils/metrics_utils.py
- utils/format_utils.py
- llm/base.py
- evaluation_result.py

Layer 1 (Utils + Config):
- config.py
- utils/async_utils.py
- prompt/templates.py

Layer 2 (Config + Base):
- llm/openai.py
- embedding.py

Layer 3 (LLM + Storage):
- llm/ensemble.py
- database.py

Layer 4 (Storage + Prompts):
- prompt/sampler.py
- evolution_trace.py

Layer 5 (Evaluator):
- evaluator.py

Layer 6 (Iteration):
- iteration.py
- process_parallel.py

Layer 7 (Controller):
- controller.py

Layer 8 (API/CLI):
- api.py
- cli.py
```

**Circular Dependencies:** None detected (clean acyclic structure)

**Hotspots (most dependencies):**
1. controller.py (imports 7 modules)
2. database.py (imported by 6 modules)
3. config.py (imported by 8 modules)

---

## File Organization Standards

**Naming Conventions:**
- Snake_case for modules: `process_parallel.py`
- PascalCase for classes: `ProgramDatabase`
- Snake_case for functions: `safe_numeric_average()`
- UPPER_CASE for constants: `DEFAULT_TIMEOUT`

**Module Structure Pattern:**
```python
"""Module docstring"""

import stdlib
import third_party
import openevolve

logger = logging.getLogger(__name__)

# Constants
DEFAULT_VALUE = 42

# Classes
class MyClass:
    """Class docstring"""
    pass

# Functions
def my_function():
    """Function docstring"""
    pass
```

**Testing:**
- Test files in `/tests/` directory
- Naming: `test_<module>.py`
- Uses unittest framework
- 35 test files covering core functionality

---

## Key Architectural Patterns

1. **Dependency Injection:** Config passed to all components
2. **Strategy Pattern:** Pluggable LLM implementations
3. **Template Method:** Cascade evaluation stages
4. **Repository Pattern:** Database abstraction
5. **Builder Pattern:** Prompt construction
6. **Facade Pattern:** API layer over controller
7. **Worker Pool Pattern:** Process parallelism

---

## Code Quality Metrics

**Maintainability Index:** HIGH
- Clear module boundaries
- Minimal coupling
- High cohesion within modules
- Comprehensive docstrings

**Testability:** MEDIUM-HIGH
- Good unit test coverage for core algorithms
- Limited integration tests (require LLM API)
- Deterministic behavior (seeded randomness)

**Documentation:** HIGH
- Module-level docstrings
- Class-level docstrings
- Function-level docstrings
- Inline comments for complex logic
- External README and examples

---

## Recommended Refactoring Opportunities

### Quick Wins
1. Extract constants to `constants.py` module
2. Move helper functions to utils
3. Add type hints to all public APIs
4. Standardize error classes

### Medium-term
1. Split database.py into sub-modules (island.py, grid.py, etc.)
2. Extract sampling strategies to separate classes
3. Create abstract Evaluator interface
4. Add metrics collection infrastructure

### Strategic
1. Plugin system for custom LLM backends
2. Database backend abstraction (support SQL, etc.)
3. Distributed execution support
4. Real-time monitoring integration

---

**Navigation:** Use IDE "Go to Definition" with cross-references above. Module paths are relative to repository root.
