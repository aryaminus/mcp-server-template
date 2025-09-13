# Memory Palace MCP Demo 🏰

## Quick Demo Script

Here's a complete demonstration of the Memory Palace MCP Server, showing both the Python code for developers and the natural language prompts users would send:

### 1. Create Your First Room

**User would say:**
```
I want to make a memory room for my Python programming notes. Can you make it look like a beautiful library with big oak bookshelves?
```

**Backend code:**
```python
create_room(
    name="Python Library",
    description="A grand library dedicated to Python programming knowledge",
    connections=["Study Hall", "Code Workshop"]
)
```

### 2. Store Your First Memory

**User would say:**
```
I want to remember how to make list comprehensions in Python. Can you add this to my Python room? I'm picturing a golden book on the oak shelf at eye level.
```

**Backend code:**
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

**User would say:**
```
I also want to remember dictionary comprehensions in Python. I'm picturing a silver tablet on the marble reading desk.
```

**Backend code:**
```python
store_memory(
    room="Python Library", 
    content="Dictionary comprehensions: {k: v**2 for k, v in items.items()}",
    visual_anchor="Silver tablet resting on the marble reading desk",
    x=0.0, y=2.0, z=0.8,
    keywords=["python", "dict-comprehension", "mapping"]
)
```

**User would say:**
```
Can you also help me remember lambda functions? I'm thinking of a glowing scroll hanging on the east wall.
```

**Backend code:**
```python
store_memory(
    room="Python Library",
    content="Lambda functions: lambda x, y: x + y creates anonymous functions", 
    visual_anchor="Glowing scroll mounted on the eastern wall",
    x=4.0, y=1.0, z=1.2,
    keywords=["python", "lambda", "functions", "anonymous"]
)
```

### 4. Take a Memory Journey

**User would say:**
```
Can we take a walk through my Python Library to see what I've saved there?
```

**Backend code:**
```python
memory_journey("Python Library", include_connections=True)
```

**System response to user:**
```
🧭 Ready for an exploration of your Python Library? Let's go!

Journey through Python Library (mastery level: 10%):

1. At the marble reading desk: Silver tablet resting on the marble reading desk
   Content: "Dictionary comprehensions: {k: v**2 for k, v in items.items()}"
   Keywords: python, dict-comprehension, mapping

2. At the oak bookshelf: Golden leather-bound book on the oak shelf
   Content: "List comprehensions create new lists: [x**2 for x in range(5)] = [0,1,4,9,16]"
   Keywords: python, list-comprehension, syntax, squares

3. On the eastern wall: Glowing scroll mounted on the eastern wall
   Content: "Lambda functions: lambda x, y: x + y creates anonymous functions"
   Keywords: python, lambda, functions, anonymous

Total memories: 3
+15 XP gained!

Connected rooms: Study Hall, Code Workshop

Woohoo! 1 day of adventure! Your memory map gets bigger every day!
```

### 5. Search Your Palace

**User would say:**
```
Can you help me find anything about comprehensions in my memory palace?
```

**Backend code:**
```python
search_memories("comprehensions")
```

**System response to user:**
```
🔍 I found something in your memory palace!

Found 2 results for "comprehensions":

1. Room: Python Library
   Visual anchor: Silver tablet resting on the marble reading desk
   Content: Dictionary comprehensions: {k: v**2 for k, v in items.items()}
   Keywords: python, dict-comprehension, mapping

2. Room: Python Library
   Visual anchor: Golden leather-bound book on the oak shelf
   Content: List comprehensions create new lists: [x**2 for x in range(5)] = [0,1,4,9,16]
   Keywords: python, list-comprehension, syntax, squares

+8 XP gained!
```

### 6. Get Palace Overview

**User would say:**
```
Can I see a map of my whole memory palace?
```

**Backend code:**
```python
get_palace_overview()
```

**System response to user:**
```
🏰 Memory Palace Overview:

Total rooms: 1
Total memories: 3
Overall mastery: 10%

Room stats:
- Python Library:
  Description: A grand library dedicated to Python programming knowledge
  Memory count: 3
  Connections: Study Hall, Code Workshop

Recent activity:
- Room: Python Library
  Visual anchor: Glowing scroll mounted on the eastern wall
  Last accessed: Just now

User stats:
Level: 2
XP: 53/150 to next level
Streak days: 1
Personality: Explorer (🧭)
Total achievements: 2/10

Woohoo! 1 day of adventure! Your memory map gets bigger every day!
```

## 🌟 Advanced Use Cases

### Building a Computer Science Palace

**User conversations might look like:**
```
I want to create rooms for different computer science topics. Can I have a Data Structures Hall with trees and arrays?

Can you add another room called Algorithms Workshop for sorting and searching? It should connect to my Data Structures Hall.

I'd like one more room called Systems Laboratory for operating systems and networking. Connect it to the Algorithms Workshop.

Let me add something about binary trees to my Data Structures Hall. I'm picturing a big old oak tree in the center courtyard.

Now I want to add something about quicksort to my Algorithms Workshop. I'm thinking of a blacksmith's forge where the hammering looks like the recursive steps of the algorithm.
```

**Backend code:**
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

**User conversations might look like:**
```
I want to make rooms for my math classes. First, can I have an Algebra Garden with flowers arranged in equations?

Now I want to add a Calculus Observatory where I can look at functions changing. Connect it to my Algebra Garden.

For my statistics class, can I have a Statistics Laboratory connected to the Calculus Observatory?
```

**Backend code:**
```python
# Mathematics progression
create_room("Algebra Garden", "Peaceful garden for basic algebra")
create_room("Calculus Observatory", "Observatory for limits and derivatives", ["Algebra Garden"])  
create_room("Statistics Laboratory", "Lab for probability and inference", ["Calculus Observatory"])

# Each concept builds spatially on the last
```

## 🎯 Integration with Poke

The Memory Palace integrates beautifully with Poke's SMS system, with friendly messages like:

1. **Study Reminders**: "Hey there! 👋 Time to visit your Python Library and review what you've learned!"

2. **Spaced Repetition**: "Memory game time! 🎮 Can you remember what you stored at the golden book on the oak shelf?"

3. **Knowledge Retrieval**: 
   User: "I forgot how lambda functions work in Python"
   System: "I found that in your Python Library! It's on the glowing scroll on the eastern wall: Lambda functions: lambda x, y: x + y creates anonymous functions"

4. **Progress Tracking**: "Amazing work! 🎉 You've learned 15 things in your Data Structures Hall! Keep it up!"

This creates a **friendly memory helper** that makes learning more fun and helps you remember things better!