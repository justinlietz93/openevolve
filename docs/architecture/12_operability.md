# Operability & Operations Manual

**System:** OpenEvolve  
**Commit:** 1c88c4a3df6032aae4052bb543f44ece15f03901  
**Analysis Date:** 2025-11-09

---

## 1. Logging System

### 1.1 Configuration

**Implementation:** Python `logging` module

**Configuration Location:**
- `openevolve/controller.py` - `_setup_logging()` method

**Log Levels:**
```python
logging.DEBUG    # Detailed debug information
logging.INFO     # General informational messages  
logging.WARNING  # Warning messages
logging.ERROR    # Error messages
logging.CRITICAL # Critical failures
```

**Log Destinations:**
1. **Console:** stdout (INFO and above)
2. **File:** `<output_dir>/openevolve.log` (DEBUG and above)

### 1.2 Log Format

```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

**Example:**
```
2025-11-09 14:23:45 - openevolve.controller - INFO - Starting evolution run
2025-11-09 14:23:45 - openevolve.database - INFO - Initialized database with 5 islands
2025-11-09 14:23:46 - openevolve.llm.openai - DEBUG - Calling OpenAI API (model=gemini-2.5-pro)
```

### 1.3 Key Log Events

| Event | Level | Logger | Message Pattern |
|-------|-------|--------|-----------------|
| **Iteration Start** | INFO | controller | `Iteration {n}/{total} starting` |
| **Program Added** | INFO | database | `Added program {id} to island {island_id}` |
| **Best Updated** | INFO | controller | `New best program! Score: {score}` |
| **Migration** | INFO | database | `Migrating {n} programs from island {src} to {dst}` |
| **Checkpoint** | INFO | controller | `Saving checkpoint at iteration {n}` |
| **LLM Error** | WARNING | llm.openai | `API error: {error}, retrying...` |
| **Eval Failure** | WARNING | evaluator | `Evaluation failed: {reason}` |
| **Crash** | ERROR | * | `Unexpected error: {traceback}` |

### 1.4 Log Management

**Rotation:** Not implemented  
**Recommendation:** Use `logging.handlers.RotatingFileHandler`

```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'openevolve.log',
    maxBytes=10*1024*1024,  # 10 MB
    backupCount=5
)
```

**Retention:** Manual deletion required  
**Search:** Standard text tools (grep, awk, etc.)

---

## 2. Metrics & Monitoring

### 2.1 Built-in Metrics

**Tracked Automatically:**

| Metric | Type | Location | Frequency |
|--------|------|----------|-----------|
| **Iterations completed** | Counter | Controller | Per iteration |
| **Best score** | Gauge | Controller | Per iteration |
| **Programs in database** | Gauge | Database | Real-time |
| **Grid coverage** | Gauge | Database | Per iteration |
| **Island population** | Gauge | Database | Real-time |
| **Successful evaluations** | Counter | Evaluator | Per eval |
| **Failed evaluations** | Counter | Evaluator | Per eval |

**Access:** Logged to console/file, stored in checkpoint metadata

### 2.2 Programmatic Access

```python
from openevolve import OpenEvolve

controller = OpenEvolve(...)
controller.run()

# Access metrics
best_program = controller.best_program
database_stats = controller.database.get_stats()
island_stats = controller.database.get_island_stats()
```

### 2.3 External Monitoring Integration

**Current:** None implemented

**Recommendation:** Add Prometheus metrics exporter

```python
from prometheus_client import Counter, Gauge, start_http_server

# Define metrics
iterations = Counter('openevolve_iterations_total', 'Total iterations')
best_score = Gauge('openevolve_best_score', 'Current best score')

# Export
start_http_server(9090)
```

---

## 3. Tracing & Debugging

### 3.1 Evolution Traces

**Purpose:** Track program lineage and improvements

**Storage:**
- In checkpoint: `traces/` directory
- Formats: JSON, JSONL, HDF5

**Contents:**
```json
{
  "program_id": "uuid-here",
  "parent_id": "parent-uuid",
  "generation": 5,
  "iteration": 123,
  "timestamp": 1699564800.0,
  "metrics": {"score": 0.85, "time": 12.3},
  "improvement": {"score": +0.05},
  "island_id": 2
}
```

**Usage:**
```python
from openevolve.evolution_trace import extract_full_lineage_traces

traces = extract_full_lineage_traces(checkpoint_dir)
# Analyze lineage, compute statistics, visualize
```

### 3.2 Debug Mode

**Enable:**
```bash
# Environment variable
export OPENEVOLVE_DEBUG=1

# Or in code
import logging
logging.getLogger('openevolve').setLevel(logging.DEBUG)
```

**Debug Output Includes:**
- Detailed LLM prompts
- API request/response
- Database operations
- Feature computation
- Sampling decisions

### 3.3 Debugging Failed Runs

**Checklist:**

1. **Check logs:**
   ```bash
   tail -f <output_dir>/openevolve.log
   grep ERROR <output_dir>/openevolve.log
   ```

2. **Check checkpoint:**
   ```bash
   ls -lh <output_dir>/checkpoints/
   cat <output_dir>/checkpoints/checkpoint_N/metadata.json
   ```

3. **Enable debug logging:**
   ```bash
   OPENEVOLVE_DEBUG=1 python openevolve-run.py ...
   ```

4. **Examine database:**
   ```python
   from openevolve.database import ProgramDatabase
   db = ProgramDatabase.load_from_file('checkpoint_N/database.json')
   print(db.get_stats())
   ```

---

## 4. Configuration Management

### 4.1 Configuration Sources (Priority Order)

1. **CLI Arguments** (highest priority)
2. **Config File** (YAML)
3. **Environment Variables**
4. **Defaults** (lowest priority)

### 4.2 Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `OPENAI_API_KEY` | LLM API key | `sk-...` |
| `OPENAI_API_BASE` | API endpoint override | `http://localhost:8000/v1` |
| `OPENEVOLVE_DEBUG` | Enable debug logging | `1` |

### 4.3 Configuration Files

**Format:** YAML

**Location:**
- User-provided: `--config path/to/config.yaml`
- Defaults: `configs/default_config.yaml`

**Structure:**
```yaml
max_iterations: 1000
random_seed: 42
output_dir: "./openevolve_output"

llm:
  models:
    - name: "gemini-2.5-pro"
      weight: 0.6
    - name: "gemini-2.5-flash"
      weight: 0.4
  temperature: 0.7
  
database:
  population_size: 500
  num_islands: 5
  feature_dimensions: ["complexity", "diversity"]
  
evaluator:
  cascade_evaluation: true
  parallel_evaluations: 4
```

**Validation:**
- Automatic on load
- Raises `ValueError` on invalid config

### 4.4 Runtime Configuration Updates

**Not Supported:** Config changes require restart

**Workaround:** Use checkpoint resume with new config

```bash
# Initial run
python openevolve-run.py ... --config config_v1.yaml --iterations 500

# Resume with new config
python openevolve-run.py ... --config config_v2.yaml \
  --checkpoint openevolve_output/checkpoints/checkpoint_500 \
  --iterations 1000
```

---

## 5. Feature Flags

### 5.1 Available Flags

**In Configuration:**

| Flag | Purpose | Default | Impact |
|------|---------|---------|--------|
| `cascade_evaluation` | Enable cascade | `true` | Performance |
| `enable_artifacts` | Artifact collection | `true` | Feedback quality |
| `use_llm_feedback` | LLM code review | `false` | Quality + cost |
| `enable_migration` | Island migration | `true` | Diversity |
| `enable_embeddings` | Novelty detection | `false` | Diversity + cost |
| `template_stochasticity` | Random prompts | `false` | Exploration |

**Toggle:**
```yaml
evaluator:
  cascade_evaluation: true
  enable_artifacts: true
  use_llm_feedback: false

database:
  enable_migration: true
  enable_embeddings: false

prompt:
  use_template_stochasticity: false
```

### 5.2 Dynamic Feature Flags

**Not Currently Supported**

**Recommendation:** Add feature flag service integration (LaunchDarkly, etc.)

---

## 6. Deployment Patterns

### 6.1 Local Development

```bash
# Install
pip install -e ".[dev]"

# Run
python openevolve-run.py \
  examples/function_minimization/initial_program.py \
  examples/function_minimization/evaluator.py \
  --config examples/function_minimization/config.yaml \
  --iterations 100
```

**Pros:** Fast iteration, easy debugging  
**Cons:** Requires local setup

---

### 6.2 Docker

**Image:** `ghcr.io/codelion/openevolve:latest`

```bash
# Pull
docker pull ghcr.io/codelion/openevolve:latest

# Run
docker run --rm \
  -v $(pwd):/app \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  ghcr.io/codelion/openevolve:latest \
  examples/function_minimization/initial_program.py \
  examples/function_minimization/evaluator.py \
  --iterations 100
```

**Pros:** Reproducible, isolated  
**Cons:** Slightly slower, more complex

---

### 6.3 Cloud (AWS Example)

**EC2 Instance:**
```bash
# Launch t3.xlarge (4 vCPU, 16 GB RAM)
# Install dependencies
sudo yum install -y python3.10

# Install OpenEvolve
pip3 install openevolve

# Run
python3 -m openevolve.cli \
  initial_program.py \
  evaluator.py \
  --config config.yaml \
  --iterations 10000

# Copy results
aws s3 cp openevolve_output/ s3://my-bucket/ --recursive
```

**Cost Estimate:** ~$0.17/hour + LLM API costs

---

### 6.4 Kubernetes (Future)

**Not Currently Supported**

**Recommendation:** Add Helm chart and operator

```yaml
apiVersion: openevolve.io/v1
kind: EvolutionJob
metadata:
  name: optimize-algorithm
spec:
  initialProgram: "s3://bucket/program.py"
  evaluator: "s3://bucket/evaluator.py"
  config:
    maxIterations: 10000
    parallelism: 8
  resources:
    limits:
      cpu: "8"
      memory: "16Gi"
```

---

## 7. Operational Runbooks

### 7.1 Start New Evolution Run

```bash
# 1. Prepare inputs
cat initial_program.py
cat evaluator.py
cat config.yaml

# 2. Set API key
export OPENAI_API_KEY="your-key"

# 3. Run
python openevolve-run.py \
  initial_program.py \
  evaluator.py \
  --config config.yaml \
  --iterations 1000 \
  --output-dir ./run_$(date +%Y%m%d_%H%M%S)

# 4. Monitor
tail -f ./run_*/openevolve.log
```

---

### 7.2 Resume from Checkpoint

```bash
# 1. Locate checkpoint
ls -lh openevolve_output/checkpoints/

# 2. Resume
python openevolve-run.py \
  initial_program.py \
  evaluator.py \
  --config config.yaml \
  --checkpoint openevolve_output/checkpoints/checkpoint_500 \
  --iterations 1000

# Continues from iteration 501
```

---

### 7.3 Handle Out of Memory

**Symptoms:**
- Process killed (OOM)
- Slow performance
- Checkpoint files very large

**Resolution:**

1. **Reduce population:**
   ```yaml
   database:
     population_size: 250  # Was 500
   ```

2. **Reduce islands:**
   ```yaml
   database:
     num_islands: 3  # Was 5
   ```

3. **Enable artifact pruning:**
   ```yaml
   evaluator:
     artifact_threshold: 5000  # 5KB instead of 10KB
   ```

4. **Add swap:**
   ```bash
   sudo swapon -s
   ```

---

### 7.4 Handle API Rate Limits

**Symptoms:**
- HTTP 429 errors
- Slow iteration times
- LLM generation failures

**Resolution:**

1. **Reduce parallelism:**
   ```yaml
   evaluator:
     parallel_evaluations: 2  # Was 4
   ```

2. **Use slower model:**
   ```yaml
   llm:
     models:
       - name: "gemini-2.5-flash"  # Cheaper tier
   ```

3. **Add delay between calls:**
   ```yaml
   llm:
     timeout: 60  # Increase timeout
   ```

4. **Use OptiLLM for rate limiting:**
   ```bash
   optillm --port 8000 --rate-limit 10
   ```

---

### 7.5 Recover from Crash

```bash
# 1. Check last checkpoint
ls -lht openevolve_output/checkpoints/ | head

# 2. Verify checkpoint integrity
python -c "
from openevolve.database import ProgramDatabase
db = ProgramDatabase.load_from_file('checkpoints/checkpoint_450/database.json')
print(f'Programs: {len(db.programs)}')
"

# 3. Resume
python openevolve-run.py \
  initial_program.py \
  evaluator.py \
  --checkpoint openevolve_output/checkpoints/checkpoint_450 \
  --iterations 1000
```

---

## 8. Performance Tuning

### 8.1 Tuning Knobs

| Parameter | Effect | Recommendation |
|-----------|--------|----------------|
| `parallel_evaluations` | CPU usage | Match CPU cores |
| `population_size` | Memory + quality | 250-1000 |
| `num_islands` | Diversity vs overhead | 3-7 |
| `migration_interval` | Exploration | 10-50 generations |
| `cascade_evaluation` | Speed | Always enable |
| `checkpoint_interval` | Disk I/O | 25-100 iterations |

### 8.2 Optimization Checklist

**For Speed:**
- ✅ Enable cascade evaluation
- ✅ Use fast LLM model (Gemini Flash)
- ✅ Reduce population size
- ✅ Increase parallelism
- ✅ Optimize user evaluator code

**For Quality:**
- ✅ Increase population size
- ✅ Increase islands
- ✅ Enable embeddings (diversity)
- ✅ Use better LLM model (GPT-4, Gemini Pro)
- ✅ Enable LLM feedback

**For Cost:**
- ✅ Use cheaper model (Gemini Flash)
- ✅ Enable cascade (fewer LLM calls)
- ✅ Reduce iterations
- ✅ Use local models (Ollama)

---

## 9. Troubleshooting Guide

### 9.1 Common Issues

**Issue: "No module named 'openevolve'"**
```bash
# Solution: Install package
pip install openevolve
# Or for development
pip install -e .
```

**Issue: "Evaluation file not found"**
```bash
# Solution: Use absolute path
python openevolve-run.py \
  $(pwd)/initial_program.py \
  $(pwd)/evaluator.py
```

**Issue: "API key not found"**
```bash
# Solution: Set environment variable
export OPENAI_API_KEY="your-key"
```

**Issue: "Checkpoint corrupted"**
```bash
# Solution: Use earlier checkpoint
ls openevolve_output/checkpoints/
# Use checkpoint_N-1 instead
```

---

### 9.2 Debug Techniques

**Enable verbose output:**
```bash
python openevolve-run.py ... --verbose
```

**Test LLM connection:**
```python
from openevolve.llm.openai import OpenAILLM

llm = OpenAILLM(model="gemini-2.5-pro")
result = llm.generate("Say hello")
print(result)
```

**Test evaluator:**
```python
from openevolve.evaluator import Evaluator

evaluator = Evaluator(config, "evaluator.py")
result = evaluator.evaluate_program("test_program.py")
print(result)
```

---

## 10. Operational Checklist

### Pre-Launch
- [ ] Test LLM API connection
- [ ] Validate initial program syntax
- [ ] Test evaluator with initial program
- [ ] Review configuration
- [ ] Ensure sufficient disk space
- [ ] Set API key environment variable

### During Run
- [ ] Monitor logs for errors
- [ ] Check iteration progress
- [ ] Monitor system resources (htop)
- [ ] Verify checkpoints being created
- [ ] Track best score improvements

### Post-Run
- [ ] Review final results
- [ ] Analyze evolution traces
- [ ] Export best program
- [ ] Archive checkpoints
- [ ] Document findings

---

## 11. Incident Response

### Severity Levels

**P0 - Critical:**
- System crash with no checkpoint
- Data corruption
- Security breach

**P1 - High:**
- Repeated failures
- Performance degradation >50%
- Checkpoint failure

**P2 - Medium:**
- Single iteration failures
- Slow performance
- Warning logs

**P3 - Low:**
- Cosmetic issues
- Documentation errors

### Response Procedures

**P0/P1:**
1. Stop current run
2. Preserve logs and checkpoints
3. Identify root cause
4. Resume from last valid checkpoint
5. Document incident

**P2/P3:**
1. Log issue
2. Continue monitoring
3. Address in next maintenance window

---

**Conclusion:** OpenEvolve provides **strong operational capabilities** with excellent logging, checkpoint/resume, and configuration management. Primary gaps are in external monitoring integration and distributed tracing.
