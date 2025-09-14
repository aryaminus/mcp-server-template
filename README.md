# Memory Palace MCP Server 🏰

A revolutionary [FastMCP](https://github.com/jlowin/fastmcp) server that implements the ancient **Memory Palace** technique for spatial knowledge organization, enhanced with modern AI capabilities.

## 🧠 What is a Memory Palace?

The Memory Palace (Method of Loci) is an ancient mnemonic technique where you visualize a familiar location and place information at specific spots within it. This MCP server brings this powerful memory technique into the digital age, allowing AI assistants to help you:

- **Create Virtual Rooms** for organizing different topics
- **Store Memories Spatially** with 3D coordinates and visual anchors  
- **Take Memory Journeys** through your knowledge in a structured path
- **Search Spatially** - find information by location, keywords, or visual cues
- **Build Connected Knowledge** through room connections and relationships

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/aryaminus/memory-palace-mcp)

## Local Development

### Setup

Fork the repo, then run:

```bash
git clone https://github.com/aryaminus/memory-palace-mcp
cd memory-palace-mcp
conda create -n mcp-server python=3.13
conda activate mcp-server
pip install -r requirements.txt
```

### Test

```bash
python src/server.py
# then in another terminal run:
npx @modelcontextprotocol/inspector
```

Open http://localhost:3000 and connect to `http://localhost:8000/mcp` using "Streamable HTTP" transport (NOTE THE `/mcp`!).

## Deployment

### Option 1: One-Click Deploy
Click the "Deploy to Render" button above.

### Option 2: Manual Deployment
1. Fork this repository
2. Connect your GitHub account to Render
3. Create a new Web Service on Render
4. Connect your forked repository
5. Render will automatically detect the `render.yaml` configuration

Your server will be available at `https://your-service-name.onrender.com/mcp` (NOTE THE `/mcp`!)

## 🛠️ Available Tools

The Memory Palace MCP Server provides these powerful tools:

### 🏠 Room Management
- **`create_room`** - Create new rooms in your memory palace
- **`get_palace_overview`** - Get a complete overview of all rooms and statistics

### 🧭 Memory Operations  
- **`store_memory`** - Store information at specific 3D coordinates with visual anchors
- **`memory_journey`** - Take guided journeys through rooms, visiting memories in spatial order
- **`search_memories`** - Search across your entire palace using keywords or content

### 📊 Analytics
- **`get_server_info`** - Get detailed information about server capabilities

## 🎯 Example Usage

```python
# Create a room for learning Python
create_room(
    name="Python Library", 
    description="A cozy library for Python programming knowledge",
    connections=["Study Hall", "Code Workshop"]
)

# Store a memory about list comprehensions
store_memory(
    room="Python Library",
    content="List comprehensions: [x**2 for x in range(10)] creates squares 0-81",
    visual_anchor="Golden book on the left bookshelf, third shelf from top",
    x=2.0, y=3.0, z=1.5,
    keywords=["python", "lists", "comprehensions", "syntax"]
)

# Take a journey through your Python knowledge
memory_journey("Python Library", include_connections=True)

# Search for specific concepts
search_memories("comprehensions", room="Python Library")
```

## 🌟 Why Memory Palace?

This MCP server addresses a unique gap in knowledge management by:

1. **Spatial Intelligence**: Leverages how our brains naturally organize information in space
2. **Visual Memory**: Uses visual anchors to improve recall and retention
3. **Structured Learning**: Provides guided paths through complex information
4. **Personal Knowledge Graph**: Creates interconnected spaces of understanding
5. **AI-Enhanced**: Combines ancient techniques with modern AI assistance

Perfect for students, researchers, programmers, and anyone who wants to organize and recall information more effectively!

## How to Add Your New MCP to Poke

![Poke integration setup](poke-integration.png)

Want to integrate your Model Context Protocol (MCP) server with Poke?

Go to https://poke.com/settings/connections/integrations/new to add your MCP integration.
