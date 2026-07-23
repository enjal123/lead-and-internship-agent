from memory.chroma_store import add_memory, search_memory


class MemoryManager:
    """
    Lets agents remember past businesses/internships they've researched
    so future runs can recall prior context (e.g. "have I already
    contacted this business?").
    """

    def store_business_memory(self, business_name, notes):
        add_memory(
            text=f"{business_name}: {notes}",
            metadata={"type": "business"},
        )

    def store_internship_memory(self, company, notes):
        add_memory(
            text=f"{company}: {notes}",
            metadata={"type": "internship"},
        )

    def search_related_memories(self, query):
        return search_memory(query)
