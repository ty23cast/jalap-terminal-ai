import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict


class CommandHistory:
    """Manages command history storage and retrieval."""
    
    def __init__(self):
        # Store history in user's home directory
        self.history_file = Path.home() / ".jalap_history"
        self.max_history = 50
        self._ensure_history_file()
    
    def _ensure_history_file(self):
        """Create history file if it doesn't exist."""
        if not self.history_file.exists():
            self.history_file.write_text(json.dumps([]))
    
    def add(self, command: str, executed: bool = True, exit_code: int = None):
        """
        Add a command to history.
        
        Args:
            command: The command that was run
            executed: Whether the command was actually executed
            exit_code: The exit code from the command (if executed)
        """
        history = self._load_history()
        
        entry = {
            "command": command,
            "timestamp": datetime.now().isoformat(),
            "executed": executed,
            "exit_code": exit_code,
        }
        
        history.append(entry)
        
        # Keep only the last N commands
        if len(history) > self.max_history:
            history = history[-self.max_history:]
        
        self._save_history(history)
    
    def get_recent(self, count: int = 5) -> List[Dict]:
        """Get the most recent N commands."""
        history = self._load_history()
        return history[-count:]
    
    def get_all(self) -> List[Dict]:
        """Get all historical commands."""
        return self._load_history()
    
    def _load_history(self) -> List[Dict]:
        """Load history from file."""
        try:
            content = self.history_file.read_text()
            return json.loads(content) if content else []
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_history(self, history: List[Dict]):
        """Save history to file."""
        self.history_file.write_text(json.dumps(history, indent=2))
    
    def format_recent(self, count: int = 5) -> str:
        """Format recent commands for display."""
        recent = self.get_recent(count)
        if not recent:
            return "No command history found."
        
        output = f"Last {min(count, len(recent))} commands:\n"
        for i, entry in enumerate(recent, 1):
            timestamp = entry.get("timestamp", "unknown")
            command = entry.get("command", "unknown")
            exit_code = entry.get("exit_code", "N/A")
            executed = "Executed" if entry.get("executed") else "Failed to execute"
            output += f"{i}. [{executed}] {command} (exit: {exit_code})\n"
        
        return output
