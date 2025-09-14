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
        "description": "A friendly wise guide who shares helpful advice",
        "messages": {
            "welcome": "Hi there! Welcome to your Memory Palace. I'm here to help you remember things better!",
            "achievement": "Great job! Each time you add a memory, you're getting better at remembering things.",
            "challenge": "Would you like to play a quick memory game to see what you remember?",
            "tip": "Try to picture really colorful and funny images - they're easier to remember!",
            "streak": "Wow! You've practiced {streak} days in a row! Your memory is getting so strong!"
        },
        "emoji": "🧙‍♂️"
    },
    "explorer": {
        "name": "Explorer",
        "description": "An adventurous guide who makes learning feel like a fun journey",
        "messages": {
            "welcome": "Hey there, explorer! Ready for an adventure in your Memory Palace?",
            "achievement": "Amazing discovery! You've added a new memory to your collection!",
            "challenge": "Want to go on a treasure hunt through your memories? Let's see what we can find!",
            "tip": "The sillier and more colorful the picture in your mind, the easier it is to find later!",
            "streak": "Woohoo! {streak} days of adventure! Your memory map gets bigger every day!"
        },
        "emoji": "🧭"
    },
    "architect": {
        "name": "Architect",
        "description": "A friendly builder who helps you organize your memories",
        "messages": {
            "welcome": "Hello! I'm your memory builder. Let's create an amazing place for your memories!",
            "achievement": "You did it! Your memory building is looking better and better!",
            "challenge": "Should we check how sturdy your memory building is with a quick game?",
            "tip": "Try to put similar memories near each other - it makes them easier to find later!",
            "streak": "{streak} days of building memories! You're becoming a master memory builder!"
        },
        "emoji": "👷‍♀️"
    },
    "coach": {
        "name": "Coach",
        "description": "A friendly and encouraging memory coach who cheers you on",
        "messages": {
            "welcome": "Hi team! Ready to exercise that amazing brain of yours?",
            "achievement": "Way to go! Your memory is getting stronger every time we practice!",
            "challenge": "Ready for a quick memory workout? It'll be fun!",
            "tip": "Just like sports practice, the more you review your memories, the better you'll get!",
            "streak": "Amazing! {streak} days of practice in a row! You're becoming a memory superstar!"
        },
        "emoji": "🏋️‍♀️"
    },
    "friend": {
        "name": "Friend",
        "description": "A kind and supportive friend who helps you remember things",
        "messages": {
            "welcome": "Hey buddy! So glad you're here! Want to work on remembering things together?",
            "achievement": "You did it! I knew you could! Your memory palace is looking awesome!",
            "challenge": "Want to play a fun memory game with me?",
            "tip": "The funniest and weirdest pictures are the ones we remember best!",
            "streak": "We've been practicing for {streak} days together! You're doing amazing!"
        },
        "emoji": "🤗"
    },
    "wizard": {
        "name": "Wizard",
        "description": "A friendly memory wizard who makes learning magical and fun",
        "messages": {
            "welcome": "Abracadabra! Welcome to your magical Memory Palace! I'm your wizard helper!",
            "achievement": "Magic happening! You've created a new memory spell!",
            "challenge": "Shall we test your magical memory powers with a fun challenge?",
            "tip": "The most magical and sparkly images are the easiest to remember!",
            "streak": "Magical! You've practiced your memory spells for {streak} days in a row!"
        },
        "emoji": "✨"
    }
}

# Default achievement definitions
DEFAULT_ACHIEVEMENTS = {
    "first_room": {
        "id": "first_room",
        "name": "Room Builder",
        "description": "You made your first memory room!",
        "icon": "🏗️",
        "xp_reward": 50
    },
    "first_memory": {
        "id": "first_memory",
        "name": "Memory Maker",
        "description": "You saved your first memory!",
        "icon": "🌱",
        "xp_reward": 50
    },
    "three_rooms": {
        "id": "three_rooms",
        "name": "Super Builder",
        "description": "You made three memory rooms!",
        "icon": "🏛️",
        "xp_reward": 100
    },
    "ten_memories": {
        "id": "ten_memories",
        "name": "Memory Collector",
        "description": "You saved ten memories!",
        "icon": "💎",
        "xp_reward": 150
    },
    "memory_journey": {
        "id": "memory_journey",
        "name": "Memory Explorer",
        "description": "You took your first memory walk!",
        "icon": "🧭",
        "xp_reward": 75
    },
    "perfect_recall": {
        "id": "perfect_recall",
        "name": "Memory Champion",
        "description": "You remembered 5 memories perfectly!",
        "icon": "🧠",
        "xp_reward": 200
    },
    "three_day_streak": {
        "id": "three_day_streak",
        "name": "Regular Visitor",
        "description": "You practiced 3 days in a row!",
        "icon": "🔥",
        "xp_reward": 100
    },
    "seven_day_streak": {
        "id": "seven_day_streak",
        "name": "Memory Star",
        "description": "You practiced 7 days in a row!",
        "icon": "🏆",
        "xp_reward": 250
    },
    "first_search": {
        "id": "first_search",
        "name": "Memory Detective",
        "description": "You found a memory by searching!",
        "icon": "🔍",
        "xp_reward": 50
    },
    "connected_rooms": {
        "id": "connected_rooms",
        "name": "Room Connector",
        "description": "You connected three rooms together!",
        "icon": "🔗",
        "xp_reward": 150
    },
}

# Default challenge templates
DEFAULT_CHALLENGES = {
    "quick_recall": {
        "name": "Memory Sprint",
        "description": "Can you remember {count} things from your {room} room? Let's play!",
        "difficulty_levels": {
            "easy": {"count": 3, "xp_reward": 50},
            "medium": {"count": 5, "xp_reward": 100},
            "hard": {"count": 10, "xp_reward": 200}
        }
    },
    "room_mastery": {
        "name": "Room Champion",
        "description": "Try to remember everything in your {room} room!",
        "xp_reward": 150
    },
    "visual_anchors": {
        "name": "Picture Match",
        "description": "Match {count} pictures to the right memories - like a matching game!",
        "difficulty_levels": {
            "easy": {"count": 3, "xp_reward": 75},
            "medium": {"count": 7, "xp_reward": 125},
            "hard": {"count": 12, "xp_reward": 225}
        }
    },
    "position_recall": {
        "name": "Memory Map",
        "description": "Do you remember where you put {count} of your memories?",
        "difficulty_levels": {
            "easy": {"count": 3, "xp_reward": 100},
            "medium": {"count": 5, "xp_reward": 150},
            "hard": {"count": 8, "xp_reward": 250}
        }
    },
    "palace_tour": {
        "name": "Grand Tour",
        "description": "Let's visit every room in your memory palace in one big adventure!",
        "xp_reward": 300
    }
}

# Default learning paths
DEFAULT_LEARNING_PATHS = {
    "memory_palace_basics": {
        "name": "Memory Palace Adventure",
        "description": "Learn how to make and use your own memory palace",
        "stages": [
            {
                "name": "First Steps",
                "tasks": ["Make your first room", "Save your first memory"],
                "xp_reward": 50
            },
            {
                "name": "Memory Pictures",
                "tasks": ["Save 3 memories with fun pictures to help you remember"],
                "xp_reward": 75
            },
            {
                "name": "Memory Walk",
                "tasks": ["Take a walk through your memories", "Connect two rooms together"],
                "xp_reward": 100
            },
            {
                "name": "Growing Your Palace",
                "tasks": ["Make a total of 3 rooms", "Save 10 memories"],
                "xp_reward": 150
            },
            {
                "name": "Palace Champion",
                "tasks": ["Visit all your rooms in one trip", "Play a memory game and win"],
                "xp_reward": 200
            }
        ]
    },
    "vocabulary_mastery": {
        "name": "Word Adventure",
        "description": "Use your memory palace to learn new words for any subject",
        "stages": [
            {
                "name": "Word Collection",
                "tasks": ["Make a room for your words", "Save 5 words you want to learn"],
                "xp_reward": 75
            },
            {
                "name": "Word Pictures",
                "tasks": ["Make funny pictures for each word to help you remember them"],
                "xp_reward": 100
            },
            {
                "name": "Word Practice",
                "tasks": ["Try to remember all your words", "Add 5 more new words"],
                "xp_reward": 125
            },
            {
                "name": "Word Connections",
                "tasks": ["Connect words that go together", "Add examples of how to use the words"],
                "xp_reward": 150
            },
            {
                "name": "Word Master",
                "tasks": ["Remember all your words perfectly", "Win the word challenge game"],
                "xp_reward": 200
            }
        ]
    },
    "study_system": {
        "name": "Super Study Adventure",
        "description": "Create an awesome study system using your memory palace",
        "stages": [
            {
                "name": "Subject Rooms",
                "tasks": ["Make different rooms for different subjects", "Connect them in a way that makes sense"],
                "xp_reward": 100
            },
            {
                "name": "Important Ideas",
                "tasks": ["Save the most important ideas in each subject room"],
                "xp_reward": 125
            },
            {
                "name": "Idea Connections",
                "tasks": ["Connect ideas that go together even if they're in different rooms"],
                "xp_reward": 150
            },
            {
                "name": "Daily Practice",
                "tasks": ["Practice visiting your memory rooms every day"],
                "xp_reward": 175
            },
            {
                "name": "Study Champion",
                "tasks": ["Show you can remember everything in all your subjects"],
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

# ===========================================
# Defaults for Natural-Language Routing & UX
# ===========================================

# Default room and content helpers
DEFAULT_ROOM_NAME = "Study Hall"
DEFAULT_ROOM_DESCRIPTION = "A cozy place for your memories"
DEFAULT_VISUAL_ANCHOR = "A big colorful note on the wall"

# Personality types list (for easy validation)
PERSONALITY_TYPES = list(PERSONALITIES.keys())

# Friendly example suggestions when input is unclear
DEFAULT_IDEA_SUGGESTIONS = [
    "Make a room called 'Study Hall'",
    "Save a memory in 'Study Hall': The sun is a star",
    "Walk through 'Study Hall'",
    "Find photosynthesis in 'Study Hall'",
    "Quiz me in 'Study Hall' with 3 questions",
    "Remind me to practice 'Study Hall'",
    "Be my wizard"
]