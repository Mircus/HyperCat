# HyperCat Agents DSL User Guide

A comprehensive guide to building and composing categorical agents using the HyperCat functional DSL.

## 🎯 Overview

HyperCat Agents provide a mathematically rigorous approach to agent composition using category theory. Agents are categorical objects with tools, beliefs, and memory, composed via morphisms that preserve mathematical structure.

## 🏗️ Basic Agent Construction

### Creating Simple Agents

```python
from hypercat_agents import agent_obj, with_tools, with_beliefs, with_memory, pipe

# Create a basic agent
analyzer = agent_obj("Analyzer")

# Add capabilities functionally using pipe
reasoning_agent = pipe(
    agent_obj("ReasoningAgent"),
    with_tools(logic_tool, inference_tool),
    with_beliefs("logic", ["use formal reasoning", "check consistency"]),
    with_memory("session_start", {"initialized": True, "confidence": 0.8}),
    with_arity(1)  # Can process 1 input at a time
)

print(f"Agent: {reasoning_agent.name}")
print(f"Tools: {len(reasoning_agent.tools)}")
print(f"Beliefs: {reasoning_agent.beliefs}")
```

### Agent Properties

```python
# Agents are immutable and composable
agent = pipe(
    agent_obj("MyAgent"),
    with_arity(2),  # Operadic arity - how many inputs it can handle
    with_beliefs("domain", ["expert knowledge", "best practices"]),
    with_memory("t0", {"state": "ready"})
)

# Access properties
print(f"Arity: {agent.operadic_arity}")
print(f"Belief contexts: {list(agent.beliefs.keys())}")
print(f"Memory points: {list(agent.memory.keys())}")
```

## 🏛️ Building Agent Categories

### Creating Categories with Multiple Agents

```python
from hypercat_agents import agent_category, agent_objects, agent_morphisms, operadic_compositions

# Build a category of reasoning agents
reasoning_category = pipe(
    agent_category("ReasoningAgents"),
    agent_objects(
        {"name": "Analyzer", "arity": 1, "beliefs": {"logic": ["formal reasoning"]}},
        {"name": "Synthesizer", "arity": 2, "beliefs": {"creativity": ["combine ideas"]}},
        {"name": "Critic", "arity": 1, "beliefs": {"evaluation": ["find flaws"]}}
    ),
    agent_morphisms(
        ("analyze", "Analyzer", "Synthesizer", "sequential"),
        ("synthesize", "Synthesizer", "Critic", "parallel"),
        ("critique", "Critic", "Analyzer", "sequential")
    ),
    operadic_compositions(
        {"inputs": ["Analyzer", "Synthesizer"], "output": "Critic", 
         "type": "sequential", "name": "reason_chain"}
    )
).build()

print(f"Category: {reasoning_category.name}")
print(f"Agents: {[obj.name for obj in reasoning_category.objects]}")
```

### Standard Agent Categories

```python
from hypercat_agents import StandardAgentCategories

# Pre-built categories for common use cases
reasoning_agents = StandardAgentCategories.reasoning_agents()
arc_solvers = StandardAgentCategories.arc_solving_agents()
collaborative_agents = StandardAgentCategories.collaborative_agents()

print("Available standard categories:")
for cat in [reasoning_agents, arc_solvers, collaborative_agents]:
    print(f"  {cat.name}: {[obj.name for obj in cat.objects]}")
```

## 🔗 Agent Composition

### Sequential Composition (f ; g ; h)

```python
from hypercat_agents import sequential_composition

# Create individual agents
pattern_detector = pipe(
    agent_obj("PatternDetector"),
    with_beliefs("patterns", ["detect symmetries", "find objects"]),
    with_arity(1)
)

rule_inferrer = pipe(
    agent_obj("RuleInferrer"), 
    with_beliefs("inference", ["generalize rules", "find mappings"]),
    with_arity(2)
)

grid_transformer = pipe(
    agent_obj("GridTransformer"),
    with_beliefs("transformation", ["apply operations", "modify grids"]),
    with_arity(1)
)

# Sequential composition: detector → inferrer → transformer
arc_pipeline = sequential_composition([pattern_detector, rule_inferrer, grid_transformer])

print(f"Pipeline: {arc_pipeline.name}")
print(f"Combined arity: {arc_pipeline.operadic_arity}")
print(f"Total tools: {len(arc_pipeline.tools)}")
```

### Parallel Composition (f ⊗ g ⊗ h)

```python
from hypercat_agents import parallel_composition

# Parallel composition: all agents work simultaneously
parallel_analysis = parallel_composition([pattern_detector, rule_inferrer, grid_transformer])

print(f"Parallel system: {parallel_analysis.name}")
print(f"Max arity: {parallel_analysis.operadic_arity}")  # Takes maximum arity
```

### Tree Composition (Binary Tree Structure)

```python
from hypercat_agents import tree_composition

# Tree composition: balanced binary tree structure
tree_system = tree_composition([pattern_detector, rule_inferrer, grid_transformer])

print(f"Tree system: {tree_system.name}")
print(f"Tree arity: {tree_system.operadic_arity}")
```

## 🧩 Specialized Example: ARC Puzzle Solving

### Building ARC Solver Category

```python
# Create ARC-specific tools (mock for demonstration)
class ARCTool:
    def __init__(self, name, description):
        self.name = name
        self.description = description

flood_fill_tool = ARCTool("flood_fill", "Fill connected regions")
reflect_tool = ARCTool("reflect_x", "Reflect along X axis")
color_shift_tool = ARCTool("color_shift", "Shift color mapping")

# Build ARC agents with domain-specific knowledge
arc_agents = [
    pipe(
        agent_obj("FloodFill"),
        with_tools(flood_fill_tool),
        with_beliefs("spatial", ["connected regions", "flooding algorithms"]),
        with_memory("last_op", "flood_fill_complete")
    ),
    pipe(
        agent_obj("ReflectX"),
        with_tools(reflect_tool),
        with_beliefs("geometric", ["symmetry", "reflection"]),
        with_memory("last_op", "reflection_complete")
    ),
    pipe(
        agent_obj("ColorShift"),
        with_tools(color_shift_tool),
        with_beliefs("color", ["mapping", "transformation"]),
        with_memory("last_op", "color_shift_complete")
    )
]

# Create ARC category with Tamari structure for different solution strategies
arc_category = pipe(
    agent_category("ARC_Solvers"),
    agent_objects(*[{"name": agent.name, "arity": agent.operadic_arity} for agent in arc_agents]),
    operadic_compositions(
        # Different bracketings represent different solution strategies
        {"inputs": ["FloodFill", "ReflectX", "ColorShift"], 
         "output": "ColorShift", "type": "sequential", "name": "strategy_1"},
        {"inputs": ["FloodFill", "ReflectX", "ColorShift"], 
         "output": "ColorShift", "type": "tree", "name": "strategy_2"}
    )
).build()
```

### Tamari Lattice Navigation for Strategy Search

```python
from hypercat_agents import FunctionalTamariMCTS

# Define evaluation function for ARC tasks
def evaluate_arc_strategy(agent_composition, task_data):
    """Evaluate how well a composition solves an ARC task"""
    if "sequential" in agent_composition.name.lower():
        return 0.7  # Sequential good for step-by-step
    elif "parallel" in agent_composition.name.lower():
        return 0.5  # Parallel for independent operations
    elif "tree" in agent_composition.name.lower():
        return 0.8  # Tree structure often optimal
    return 0.4

# Create Tamari-MCTS solver for strategy optimization
tamari_mcts = FunctionalTamariMCTS(arc_agents, evaluate_arc_strategy)

# Example ARC task
example_task = {
    "input": [[1, 0, 1], [0, 1, 0], [1, 0, 1]],
    "output": [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
}

# Search for optimal strategy
optimal_strategy = tamari_mcts.search_optimal_bracketing(
    tamari_mcts.bracketings[0],  # Start with first strategy
    example_task,
    iterations=50
)

print(f"Optimal strategy: {optimal_strategy.name}")
```

## 🎨 Advanced Composition Patterns

### Context-Dependent Beliefs (Sheaf Structure)

```python
# Agents can have different beliefs in different contexts
multi_context_agent = pipe(
    agent_obj("ContextualAgent"),
    with_beliefs("mathematics", ["formal proofs", "symbolic reasoning"]),
    with_beliefs("creativity", ["brainstorming", "lateral thinking"]),
    with_beliefs("analysis", ["critical evaluation", "systematic decomposition"])
)

# Access context-specific beliefs
math_beliefs = multi_context_agent.beliefs.get("mathematics", [])
creative_beliefs = multi_context_agent.beliefs.get("creativity", [])
```

### Time-Indexed Memory (Fibration Structure)

```python
# Agents maintain memory across different time points
temporal_agent = pipe(
    agent_obj("TemporalAgent"),
    with_memory("t0", {"state": "initialized", "confidence": 0.5}),
    with_memory("t1", {"state": "learning", "confidence": 0.7}),
    with_memory("t2", {"state": "expert", "confidence": 0.9})
)

# Access temporal memory
current_state = temporal_agent.memory.get("t2", {})
print(f"Current state: {current_state}")
```

### Operadic Arity and Multi-Input Agents

```python
# Agents with different input capabilities
unary_agent = pipe(agent_obj("Unary"), with_arity(1))      # Takes 1 input
binary_agent = pipe(agent_obj("Binary"), with_arity(2))    # Takes 2 inputs  
ternary_agent = pipe(agent_obj("Ternary"), with_arity(3))  # Takes 3 inputs

# Composition respects arity constraints
high_arity_system = sequential_composition([unary_agent, binary_agent, ternary_agent])
print(f"System arity: {high_arity_system.operadic_arity}")  # Sum of arities
```

## 🔍 Introspection and Analysis

### Agent State Inspection

```python
def inspect_agent(agent):
    """Inspect agent structure"""
    return {
        "name": agent.name,
        "arity": agent.operadic_arity,
        "tools": len(agent.tools),
        "belief_contexts": list(agent.beliefs.keys()),
        "memory_points": list(agent.memory.keys()),
        "total_beliefs": sum(len(beliefs) for beliefs in agent.beliefs.values())
    }

# Inspect complex composition
complex_agent = tree_composition([pattern_detector, rule_inferrer, grid_transformer])
analysis = inspect_agent(complex_agent)
print(f"Agent analysis: {analysis}")
```

### Category Analysis

```python
def analyze_category(category):
    """Analyze categorical structure"""
    return {
        "name": category.name,
        "objects": len(category.objects),
        "morphisms": len(category.morphisms),
        "agent_types": [obj.__class__.__name__ for obj in category.objects],
        "composition_types": [morph.data.get('type', 'unknown') 
                             for morph in category.morphisms if hasattr(morph, 'data')]
    }

category_info = analyze_category(reasoning_category)
print(f"Category structure: {category_info}")
```

## 🚀 Best Practices

### 1. Start Simple, Compose Complex

```python
# Build simple agents first
basic_agent = pipe(
    agent_obj("Basic"),
    with_arity(1),
    with_beliefs("core", ["fundamental principles"])
)

# Then compose into complex systems
complex_system = pipe(
    basic_agent,
    lambda agent: sequential_composition([agent, enhanced_agent, expert_agent])
)
```

### 2. Use Meaningful Names

```python
# Good: descriptive names
nlp_preprocessor = agent_obj("NLP_Preprocessor")
sentiment_analyzer = agent_obj("Sentiment_Analyzer") 
text_summarizer = agent_obj("Text_Summarizer")

# Better: compose into named pipeline
text_processing_pipeline = sequential_composition([
    nlp_preprocessor, sentiment_analyzer, text_summarizer
])
```

### 3. Leverage Category Structure

```python
# Build categories that reflect domain structure
nlp_category = pipe(
    agent_category("NLP_Pipeline"),
    agent_objects(nlp_preprocessor, sentiment_analyzer, text_summarizer),
    agent_morphisms(
        ("preprocess", "NLP_Preprocessor", "Sentiment_Analyzer", "sequential"),
        ("analyze", "Sentiment_Analyzer", "Text_Summarizer", "sequential")
    )
).build()
```

### 4. Use Appropriate Composition Types

```python
# Sequential: when order matters
sequential_composition([step1, step2, step3])

# Parallel: when independence is desired  
parallel_composition([independent1, independent2, independent3])

# Tree: when hierarchical structure is beneficial
tree_composition([base_skill1, base_skill2, meta_skill])
```

## 📖 Quick Reference

### Core Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `agent_obj(name)` | Create agent | `agent_obj("MyAgent")` |
| `with_tools(*tools)` | Add tools | `with_tools(tool1, tool2)` |
| `with_beliefs(context, beliefs)` | Add beliefs | `with_beliefs("logic", ["reasoning"])` |
| `with_memory(time, data)` | Add memory | `with_memory("t0", {"state": "ready"})` |
| `with_arity(n)` | Set arity | `with_arity(2)` |
| `sequential_composition(agents)` | Sequential | `sequential_composition([a, b, c])` |
| `parallel_composition(agents)` | Parallel | `parallel_composition([a, b, c])` |
| `tree_composition(agents)` | Tree | `tree_composition([a, b, c])` |
| `pipe(initial, *funcs)` | Function composition | `pipe(agent, with_tools(t), with_arity(1))` |

### Category Builders

| Function | Purpose | Example |
|----------|---------|---------|
| `agent_category(name)` | Start category | `agent_category("MyCategory")` |
| `agent_objects(*specs)` | Add objects | `agent_objects(agent1, agent2)` |
| `agent_morphisms(*specs)` | Add morphisms | `agent_morphisms(("f", "A", "B"))` |
| `operadic_compositions(*specs)` | Add compositions | `operadic_compositions({...})` |

This guide provides the foundation for building sophisticated agent systems using categorical composition. The mathematical rigor ensures predictable behavior while the functional DSL keeps code clean and composable.