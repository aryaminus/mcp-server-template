#!/usr/bin/env python3
"""
Constants for the Memory Palace MCP Server
"""

# ===========================================
# Personalities and Engagement System
# ===========================================

PERSONALITIES = {
    "sage": {
        "name": "Sage",
        "description": "A wise and patient guide who speaks with ancient wisdom",
        "messages": {
            "welcome": "Welcome, seeker of knowledge. Your Memory Palace awaits your wisdom.",
            "achievement": "Your mind grows stronger with each memory, young scholar.",
            "challenge": "A true sage tests their memory regularly. Are you ready for a challenge?",
            "tip": "Remember, the most vivid visual anchors create the strongest memories.",
            "streak": "Your dedication to memory practice is most impressive. {streak} days of wisdom!"
        },
        "emoji": "🧙‍♂️"
    },
    "explorer": {
        "name": "Explorer",
        "description": "An adventurous guide who treats your memory palace as a world to discover",
        "messages": {
            "welcome": "Adventure awaits in your Memory Palace! Let's explore new territories of knowledge!",
            "achievement": "Fantastic discovery! You've unlocked new regions of your mental map!",
            "challenge": "Ready for an expedition to test your memory terrain? Let's go!",
            "tip": "The best explorers mark their discoveries with vivid flags. Make your visual anchors stand out!",
            "streak": "What an expedition! {streak} days of continuous exploration! Your map grows richer!"
        },
        "emoji": "🧭"
    },
    "architect": {
        "name": "Architect",
        "description": "A precise designer who helps you construct your palace with elegant structure",
        "messages": {
            "welcome": "Welcome to your mental blueprint. Let's design something magnificent together.",
            "achievement": "Excellent construction! Your mental architecture is taking beautiful form.",
            "challenge": "A good architect tests their structures. Shall we inspect your memory foundations?",
            "tip": "The strongest memories have precise coordinates. Be exact in your spatial positioning.",
            "streak": "{streak} days of consistent building! Your memory palace grows more magnificent daily."
        },
        "emoji": "👷‍♀️"
    },
    "coach": {
        "name": "Coach",
        "description": "An energetic memory trainer who pushes you to strengthen your recall",
        "messages": {
            "welcome": "Let's train that memory muscle! Your Palace awaits your workout!",
            "achievement": "INCREDIBLE WORK! Your memory is getting STRONGER every day!",
            "challenge": "No pain, no gain! Ready for a memory challenge to flex those brain muscles?",
            "tip": "Mental repetition is like memory protein! Review those spaces daily!",
            "streak": "AMAZING CONSISTENCY! {streak} day streak! You're becoming a memory CHAMPION!"
        },
        "emoji": "🏋️‍♀️"
    }
}

# Default achievement definitions
DEFAULT_ACHIEVEMENTS = {
    "first_room": {
        "id": "first_room",
        "name": "Architect's Apprentice",
        "description": "Create your first room in your Memory Palace",
        "icon": "🏗️",
        "xp_reward": 50
    },
    "first_memory": {
        "id": "first_memory",
        "name": "Memory Seedling",
        "description": "Plant your first memory in your palace",
        "icon": "🌱",
        "xp_reward": 50
    },
    "three_rooms": {
        "id": "three_rooms",
        "name": "Master Builder",
        "description": "Create three different rooms in your Memory Palace",
        "icon": "🏛️",
        "xp_reward": 100
    },
    "ten_memories": {
        "id": "ten_memories",
        "name": "Memory Collector",
        "description": "Store ten memories in your palace",
        "icon": "💎",
        "xp_reward": 150
    },
    "memory_journey": {
        "id": "memory_journey",
        "name": "Palace Explorer",
        "description": "Take your first memory journey",
        "icon": "🧭",
        "xp_reward": 75
    },
    "perfect_recall": {
        "id": "perfect_recall",
        "name": "Perfect Recall",
        "description": "Successfully recall 5 memories in a row",
        "icon": "🧠",
        "xp_reward": 200
    },
    "three_day_streak": {
        "id": "three_day_streak",
        "name": "Consistent Scholar",
        "description": "Use your Memory Palace for 3 days in a row",
        "icon": "🔥",
        "xp_reward": 100
    },
    "seven_day_streak": {
        "id": "seven_day_streak",
        "name": "Memory Master",
        "description": "Maintain a 7-day practice streak",
        "icon": "🏆",
        "xp_reward": 250
    },
    "first_search": {
        "id": "first_search",
        "name": "Memory Detective",
        "description": "Successfully search your Memory Palace",
        "icon": "🔍",
        "xp_reward": 50
    },
    "connected_rooms": {
        "id": "connected_rooms",
        "name": "Palace Architect",
        "description": "Connect three rooms together in your palace",
        "icon": "🔗",
        "xp_reward": 150
    },
}

# Default challenge templates
DEFAULT_CHALLENGES = {
    "quick_recall": {
        "name": "Quick Recall",
        "description": "Recall {count} memories from {room} within 60 seconds",
        "difficulty_levels": {
            "easy": {"count": 3, "xp_reward": 50},
            "medium": {"count": 5, "xp_reward": 100},
            "hard": {"count": 10, "xp_reward": 200}
        }
    },
    "room_mastery": {
        "name": "Room Mastery",
        "description": "Recall all memories in {room} with perfect accuracy",
        "xp_reward": 150
    },
    "visual_anchors": {
        "name": "Visual Anchor Challenge",
        "description": "Match {count} visual anchors to their correct memories",
        "difficulty_levels": {
            "easy": {"count": 3, "xp_reward": 75},
            "medium": {"count": 7, "xp_reward": 125},
            "hard": {"count": 12, "xp_reward": 225}
        }
    },
    "position_recall": {
        "name": "Spatial Positioning",
        "description": "Identify the correct 3D coordinates for {count} memories",
        "difficulty_levels": {
            "easy": {"count": 3, "xp_reward": 100},
            "medium": {"count": 5, "xp_reward": 150},
            "hard": {"count": 8, "xp_reward": 250}
        }
    },
    "palace_tour": {
        "name": "Complete Palace Tour",
        "description": "Visit every room in your Memory Palace in a single journey",
        "xp_reward": 300
    }
}

# Default learning paths
DEFAULT_LEARNING_PATHS = {
    "memory_palace_basics": {
        "name": "Memory Palace Foundations",
        "description": "Learn the fundamentals of creating and using a memory palace",
        "stages": [
            {
                "name": "Introduction to Memory Palaces",
                "tasks": ["Create your first room", "Store your first memory"],
                "xp_reward": 50
            },
            {
                "name": "Visual Anchors",
                "tasks": ["Create 3 memories with vivid visual anchors"],
                "xp_reward": 75
            },
            {
                "name": "Spatial Navigation",
                "tasks": ["Take your first memory journey", "Connect two rooms"],
                "xp_reward": 100
            },
            {
                "name": "Memory Expansion",
                "tasks": ["Create a total of 3 rooms", "Store 10 memories"],
                "xp_reward": 150
            },
            {
                "name": "Master Tour",
                "tasks": ["Complete a tour of your entire palace", "Pass a recall challenge"],
                "xp_reward": 200
            }
        ]
    },
    "vocabulary_mastery": {
        "name": "Vocabulary Mastery",
        "description": "Use your memory palace to master new vocabulary in any subject",
        "stages": [
            {
                "name": "Vocabulary Foundation",
                "tasks": ["Create a vocabulary-focused room", "Store 5 vocabulary terms"],
                "xp_reward": 75
            },
            {
                "name": "Visual Word Association",
                "tasks": ["Create memories with visual anchors for each word"],
                "xp_reward": 100
            },
            {
                "name": "Recall Training",
                "tasks": ["Successfully recall all vocabulary items", "Add 5 more terms"],
                "xp_reward": 125
            },
            {
                "name": "Context Building",
                "tasks": ["Create connections between related terms", "Add usage examples"],
                "xp_reward": 150
            },
            {
                "name": "Vocabulary Mastery",
                "tasks": ["Perfect recall of all vocabulary", "Complete vocabulary challenge"],
                "xp_reward": 200
            }
        ]
    },
    "study_system": {
        "name": "Study System Mastery",
        "description": "Create a comprehensive study system using your memory palace",
        "stages": [
            {
                "name": "Subject Organization",
                "tasks": ["Create rooms for different subjects", "Connect them logically"],
                "xp_reward": 100
            },
            {
                "name": "Key Concept Placement",
                "tasks": ["Store key concepts in each subject room"],
                "xp_reward": 125
            },
            {
                "name": "Relationship Mapping",
                "tasks": ["Create connections between related concepts across rooms"],
                "xp_reward": 150
            },
            {
                "name": "Recall Practice",
                "tasks": ["Practice daily recall journeys through your subjects"],
                "xp_reward": 175
            },
            {
                "name": "Study System Mastery",
                "tasks": ["Demonstrate perfect recall across all subjects"],
                "xp_reward": 250
            }
        ]
    }
}

# Spaced repetition intervals (in days) based on the Ebbinghaus forgetting curve
SPACED_REPETITION_INTERVALS = [1, 3, 7, 14, 30, 90, 180]

# Server information
SERVER_INFO = {
    "server_name": "Memory Palace MCP Server",
    "version": "2.0.0",
    "description": "A gamified spatial memory system using ancient memory palace techniques enhanced with AI",
    "capabilities": [
        "Create virtual rooms for organizing knowledge",
        "Store memories with spatial coordinates and visual anchors",
        "Take guided journeys through your knowledge",
        "Search memories across the entire palace",
        "Earn XP and unlock achievements as you build your palace",
        "Take memory challenges to test your recall",
        "Choose personality guides to customize your experience",
        "Track your daily streak and learning progress"
    ],
    "storage_type": "local_json"
}