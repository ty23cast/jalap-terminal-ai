import re
from typing import Tuple


class CommandSafetyChecker:
    """Checks if a command contains potentially dangerous patterns."""
    
    # Dangerous patterns to watch out for
    DANGEROUS_PATTERNS = [
        (r"rm\s+-rf\s+/", "Deleting root directory"),
        (r"rm\s+-rf\s+~", "Deleting home directory"),
        (r"rm\s+-rf\s+\.", "Deleting current directory recursively"),
        (r"sudo\s+rm\s+-rf", "Using sudo with recursive delete"),
        (r":\(\s*\)\s*\{.*\}", "Fork bomb attack pattern"),
        (r"curl\s+.*\|\s*(bash|sh|zsh)", "Piping curl output to shell"),
        (r"wget\s+.*\|\s*(bash|sh|zsh)", "Piping wget output to shell"),
        (r"\|\s*python", "Piping to Python interpreter"),
        (r"dd\s+if=", "Using dd command (risky data manipulation)"),
        (r"chmod\s+777", "Setting overly permissive file permissions"),
        (r"mkfs", "Creating filesystem (data loss)"),
    ]
    
    @classmethod
    def check(cls, command: str) -> Tuple[bool, str]:
        """
        Check if a command is potentially dangerous.
        
        Returns:
            Tuple of (is_dangerous, reason)
        """
        command_lower = command.lower()
        
        for pattern, reason in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, command_lower):
                return True, reason
        
        return False, ""
    
    @classmethod
    def format_warning(cls, command: str, reason: str) -> str:
        """Format a danger warning for display."""
        return f"""
   WARNING: Potentially Dangerous Command Detected
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reason: {reason}

Command: {command}

This command could cause data loss or system damage.
Are you sure you want to proceed? (y/N): """
