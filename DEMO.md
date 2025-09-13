# Memory Palace MCP Demo 🏰

## Quick Demo Script

Here's a complete demonstration of the Memory Palace MCP Server:

### 1. Create Your First Room
```python
create_room(
    name="Python Library",
    description="A grand library dedicated to Python programming knowledge",
    connections=["Study Hall", "Code Workshop"]
)
```

### 2. Store Your First Memory
```python
store_memory(
    room="Python Library",
    content="List comprehensions create new lists: [x**2 for x in range(5)] = [0,1,4,9,16]",
    visual_anchor="Golden leather-bound book on the oak shelf, eye-level, third from left",
    x=2.5, y=1.8, z=0.0,
    keywords=["python", "list-comprehension", "syntax", "squares"]
)
```

### 3. Add More Knowledge
```python
store_memory(
    room="Python Library", 
    content="Dictionary comprehensions: {k: v**2 for k, v in items.items()}",
    visual_anchor="Silver tablet resting on the marble reading desk",
    x=0.0, y=2.0, z=0.8,
    keywords=["python", "dict-comprehension", "mapping"]
)

store_memory(
    room="Python Library",
    content="Lambda functions: lambda x, y: x + y creates anonymous functions", 
    visual_anchor="Glowing scroll mounted on the eastern wall",
    x=4.0, y=1.0, z=1.2,
    keywords=["python", "lambda", "functions", "anonymous"]
)
```

### 4. Take a Memory Journey
```python
memory_journey("Python Library", include_connections=True)
```

**Expected Output:**
```json
{
  "room": "Python Library",
  "description": "A grand library dedicated to Python programming knowledge", 
  "journey_path": [
    {
      "location_id": "abc123def456",
      "position": {"x": 0.0, "y": 2.0, "z": 0.8},
      "visual_anchor": "Silver tablet resting on the marble reading desk",
      "content": "Dictionary comprehensions: {k: v**2 for k, v in items.items()}",
      "keywords": ["python", "dict-comprehension", "mapping"]
    },
    {
      "location_id": "def456ghi789", 
      "position": {"x": 2.5, "y": 1.8, "z": 0.0},
      "visual_anchor": "Golden leather-bound book on the oak shelf",
      "content": "List comprehensions create new lists: [x**2 for x in range(5)]",
      "keywords": ["python", "list-comprehension", "syntax", "squares"]
    },
    {
      "location_id": "ghi789jkl012",
      "position": {"x": 4.0, "y": 1.0, "z": 1.2}, 
      "visual_anchor": "Glowing scroll mounted on the eastern wall",
      "content": "Lambda functions: lambda x, y: x + y creates anonymous functions",
      "keywords": ["python", "lambda", "functions", "anonymous"]
    }
  ],
  "total_memories": 3,
  "connected_rooms": ["Study Hall", "Code Workshop"]
}
```

### 5. Search Your Palace
```python
search_memories("comprehensions")
```

**Expected Output:**
```json
{
  "query": "comprehensions",
  "results_count": 2,
  "results": [
    {
      "location_id": "abc123def456",
      "room": "Python Library", 
      "position": {"x": 0.0, "y": 2.0, "z": 0.8},
      "visual_anchor": "Silver tablet resting on the marble reading desk",
      "content": "Dictionary comprehensions: {k: v**2 for k, v in items.items()}",
      "keywords": ["python", "dict-comprehension", "mapping"],
      "relevance_score": 2
    },
    {
      "location_id": "def456ghi789",
      "room": "Python Library",
      "position": {"x": 2.5, "y": 1.8, "z": 0.0}, 
      "visual_anchor": "Golden leather-bound book on the oak shelf",
      "content": "List comprehensions create new lists: [x**2 for x in range(5)]",
      "keywords": ["python", "list-comprehension", "syntax", "squares"],
      "relevance_score": 2
    }
  ]
}
```

### 6. Get Palace Overview
```python
get_palace_overview()
```

**Expected Output:**
```json
{
  "total_rooms": 1,
  "total_memories": 3,
  "room_stats": {
    "Python Library": {
      "description": "A grand library dedicated to Python programming knowledge",
      "memory_count": 3,
      "connections": ["Study Hall", "Code Workshop"] 
    }
  },
  "recent_activity": [
    {
      "location_id": "ghi789jkl012",
      "room": "Python Library", 
      "visual_anchor": "Glowing scroll mounted on the eastern wall",
      "last_accessed": "2025-09-13T15:30:45.123456"
    }
  ],
  "palace_health": "excellent"
}
```

## 🌟 Advanced Use Cases

### Building a Computer Science Palace
```python
# Create connected learning spaces
create_room("Data Structures Hall", "Hall of arrays, trees, and graphs")
create_room("Algorithms Workshop", "Workshop for sorting and searching", ["Data Structures Hall"])
create_room("Systems Laboratory", "Lab for OS and networking concepts", ["Algorithms Workshop"])

# Store interconnected knowledge
store_memory("Data Structures Hall", "Binary trees: left < parent < right", 
            "Ancient oak tree in the center courtyard", x=0, y=0, z=0)
            
store_memory("Algorithms Workshop", "Quicksort: divide-and-conquer O(n log n)",
            "Blacksmith's forge with recursive hammering", x=1, y=0, z=0)
```

### Personal Learning Journey
```python
# Mathematics progression
create_room("Algebra Garden", "Peaceful garden for basic algebra")
create_room("Calculus Observatory", "Observatory for limits and derivatives", ["Algebra Garden"])  
create_room("Statistics Laboratory", "Lab for probability and inference", ["Calculus Observatory"])

# Each concept builds spatially on the last
```

## 🎯 Integration with Poke

The Memory Palace integrates beautifully with Poke's SMS system:

1. **Study Reminders**: "Time to visit your Python Library! 📚"
2. **Spaced Repetition**: "Quick quiz: What's at coordinates (2.5, 1.8, 0.0)?"
3. **Knowledge Retrieval**: "SMS: 'Find lambda functions' → Returns spatial location + content"
4. **Progress Tracking**: "You've mastered 15 concepts in your Data Structures Hall! 🏆"

This creates a **personal knowledge assistant** that uses spatial memory to enhance learning and retention!