from langchain_core.tools import tool



def note_tool(note: str):
    """
    saves a note to a local file

    Args:
        note: the text note to save
    """
    with open("notes.txt", "a") as f:
        f.write(note + "\n")