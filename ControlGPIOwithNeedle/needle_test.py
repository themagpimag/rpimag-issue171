import needle
from pathlib import Path
import subprocess
notes_path = Path("needle-notes.txt")

@needle.tool
def save_note(text: str):
    """Append a note to a local text file."""
    with notes_path.open("a", encoding="utf-8") as notes:
        notes.write(text + "\n")
    return {"text": text, "path": str(notes_path)}

@needle.tool
def get_temperature():
    """Return the current CPU temperature of this Raspberry Pi in Celsius."""
    out = subprocess.check_output(["vcgencmd", "measure_temp"], text=True)
    return {"temperature_c": float(out.split("=")[1].split("'")[0])}

agent = needle.Needle(tools=[save_note, get_temperature])
response = agent.run("Save a note that says the cooler is working.")