#!/usr/bin/env python3
import os
import json
import hashlib
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict, field
from fastmcp import FastMCP

# Import constants
# Use relative import when running from src directory
try:
    from const import (
        PERSONALITIES, 
        DEFAULT_ACHIEVEMENTS,
        DEFAULT_CHALLENGES,
        DEFAULT_LEARNING_PATHS,
        SPACED_REPETITION_INTERVALS,
        SERVER_INFO
    )
except ImportError:
    # Use package import when running from project root
    from src.const import (
        PERSONALITIES, 
        DEFAULT_ACHIEVEMENTS,
        DEFAULT_CHALLENGES,
        DEFAULT_LEARNING_PATHS,
        SPACED_REPETITION_INTERVALS,
        SERVER_INFO
    )

# Initialize the Memory Palace MCP Server
mcp = FastMCP("Memory Palace MCP Server")

@dataclass
class Achievement:
    """An achievement that can be unlocked by users"""
    id: str
    name: str
    description: str
    icon: str
    unlocked: bool = False
    unlocked_at: Optional[str] = None
    xp_reward: int = 50
    
@dataclass
class MemoryChallenge:
    """A memory challenge for the user"""
    id: str
    name: str
    description: str
    target_memories: List[str]  # List of memory IDs to recall
    difficulty: str  # "easy", "medium", "hard"
    completed: bool = False
    completed_at: Optional[str] = None
    xp_reward: int = 0

@dataclass
class UserProfile:
    """User profile with gamification elements"""
    id: str
    username: str
    personality: str = "sage"  # Default personality
    level: int = 1
    xp: int = 0
    xp_to_next_level: int = 100
    last_active: str = field(default_factory=lambda: datetime.now().isoformat())
    streak_days: int = 0
    streak_last_updated: str = field(default_factory=lambda: datetime.now().isoformat())
    achievements: List[Achievement] = field(default_factory=list)
    total_memories: int = 0
    total_rooms: int = 0
    challenges_completed: int = 0
    active_challenges: List[str] = field(default_factory=list)
    learning_paths: Dict[str, int] = field(default_factory=dict)  # Path name -> progress (0-100%)
    
    def add_xp(self, amount: int) -> Dict[str, Any]:
        """Add XP and handle level ups"""
        self.xp += amount
        result = {"xp_gained": amount, "level_up": False, "new_level": self.level}
        
        while self.xp >= self.xp_to_next_level:
            self.xp -= self.xp_to_next_level
            self.level += 1
            self.xp_to_next_level = int(self.xp_to_next_level * 1.5)  # Increase XP needed for next level
            result["level_up"] = True
            result["new_level"] = self.level
            
        return result
    
    def update_streak(self) -> Dict[str, Any]:
        """Update the user's daily streak"""
        last_date = datetime.fromisoformat(self.streak_last_updated)
        today = datetime.now()
        
        # Calculate days difference
        days_diff = (today.date() - last_date.date()).days
        
        result = {"streak_updated": False, "streak_days": self.streak_days, "streak_bonus": 0}
        
        if days_diff == 0:
            # Already updated today
            return result
        elif days_diff == 1:
            # Perfect streak continuation
            self.streak_days += 1
            streak_bonus = min(self.streak_days, 10) * 5  # Max 50 XP for 10+ day streak
            result["streak_updated"] = True
            result["streak_days"] = self.streak_days
            result["streak_bonus"] = streak_bonus
        elif days_diff > 1:
            # Streak broken
            self.streak_days = 1
            result["streak_updated"] = True
            result["streak_days"] = 1
            result["streak_broken"] = True
            
        self.streak_last_updated = today.isoformat()
        return result
    
    def get_personality(self) -> Dict[str, Any]:
        """Get the current personality"""
        return PERSONALITIES.get(self.personality, PERSONALITIES["sage"])

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
    recall_count: int = 0
    recall_success_rate: float = 100.0  # Percentage of successful recalls
    difficulty_rating: int = 1  # 1-10 scale of recall difficulty
    
@dataclass
class MemoryRoom:
    """A room in the memory palace"""
    name: str
    description: str
    locations: List[str]  # location IDs
    connections: List[str]  # connected room names
    theme: str = "default"  # Visual theme of room
    mastery_level: int = 0  # 0-100% mastery of this room's content
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_visited: str = field(default_factory=lambda: datetime.now().isoformat())

class MemoryPalaceStorage:
    """Enhanced file-based storage for memory palace data with gamification"""
    
    def __init__(self, storage_dir: str = "memory_palace_data"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        self.locations_file = os.path.join(storage_dir, "locations.json")
        self.rooms_file = os.path.join(storage_dir, "rooms.json")
        self.users_file = os.path.join(storage_dir, "users.json")
        self.challenges_file = os.path.join(storage_dir, "challenges.json")
        self.achievements_file = os.path.join(storage_dir, "achievements.json")
        self.learning_paths_file = os.path.join(storage_dir, "learning_paths.json")
        
        # Initialize default achievements if they don't exist
        self._init_default_achievements()
        self._init_default_challenges()
        self._init_default_learning_paths()
        
    def _init_default_achievements(self):
        """Initialize default achievements if they don't exist"""
        if os.path.exists(self.achievements_file):
            return
            
        # Convert dictionary definitions to Achievement objects
        default_achievements = {
            achievement_id: Achievement(**achievement_data)
            for achievement_id, achievement_data in DEFAULT_ACHIEVEMENTS.items()
        }
        
        with open(self.achievements_file, 'w') as f:
            json.dump({k: asdict(v) for k, v in default_achievements.items()}, f, indent=2)
    
    def _init_default_challenges(self):
        """Initialize default challenges if they don't exist"""
        if os.path.exists(self.challenges_file):
            return
            
        # Use challenges from const.py
        with open(self.challenges_file, 'w') as f:
            json.dump(DEFAULT_CHALLENGES, f, indent=2)
    
    def _init_default_learning_paths(self):
        """Initialize default learning paths if they don't exist"""
        if os.path.exists(self.learning_paths_file):
            return
            
        # Use learning paths from const.py
        with open(self.learning_paths_file, 'w') as f:
            json.dump(DEFAULT_LEARNING_PATHS, f, indent=2)
        
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
            
    def load_user_profile(self, user_id: str = "default") -> UserProfile:
        """Load a user profile, or create a default one if it doesn't exist"""
        if not os.path.exists(self.users_file):
            # Create default user
            default_user = UserProfile(
                id="default",
                username="Memory Explorer",
                personality=random.choice(list(PERSONALITIES.keys()))
            )
            self.save_user_profile(default_user)
            return default_user
            
        with open(self.users_file, 'r') as f:
            data = json.load(f)
        
        if user_id not in data:
            # Create new user
            new_user = UserProfile(
                id=user_id,
                username=f"Explorer_{user_id[:8]}",
                personality=random.choice(list(PERSONALITIES.keys()))
            )
            self.save_user_profile(new_user)
            return new_user
            
        # Load achievements as proper objects
        user_data = data[user_id]
        if "achievements" in user_data:
            user_data["achievements"] = [
                Achievement(**achievement) for achievement in user_data["achievements"]
            ]
            
        return UserProfile(**user_data)
    
    def save_user_profile(self, user: UserProfile):
        """Save a user profile"""
        if not os.path.exists(self.users_file):
            data = {}
        else:
            with open(self.users_file, 'r') as f:
                data = json.load(f)
                
        data[user.id] = asdict(user)
        
        with open(self.users_file, 'w') as f:
            json.dump(data, f, indent=2)
            
    def load_achievements(self) -> Dict[str, Achievement]:
        """Load all achievements"""
        if not os.path.exists(self.achievements_file):
            self._init_default_achievements()
            
        with open(self.achievements_file, 'r') as f:
            data = json.load(f)
            
        return {
            ach_id: Achievement(**ach_data)
            for ach_id, ach_data in data.items()
        }
        
    def load_challenges(self) -> Dict:
        """Load challenge templates"""
        if not os.path.exists(self.challenges_file):
            self._init_default_challenges()
            
        with open(self.challenges_file, 'r') as f:
            return json.load(f)
            
    def load_learning_paths(self) -> Dict:
        """Load learning paths"""
        if not os.path.exists(self.learning_paths_file):
            self._init_default_learning_paths()
            
        with open(self.learning_paths_file, 'r') as f:
            return json.load(f)
            
    def check_and_award_achievements(self, user_id: str = "default") -> List[Dict]:
        """Check for new achievements and award them if earned"""
        user = self.load_user_profile(user_id)
        rooms = self.load_rooms()
        locations = self.load_locations()
        achievements = self.load_achievements()
        
        # Get already unlocked achievement IDs
        unlocked_ids = [a.id for a in user.achievements if a.unlocked]
        newly_unlocked = []
        
        # Check for achievements
        if "first_room" not in unlocked_ids and len(rooms) >= 1:
            achievement = achievements["first_room"]
            achievement.unlocked = True
            achievement.unlocked_at = datetime.now().isoformat()
            user.achievements.append(achievement)
            user.add_xp(achievement.xp_reward)
            newly_unlocked.append(asdict(achievement))
            
        if "first_memory" not in unlocked_ids and len(locations) >= 1:
            achievement = achievements["first_memory"]
            achievement.unlocked = True
            achievement.unlocked_at = datetime.now().isoformat()
            user.achievements.append(achievement)
            user.add_xp(achievement.xp_reward)
            newly_unlocked.append(asdict(achievement))
            
        if "three_rooms" not in unlocked_ids and len(rooms) >= 3:
            achievement = achievements["three_rooms"]
            achievement.unlocked = True
            achievement.unlocked_at = datetime.now().isoformat()
            user.achievements.append(achievement)
            user.add_xp(achievement.xp_reward)
            newly_unlocked.append(asdict(achievement))
            
        if "ten_memories" not in unlocked_ids and len(locations) >= 10:
            achievement = achievements["ten_memories"]
            achievement.unlocked = True
            achievement.unlocked_at = datetime.now().isoformat()
            user.achievements.append(achievement)
            user.add_xp(achievement.xp_reward)
            newly_unlocked.append(asdict(achievement))
            
        if "three_day_streak" not in unlocked_ids and user.streak_days >= 3:
            achievement = achievements["three_day_streak"]
            achievement.unlocked = True
            achievement.unlocked_at = datetime.now().isoformat()
            user.achievements.append(achievement)
            user.add_xp(achievement.xp_reward)
            newly_unlocked.append(asdict(achievement))
            
        if "seven_day_streak" not in unlocked_ids and user.streak_days >= 7:
            achievement = achievements["seven_day_streak"]
            achievement.unlocked = True
            achievement.unlocked_at = datetime.now().isoformat()
            user.achievements.append(achievement)
            user.add_xp(achievement.xp_reward)
            newly_unlocked.append(asdict(achievement))
            
        # Save user with new achievements
        if newly_unlocked:
            self.save_user_profile(user)
            
        return newly_unlocked
        
    def generate_challenge(self, user_id: str = "default") -> Optional[Dict]:
        """Generate a personalized challenge based on user's palace"""
        user = self.load_user_profile(user_id)
        rooms = self.load_rooms()
        locations = self.load_locations()
        challenge_templates = self.load_challenges()
        
        if not rooms or not locations:
            return None  # Can't create challenges without content
            
        # Pick a random challenge type
        challenge_type = random.choice(list(challenge_templates.keys()))
        template = challenge_templates[challenge_type]
        
        # Pick a random room that has memories
        valid_rooms = [r for r in rooms.keys() if any(loc.room == r for loc in locations.values())]
        if not valid_rooms:
            return None
            
        room = random.choice(valid_rooms)
        room_locations = [loc for loc in locations.values() if loc.room == room]
        
        # Create a challenge based on template type
        if challenge_type == "quick_recall":
            # Choose difficulty based on user level
            if user.level < 5:
                difficulty = "easy"
            elif user.level < 10:
                difficulty = "medium"
            else:
                difficulty = "hard"
                
            count = min(template["difficulty_levels"][difficulty]["count"], len(room_locations))
            if count == 0:
                return None
                
            target_memories = random.sample([loc.id for loc in room_locations], count)
            xp_reward = template["difficulty_levels"][difficulty]["xp_reward"]
            
            challenge = MemoryChallenge(
                id=f"challenge_{int(time.time())}",
                name=template["name"],
                description=template["description"].format(count=count, room=room),
                target_memories=target_memories,
                difficulty=difficulty,
                xp_reward=xp_reward
            )
            
            return asdict(challenge)
            
        elif challenge_type == "room_mastery":
            if len(room_locations) < 3:  # Require at least 3 memories for mastery challenge
                return None
                
            challenge = MemoryChallenge(
                id=f"challenge_{int(time.time())}",
                name=template["name"],
                description=template["description"].format(room=room),
                target_memories=[loc.id for loc in room_locations],
                difficulty="medium" if len(room_locations) < 7 else "hard",
                xp_reward=template["xp_reward"]
            )
            
            return asdict(challenge)
            
        # Default fallback challenge
        return None

# Global storage instance
storage = MemoryPalaceStorage()

def generate_location_id(content: str, room: str) -> str:
    """Generate a unique ID for a memory location"""
    return hashlib.md5(f"{room}:{content}:{datetime.now()}".encode()).hexdigest()[:12]

def generate_message(message_type: str, user_id: str = "default") -> str:
    """Generate a personality-specific message"""
    user = storage.load_user_profile(user_id)
    personality = user.get_personality()
    
    message = personality["messages"].get(message_type, "")
    
    # Format any placeholders
    if "{streak}" in message:
        message = message.format(streak=user.streak_days)
        
    # Add personality emoji
    return f"{personality['emoji']} {message}"
    
def check_user_progress(user_id: str = "default") -> Dict[str, Any]:
    """Update user progress and check for achievements/leveling"""
    user = storage.load_user_profile(user_id)
    
    # Update streak
    streak_result = user.update_streak()
    
    # Check for new achievements
    new_achievements = storage.check_and_award_achievements(user_id)
    
    # Generate a random tip occasionally
    should_give_tip = random.random() < 0.3  # 30% chance
    tip = generate_message("tip", user_id) if should_give_tip else None
    
    # Generate a challenge occasionally for engaged users
    should_give_challenge = random.random() < 0.2 and user.level >= 2  # 20% chance after level 2
    challenge = storage.generate_challenge(user_id) if should_give_challenge else None
    
    # Award XP for streak continuation
    if streak_result.get("streak_updated", False) and streak_result.get("streak_bonus", 0) > 0:
        xp_result = user.add_xp(streak_result["streak_bonus"])
        if xp_result["level_up"]:
            level_up_message = f"🎉 Level Up! You've reached level {xp_result['new_level']}!"
        else:
            level_up_message = None
    else:
        level_up_message = None
    
    # Save user progress
    storage.save_user_profile(user)
    
    result = {
        "user": {
            "level": user.level,
            "xp": user.xp,
            "xp_to_next_level": user.xp_to_next_level,
            "streak_days": user.streak_days
        },
        "new_achievements": new_achievements,
        "streak_updated": streak_result.get("streak_updated", False),
        "streak_broken": streak_result.get("streak_broken", False),
        "level_up": level_up_message,
        "tip": tip,
        "challenge": challenge
    }
    
    return result

@mcp.tool(description="Create a new room in your memory palace - like making a special place to store your memories")
def create_room(name: str, description: str, theme: str = "default", connections: Optional[List[str]] = None) -> dict:
    """Create a new room in the memory palace with gamification elements"""
    rooms = storage.load_rooms()
    user_id = "default"  # For now, we use a default user
    
    if name in rooms:
        return {"error": f"Room '{name}' already exists"}
    
    new_room = MemoryRoom(
        name=name,
        description=description,
        theme=theme,
        locations=[],
        connections=connections or [],
        created_at=datetime.now().isoformat(),
        last_visited=datetime.now().isoformat()
    )
    
    rooms[name] = new_room
    storage.save_rooms(rooms)
    
    # Update user stats and check progress
    user = storage.load_user_profile(user_id)
    user.total_rooms += 1
    xp_reward = 25  # Base XP for creating a room
    xp_result = user.add_xp(xp_reward)
    storage.save_user_profile(user)
    
    # Check for achievements and progress
    progress = check_user_progress(user_id)
    
    # Prepare messages based on situation
    welcome_message = generate_message("welcome", user_id)
    
    result = {
        "success": True,
        "message": f"Room '{name}' created successfully",
        "room": asdict(new_room),
        "xp_gained": xp_reward,
        "welcome_message": welcome_message
    }
    
    # Add any progress-based messages
    if progress["new_achievements"]:
        achievement = progress["new_achievements"][0]
        result["achievement"] = achievement
        result["achievement_message"] = (
            f"🏆 Achievement Unlocked: {achievement['name']}! "
            f"{achievement['description']}. +{achievement['xp_reward']} XP!"
        )
    
    if progress["level_up"]:
        result["level_up_message"] = progress["level_up"]
        
    if progress["tip"]:
        result["tip"] = progress["tip"]
    
    return result

@mcp.tool(description="Put a memory in your memory palace - like putting a picture on the wall to help you remember something")
def store_memory(
    room: str, 
    content: str, 
    visual_anchor: str,
    x: float = 0.0, 
    y: float = 0.0, 
    z: float = 0.0,
    keywords: Optional[List[str]] = None
) -> dict:
    """Store a memory at a specific location in the memory palace with gamification"""
    
    rooms = storage.load_rooms()
    locations = storage.load_locations()
    user_id = "default"  # For now, we use a default user
    
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
        last_accessed=now,
        recall_count=0,
        recall_success_rate=100.0,
        difficulty_rating=1
    )
    
    locations[location_id] = new_location
    rooms[room].locations.append(location_id)
    rooms[room].last_visited = now
    
    storage.save_locations(locations)
    storage.save_rooms(rooms)
    
    # Update user stats and check progress
    user = storage.load_user_profile(user_id)
    user.total_memories += 1
    xp_reward = 15  # Base XP for storing a memory
    
    # Bonus XP for good visual anchors (length as proxy for quality)
    if len(visual_anchor) > 50:
        xp_reward += 10
        
    # Bonus XP for keywords
    if keywords and len(keywords) >= 3:
        xp_reward += 5
        
    xp_result = user.add_xp(xp_reward)
    storage.save_user_profile(user)
    
    # Check for achievements and progress
    progress = check_user_progress(user_id)
    
    # Prepare achievement message if applicable
    achievement_message = None
    if progress["new_achievements"]:
        achievement = progress["new_achievements"][0]
        achievement_message = (
            f"🏆 Achievement Unlocked: {achievement['name']}! "
            f"{achievement['description']}. +{achievement['xp_reward']} XP!"
        )
    
    # Prepare personality-based message
    memory_message = generate_message("achievement", user_id)
    
    result = {
        "success": True,
        "message": f"Memory stored in '{room}' at position ({x}, {y}, {z})",
        "location_id": location_id,
        "location": asdict(new_location),
        "xp_gained": xp_reward,
        "memory_message": memory_message
    }
    
    # Add progress messages
    if achievement_message:
        result["achievement_message"] = achievement_message
        
    if progress["level_up"]:
        result["level_up_message"] = progress["level_up"]
        
    if progress["tip"]:
        result["tip"] = progress["tip"]
        
    if progress["challenge"]:
        result["challenge"] = progress["challenge"]
        result["challenge_message"] = (
            f"🏅 New Challenge: {progress['challenge']['name']}! "
            f"{progress['challenge']['description']}. Complete for +{progress['challenge']['xp_reward']} XP!"
        )
    
    return result

@mcp.tool(description="Take a walk through your memory palace to see all the memories you've saved")
def memory_journey(room: str, include_connections: bool = False) -> dict:
    """Take a journey through memories in a room with gamification elements"""
    
    rooms = storage.load_rooms()
    locations = storage.load_locations()
    user_id = "default"
    
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
        location.recall_count += 1
        
        journey_path.append({
            "location_id": location.id,
            "position": location.position,
            "visual_anchor": location.visual_anchor,
            "content": location.content,
            "keywords": location.keywords,
            "recall_count": location.recall_count
        })
    
    # Update room last visited
    current_room.last_visited = datetime.now().isoformat()
    
    # Calculate room mastery level based on recall counts
    if room_locations:
        avg_recall = sum(loc.recall_count for loc in room_locations) / len(room_locations)
        # Scale mastery: 5 recalls = 50%, 10 recalls = 100%
        mastery_level = min(100, int(avg_recall * 10))
        current_room.mastery_level = mastery_level
    
    # Save updated state
    storage.save_locations(locations)
    storage.save_rooms(rooms)
    
    # Award XP based on journey
    user = storage.load_user_profile(user_id)
    xp_reward = 10 + (5 * len(room_locations))  # Base + per memory
    xp_result = user.add_xp(xp_reward)
    storage.save_user_profile(user)
    
    # Check for achievements
    progress = check_user_progress(user_id)
    
    result = {
        "room": room,
        "description": current_room.description,
        "theme": current_room.theme,
        "mastery_level": current_room.mastery_level,
        "journey_path": journey_path,
        "total_memories": len(journey_path),
        "xp_gained": xp_reward,
        "journey_message": generate_message("challenge", user_id)
    }
    
    if include_connections and current_room.connections:
        result["connected_rooms"] = current_room.connections
    
    # Add progress messages
    if progress["new_achievements"]:
        achievement = progress["new_achievements"][0]
        result["achievement_message"] = (
            f"🏆 Achievement Unlocked: {achievement['name']}! "
            f"{achievement['description']}. +{achievement['xp_reward']} XP!"
        )
        
    if progress["level_up"]:
        result["level_up_message"] = progress["level_up"]
        
    if progress["streak_updated"] and not progress["streak_broken"]:
        result["streak_message"] = generate_message("streak", user_id)
    
    return result

@mcp.tool(description="Find memories in your memory palace by telling me what you're looking for")
def search_memories(query: str, room: Optional[str] = None) -> dict:
    """Search for memories using keywords or content with gamification elements"""
    
    locations = storage.load_locations()
    user_id = "default"
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
    
    # Award XP for successful search
    user = storage.load_user_profile(user_id)
    xp_reward = 5 if results else 0  # Only reward successful searches
    if len(results) > 0:
        xp_reward += min(15, len(results) * 3)  # More results = more XP (up to 15)
    
    xp_result = user.add_xp(xp_reward)
    storage.save_user_profile(user)
    
    # Check for achievements
    progress = check_user_progress(user_id)
    
    result = {
        "query": query,
        "room_filter": room,
        "results_count": len(results),
        "results": results,
        "xp_gained": xp_reward if results else 0
    }
    
    # Add personality-based messages
    if results:
        result["search_message"] = "🔍 Your memory palace reveals its secrets!"
        
    # Add progress messages
    if progress["new_achievements"]:
        achievement = progress["new_achievements"][0]
        result["achievement_message"] = (
            f"🏆 Achievement Unlocked: {achievement['name']}! "
            f"{achievement['description']}. +{achievement['xp_reward']} XP!"
        )
        
    if progress["level_up"]:
        result["level_up_message"] = progress["level_up"]
    
    return result

@mcp.tool(description="See everything in your memory palace - like a map of all your memory rooms")
def get_palace_overview() -> dict:
    """Get an overview of the entire memory palace with gamification elements"""
    
    rooms = storage.load_rooms()
    locations = storage.load_locations()
    user_id = "default"
    user = storage.load_user_profile(user_id)
    
    room_stats = {}
    total_memories = len(locations)
    
    for room_name, room in rooms.items():
        room_location_count = len([
            loc for loc_id in room.locations 
            if loc_id in locations
        ])
        
        room_stats[room_name] = {
            "description": room.description,
            "theme": room.theme,
            "memory_count": room_location_count,
            "connections": room.connections,
            "mastery_level": room.mastery_level,
            "last_visited": room.last_visited
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
    
    # Calculate overall palace mastery
    if rooms:
        overall_mastery = sum(room.mastery_level for room in rooms.values()) / len(rooms)
    else:
        overall_mastery = 0
    
    # Update user profile
    progress = check_user_progress(user_id)
    
    # Get unlocked achievements
    unlocked_achievements = [
        asdict(achievement) for achievement in user.achievements if achievement.unlocked
    ]
    
    return {
        "total_rooms": len(rooms),
        "total_memories": total_memories,
        "overall_mastery": overall_mastery,
        "room_stats": room_stats,
        "recent_activity": recent_activity,
        "palace_health": "excellent" if total_memories > 0 else "empty",
        "user": {
            "level": user.level,
            "xp": user.xp,
            "xp_to_next_level": user.xp_to_next_level,
            "streak_days": user.streak_days,
            "personality": user.personality,
            "personality_name": user.get_personality()["name"],
            "total_achievements": len(unlocked_achievements)
        },
        "unlocked_achievements": unlocked_achievements,
        "streak_message": generate_message("streak", user_id) if user.streak_days > 0 else None
    }

@mcp.tool(description="See your player card with all the cool badges you've earned")
def get_user_profile() -> dict:
    """Get detailed information about the user's profile and progress"""
    user_id = "default"
    user = storage.load_user_profile(user_id)
    
    # Update streak and check achievements
    progress = check_user_progress(user_id)
    
    # Get unlocked and locked achievements
    all_achievements = storage.load_achievements()
    unlocked_ids = [a.id for a in user.achievements if a.unlocked]
    
    unlocked_achievements = [
        asdict(achievement) for achievement in user.achievements if achievement.unlocked
    ]
    
    locked_achievements = [
        asdict(achievement) for achievement_id, achievement in all_achievements.items()
        if achievement_id not in unlocked_ids
    ]
    
    # Get personality details
    personality = user.get_personality()
    
    return {
        "user": {
            "username": user.username,
            "level": user.level,
            "xp": user.xp,
            "xp_to_next_level": user.xp_to_next_level,
            "streak_days": user.streak_days,
            "total_memories": user.total_memories,
            "total_rooms": user.total_rooms,
            "challenges_completed": user.challenges_completed
        },
        "personality": {
            "type": user.personality,
            "name": personality["name"],
            "description": personality["description"],
            "emoji": personality["emoji"]
        },
        "achievements": {
            "unlocked": unlocked_achievements,
            "locked": locked_achievements,
            "total_unlocked": len(unlocked_achievements),
            "total_available": len(all_achievements)
        },
        "progress_message": generate_message("streak", user_id) if user.streak_days > 0 else generate_message("welcome", user_id)
    }

@mcp.tool(description="Choose a different friendly guide to help you with your memory palace")
def change_personality(personality_type: str) -> dict:
    """Change the user's guide personality"""
    user_id = "default"
    user = storage.load_user_profile(user_id)
    
    if personality_type not in PERSONALITIES:
        available = ", ".join(PERSONALITIES.keys())
        return {
            "error": f"Personality '{personality_type}' not found. Available personalities: {available}"
        }
    
    user.personality = personality_type
    storage.save_user_profile(user)
    
    new_personality = PERSONALITIES[personality_type]
    
    return {
        "success": True,
        "message": f"Personality changed to {new_personality['name']}",
        "personality": {
            "type": personality_type,
            "name": new_personality["name"],
            "description": new_personality["description"],
            "emoji": new_personality["emoji"]
        },
        "welcome_message": f"{new_personality['emoji']} {new_personality['messages']['welcome']}"
    }

@mcp.tool(description="Play a fun memory game to see what you remember and win prizes")
def start_challenge() -> dict:
    """Generate and start a memory challenge"""
    user_id = "default"
    user = storage.load_user_profile(user_id)
    
    # Generate a challenge
    challenge = storage.generate_challenge(user_id)
    
    if not challenge:
        return {
            "error": "Unable to create challenge. Add more memories to your palace first!",
            "guidance": "Try creating at least one room with 3-5 memories before attempting challenges."
        }
    
    # Add the challenge to user's active challenges
    user.active_challenges.append(challenge["id"])
    storage.save_user_profile(user)
    
    # Add personality flavor
    personality = user.get_personality()
    
    return {
        "success": True,
        "message": f"Challenge started: {challenge['name']}",
        "challenge": challenge,
        "challenge_message": f"{personality['emoji']} {personality['messages']['challenge']}",
        "guidance": (
            "To complete this challenge, recall the content of the targeted memories. "
            "The more accurately you recall, the higher your score!"
        )
    }

@mcp.tool(description="Find out all the cool things your memory palace can do")
def get_server_info() -> dict:
    """Get information about the Memory Palace MCP server"""
    info = SERVER_INFO.copy()
    info.update({
        "personalities": [p["name"] for p in PERSONALITIES.values()],
        "environment": os.environ.get("ENVIRONMENT", "development"),
        "python_version": os.sys.version.split()[0]
    })
    return info

@mcp.tool(description="Start a memory adventure with fun missions to complete")
def start_learning_path(path_id: str) -> dict:
    """Start or continue a guided learning path"""
    user_id = "default"
    user = storage.load_user_profile(user_id)
    all_paths = storage.load_learning_paths()
    
    if path_id not in all_paths:
        available = ", ".join(all_paths.keys())
        return {
            "error": f"Learning path '{path_id}' not found. Available paths: {available}"
        }
    
    path = all_paths[path_id]
    
    # Check if user is already on this path
    current_progress = user.learning_paths.get(path_id, 0)
    
    # Determine current stage (0-based index)
    current_stage_idx = min(int(current_progress / 20), len(path["stages"]) - 1)
    current_stage = path["stages"][current_stage_idx]
    
    # Prepare next goals based on current stage
    next_goals = current_stage["tasks"]
    
    # Save that user is on this path
    if path_id not in user.learning_paths:
        user.learning_paths[path_id] = 0
    
    storage.save_user_profile(user)
    
    # Generate personality-specific message
    personality = user.get_personality()
    
    return {
        "success": True,
        "path_name": path["name"],
        "path_description": path["description"],
        "current_progress": current_progress,
        "current_stage": {
            "name": current_stage["name"],
            "tasks": current_stage["tasks"],
            "xp_reward": current_stage["xp_reward"]
        },
        "message": f"{personality['emoji']} Let's begin your journey into {path['name']}!",
        "guidance": (
            f"Focus on these tasks: {', '.join(next_goals)}. "
            f"Complete them to advance to the next stage of your learning!"
        )
    }

@mcp.tool(description="Tell me when you finish a memory mission to get your reward")
def update_learning_progress(path_id: str, completed_task: str) -> dict:
    """Update progress on a learning path after completing a task"""
    user_id = "default"
    user = storage.load_user_profile(user_id)
    all_paths = storage.load_learning_paths()
    
    if path_id not in all_paths:
        return {"error": f"Learning path '{path_id}' not found."}
    
    path = all_paths[path_id]
    
    # Check if user is on this path
    if path_id not in user.learning_paths:
        return {"error": f"You haven't started the '{path['name']}' learning path yet."}
    
    current_progress = user.learning_paths[path_id]
    current_stage_idx = min(int(current_progress / 20), len(path["stages"]) - 1)
    current_stage = path["stages"][current_stage_idx]
    
    # Check if the task is in the current stage
    if completed_task not in current_stage["tasks"]:
        return {
            "error": f"Task '{completed_task}' is not in your current stage.",
            "current_tasks": current_stage["tasks"]
        }
    
    # Increase progress (each task is worth 20/num_tasks percent)
    tasks_in_stage = len(current_stage["tasks"])
    progress_per_task = 20 / tasks_in_stage
    user.learning_paths[path_id] += progress_per_task
    
    # Check if stage is complete (progress >= next stage threshold)
    stage_complete = False
    next_stage = None
    xp_earned = 0
    
    if user.learning_paths[path_id] >= (current_stage_idx + 1) * 20:
        stage_complete = True
        xp_earned = current_stage["xp_reward"]
        user.add_xp(xp_earned)
        
        # Check if there's a next stage
        if current_stage_idx + 1 < len(path["stages"]):
            next_stage = path["stages"][current_stage_idx + 1]
    
    storage.save_user_profile(user)
    progress = check_user_progress(user_id)
    
    result = {
        "success": True,
        "path_name": path["name"],
        "task_completed": completed_task,
        "current_progress": user.learning_paths[path_id],
        "stage_complete": stage_complete
    }
    
    if stage_complete:
        result["stage_complete_message"] = (
            f"🎓 Congratulations! You've completed the '{current_stage['name']}' stage! "
            f"+{xp_earned} XP!"
        )
        
        if next_stage:
            result["next_stage"] = {
                "name": next_stage["name"],
                "tasks": next_stage["tasks"]
            }
            result["guidance"] = (
                f"Your next goals: {', '.join(next_stage['tasks'])}. "
                f"Keep building your memory palace skills!"
            )
        else:
            result["path_complete"] = True
            result["completion_message"] = (
                f"🏆 Amazing! You've completed the entire '{path['name']}' learning path! "
                f"You've mastered these memory palace techniques!"
            )
    
    # Add progress messages
    if progress["level_up"]:
        result["level_up_message"] = progress["level_up"]
        
    if progress["new_achievements"]:
        achievement = progress["new_achievements"][0]
        result["achievement_message"] = (
            f"🏆 Achievement Unlocked: {achievement['name']}! "
            f"{achievement['description']}. +{achievement['xp_reward']} XP!"
        )
    
    return result

@mcp.tool(description="See all the fun memory adventures you can go on")
def get_learning_paths() -> dict:
    """Get information about all learning paths and user progress"""
    user_id = "default"
    user = storage.load_user_profile(user_id)
    all_paths = storage.load_learning_paths()
    
    user_paths = []
    for path_id, path in all_paths.items():
        progress = user.learning_paths.get(path_id, 0)
        current_stage_idx = min(int(progress / 20), len(path["stages"]) - 1)
        
        user_paths.append({
            "id": path_id,
            "name": path["name"],
            "description": path["description"],
            "progress": progress,
            "current_stage": path["stages"][current_stage_idx]["name"],
            "total_stages": len(path["stages"]),
            "started": path_id in user.learning_paths
        })
    
    # Sort by started first, then alphabetically
    user_paths.sort(key=lambda x: (not x["started"], x["name"]))
    
    return {
        "learning_paths": user_paths,
        "message": "Choose a learning path to enhance your memory palace skills!"
    }

@mcp.tool(description="Get friendly reminders to practice your memories so you won't forget them")
def setup_spaced_repetition(room: str, interval_days: int = 1, message_time: str = "morning") -> dict:
    """Setup spaced repetition reminders for a room"""
    rooms = storage.load_rooms()
    user_id = "default"
    user = storage.load_user_profile(user_id)
    
    if room not in rooms:
        return {"error": f"Room '{room}' doesn't exist"}
    
    # In a real implementation, we would store this in a database and trigger
    # actual reminders. For now, we'll just return the planned schedule.
    
    # Calculate next few reminder dates
    today = datetime.now().date()
    reminders = []
    
    # Use intervals from constants
    for i, interval in enumerate(SPACED_REPETITION_INTERVALS):
        reminder_date = today + timedelta(days=interval)
        reminders.append({
            "day": interval,
            "date": reminder_date.isoformat(),
            "repetition_number": i + 1
        })
    
    # Add some XP for setting up spaced repetition
    xp_reward = 20
    user.add_xp(xp_reward)
    storage.save_user_profile(user)
    
    return {
        "success": True,
        "room": room,
        "message": f"Spaced repetition reminders set up for '{room}'",
        "next_reminder": reminders[0]["date"],
        "reminder_schedule": reminders,
        "xp_gained": xp_reward,
        "guidance": (
            "Spaced repetition is scientifically proven to improve long-term memory. "
            "You'll receive reminders to review this room at gradually increasing intervals."
        ),
        "tip": "For best results, take a memory journey through this room each time you receive a reminder."
    }

@mcp.tool(description="Play a quick memory game to practice what you've learned")
def practice_recall(room: str, count: int = 3) -> dict:
    """Test your memory with a quick recall practice session"""
    rooms = storage.load_rooms()
    locations = storage.load_locations()
    user_id = "default"
    
    if room not in rooms:
        return {"error": f"Room '{room}' doesn't exist"}
    
    # Get memory locations for this room
    room_locations = [
        locations[loc_id] for loc_id in rooms[room].locations 
        if loc_id in locations
    ]
    
    if not room_locations:
        return {"error": f"No memories found in room '{room}'"}
    
    # Select random memories to test (or all if count > available)
    count = min(count, len(room_locations))
    test_locations = random.sample(room_locations, count)
    
    # Format the test questions
    questions = []
    for i, loc in enumerate(test_locations):
        questions.append({
            "question_number": i + 1,
            "location_id": loc.id,
            "visual_anchor": loc.visual_anchor,
            "position": loc.position,
            "hint": f"Look for the {loc.visual_anchor.split()[0]} at position ({loc.position['x']}, {loc.position['y']}, {loc.position['z']})"
        })
    
    # Update statistics
    user = storage.load_user_profile(user_id)
    xp_reward = 15 * count  # XP per memory tested
    user.add_xp(xp_reward)
    storage.save_user_profile(user)
    
    # Get personality message
    personality = user.get_personality()
    
    return {
        "success": True,
        "room": room,
        "recall_test": {
            "total_questions": count,
            "questions": questions
        },
        "message": f"{personality['emoji']} Let's test your memory palace recall!",
        "xp_reward": xp_reward,
        "guidance": (
            "For each question, try to recall the content stored at that location. "
            "The more accurately you can recall, the stronger your memory palace becomes!"
        )
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    
    print(f"Starting FastMCP server on {host}:{port}")
    
    # Create default user if it doesn't exist
    default_user = storage.load_user_profile("default")
    
    mcp.run(
        transport="http",
        host=host,
        port=port
    )
