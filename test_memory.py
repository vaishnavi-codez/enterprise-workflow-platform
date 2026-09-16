from memory.short_term_memory import ShortTermMemory
from memory.long_term_memory import LongTermMemory


# Test short-term memory
short_memory = ShortTermMemory()

short_memory.add_message(
    "test-session",
    "user",
    "My name is Vaishnavi."
)

short_memory.add_message(
    "test-session",
    "assistant",
    "Nice to meet you, Vaishnavi!"
)

print("SHORT-TERM MEMORY:")
print(short_memory.get_history("test-session"))


# Test long-term memory
long_memory = LongTermMemory()

long_memory.save_memory(
    "test-session",
    "User prefers responses related to weather and calculations."
)

print("\nLONG-TERM MEMORY:")
print(long_memory.get_memories("test-session"))