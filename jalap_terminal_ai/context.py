import platform
import os
import subprocess


def get_os() -> str:
    """
    Detect the operating system.
    Returns: 'macos', 'linux', 'windows', or 'unknown'
    """
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    elif system == "linux":
        return "linux"
    elif system == "windows":
        return "windows"
    return "unknown"


def get_shell() -> str:
    """
    Detect the user's current shell.
    Returns: 'zsh', 'bash', 'powershell', or 'unknown'
    """
    # Try SHELL environment variable (Unix/macOS/Linux)
    shell = os.environ.get("SHELL", "")
    if shell:
        shell_name = os.path.basename(shell)
        if shell_name in ["zsh", "bash", "sh", "ksh"]:
            return shell_name
    
    # Windows: check for PowerShell or cmd
    if get_os() == "windows":
        comspec = os.environ.get("COMSPEC", "")
        if "powershell" in comspec.lower():
            return "powershell"
        return "cmd"
    
    return "unknown"


def get_cwd() -> str:
    """Get current working directory."""
    return os.getcwd()


def get_username() -> str:
    """Get current username."""
    return os.environ.get("USER", os.environ.get("USERNAME", "unknown"))


def get_context() -> dict:
    """
    Get full system context as a dictionary.
    """
    return {
        "os": get_os(),
        "shell": get_shell(),
        "cwd": get_cwd(),
        "username": get_username(),
    }


def format_context() -> str:
    """Format context information for display to user."""
    ctx = get_context()
    return f"""Current Context:
- OS: {ctx['os']}
- Shell: {ctx['shell']}
- Working Directory: {ctx['cwd']}
- User: {ctx['username']}"""
