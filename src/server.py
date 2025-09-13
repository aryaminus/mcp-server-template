#!/usr/bin/env python3
import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from fastmcp import FastMCP

# Initialize the Memory Palace MCP Server
mcp = FastMCP("Memory Palace MCP Server")

@dataclass
class MemoryLocation:
    """A location in the memory palace"""
    id: str
    room: str
    position: Dict[str, float]  # {x: float, y: float, z: float}
    visual_anchor: str
    content: str
    keywords: List[str]
    created_at: str
    last_accessed: str

@dataclass
class MemoryRoom:
    """A room in the memory palace"""
    name: str
    description: str
    locations: List[str]  # location IDs
    connections: List[str]  # connected room names

class MemoryPalaceStorage:
    """Simple file-based storage for memory palace data"""
    
    def __init__(self, storage_dir: str = "memory_palace_data"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        self.locations_file = os.path.join(storage_dir, "locations.json")
        self.rooms_file = os.path.join(storage_dir, "rooms.json")
        
    def load_locations(self) -> Dict[str, MemoryLocation]:
        """Load all memory locations"""
        if not os.path.exists(self.locations_file):
            return {}
        
        with open(self.locations_file, 'r') as f:
            data = json.load(f)
            
        return {
            loc_id: MemoryLocation(**loc_data) 
            for loc_id, loc_data in data.items()
        }
    
    def save_locations(self, locations: Dict[str, MemoryLocation]):
        """Save all memory locations"""
        data = {
            loc_id: asdict(location) 
            for loc_id, location in locations.items()
        }
        
        with open(self.locations_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_rooms(self) -> Dict[str, MemoryRoom]:
        """Load all rooms"""
        if not os.path.exists(self.rooms_file):
            return {}
            
        with open(self.rooms_file, 'r') as f:
            data = json.load(f)
            
        return {
            room_name: MemoryRoom(**room_data)
            for room_name, room_data in data.items()
        }
    
    def save_rooms(self, rooms: Dict[str, MemoryRoom]):
        """Save all rooms"""
        data = {
            room_name: asdict(room)
            for room_name, room in rooms.items()
        }
        
        with open(self.rooms_file, 'w') as f:
            json.dump(data, f, indent=2)

# Global storage instance
storage = MemoryPalaceStorage()

def generate_location_id(content: str, room: str) -> str:
    """Generate a unique ID for a memory location"""
    return hashlib.md5(f"{room}:{content}:{datetime.now()}".encode()).hexdigest()[:12]

@mcp.tool(description="Create a new room in your memory palace with a name, description, and optional connections to other rooms")
def create_room(name: str, description: str, connections: Optional[List[str]] = None) -> dict:
    """Create a new room in the memory palace"""
    rooms = storage.load_rooms()
    
    if name in rooms:
        return {"error": f"Room '{name}' already exists"}
    
    new_room = MemoryRoom(
        name=name,
        description=description,
        locations=[],
        connections=connections or []
    )
    
    rooms[name] = new_room
    storage.save_rooms(rooms)
    
    return {
        "success": True,
        "message": f"Room '{name}' created successfully",
        "room": asdict(new_room)
    }

@mcp.tool(description="Store a memory at a specific location in your memory palace with visual anchors and spatial positioning")
def store_memory(
    room: str, 
    content: str, 
    visual_anchor: str,
    x: float = 0.0, 
    y: float = 0.0, 
    z: float = 0.0,
    keywords: Optional[List[str]] = None
) -> dict:
    """Store a memory at a specific location in the memory palace"""
    
    rooms = storage.load_rooms()
    locations = storage.load_locations()
    
    if room not in rooms:
        return {"error": f"Room '{room}' doesn't exist. Create it first."}
    
    location_id = generate_location_id(content, room)
    now = datetime.now().isoformat()
    
    new_location = MemoryLocation(
        id=location_id,
        room=room,
        position={"x": x, "y": y, "z": z},
        visual_anchor=visual_anchor,
        content=content,
        keywords=keywords or [],
        created_at=now,
        last_accessed=now
    )
    
    locations[location_id] = new_location
    rooms[room].locations.append(location_id)
    
    storage.save_locations(locations)
    storage.save_rooms(rooms)
    
    return {
        "success": True,
        "message": f"Memory stored in '{room}' at position ({x}, {y}, {z})",
        "location_id": location_id,
        "location": asdict(new_location)
    }

@mcp.tool(description="Take a journey through your memory palace, visiting locations in a specific room or following connections between rooms")
def memory_journey(room: str, include_connections: bool = False) -> dict:
    """Take a journey through memories in a room"""
    
    rooms = storage.load_rooms()
    locations = storage.load_locations()
    
    if room not in rooms:
        return {"error": f"Room '{room}' doesn't exist"}
    
    current_room = rooms[room]
    journey_path = []
    
    # Sort locations by position for a natural journey
    room_locations = [
        locations[loc_id] for loc_id in current_room.locations 
        if loc_id in locations
    ]
    
    room_locations.sort(key=lambda loc: (loc.position["x"], loc.position["y"], loc.position["z"]))
    
    for location in room_locations:
        # Update last accessed time
        location.last_accessed = datetime.now().isoformat()
        
        journey_path.append({
            "location_id": location.id,
            "position": location.position,
            "visual_anchor": location.visual_anchor,
            "content": location.content,
            "keywords": location.keywords
        })
    
    # Save updated access times
    storage.save_locations(locations)
    
    result = {
        "room": room,
        "description": current_room.description,
        "journey_path": journey_path,
        "total_memories": len(journey_path)
    }
    
    if include_connections and current_room.connections:
        result["connected_rooms"] = current_room.connections
    
    return result

@mcp.tool(description="Search for memories across your memory palace using keywords, room names, or content text")
def search_memories(query: str, room: Optional[str] = None) -> dict:
    """Search for memories using keywords or content"""
    
    locations = storage.load_locations()
    results = []
    
    query_lower = query.lower()
    
    for location in locations.values():
        # Skip if room filter is specified and doesn't match
        if room and location.room != room:
            continue
            
        # Check if query matches content, keywords, or visual anchor
        matches = (
            query_lower in location.content.lower() or
            query_lower in location.visual_anchor.lower() or
            any(query_lower in keyword.lower() for keyword in location.keywords)
        )
        
        if matches:
            # Update last accessed
            location.last_accessed = datetime.now().isoformat()
            
            results.append({
                "location_id": location.id,
                "room": location.room,
                "position": location.position,
                "visual_anchor": location.visual_anchor,
                "content": location.content,
                "keywords": location.keywords,
                "relevance_score": len([
                    match for match in [
                        query_lower in location.content.lower(),
                        query_lower in location.visual_anchor.lower(),
                        any(query_lower in kw.lower() for kw in location.keywords)
                    ] if match
                ])
            })
    
    # Sort by relevance score
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    # Save updated access times
    storage.save_locations(locations)
    
    return {
        "query": query,
        "room_filter": room,
        "results_count": len(results),
        "results": results
    }

@mcp.tool(description="Get a complete overview of your memory palace including all rooms, their connections, and memory statistics")
def get_palace_overview() -> dict:
    """Get an overview of the entire memory palace"""
    
    rooms = storage.load_rooms()
    locations = storage.load_locations()
    
    room_stats = {}
    total_memories = len(locations)
    
    for room_name, room in rooms.items():
        room_location_count = len([
            loc for loc_id in room.locations 
            if loc_id in locations
        ])
        
        room_stats[room_name] = {
            "description": room.description,
            "memory_count": room_location_count,
            "connections": room.connections
        }
    
    # Recent activity
    recent_locations = sorted(
        locations.values(),
        key=lambda x: x.last_accessed,
        reverse=True
    )[:5]
    
    recent_activity = [
        {
            "location_id": loc.id,
            "room": loc.room,
            "visual_anchor": loc.visual_anchor,
            "last_accessed": loc.last_accessed
        }
        for loc in recent_locations
    ]
    
    return {
        "total_rooms": len(rooms),
        "total_memories": total_memories,
        "room_stats": room_stats,
        "recent_activity": recent_activity,
        "palace_health": "excellent" if total_memories > 0 else "empty"
    }

@mcp.tool(description="Get detailed information about the Memory Palace MCP server and its capabilities")
def get_server_info() -> dict:
    """Get information about the Memory Palace MCP server"""
    return {
        "server_name": "Memory Palace MCP Server",
        "version": "1.0.0",
        "description": "A spatial memory system using ancient memory palace techniques enhanced with AI",
        "capabilities": [
            "Create virtual rooms for organizing knowledge",
            "Store memories with spatial coordinates and visual anchors",
            "Take guided journeys through your knowledge",
            "Search memories across the entire palace",
            "Track memory access patterns and usage"
        ],
        "storage_type": "local_json",
        "environment": os.environ.get("ENVIRONMENT", "development"),
        "python_version": os.sys.version.split()[0]
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    
    print(f"Starting FastMCP server on {host}:{port}")
    
    mcp.run(
        transport="http",
        host=host,
        port=port
    )
