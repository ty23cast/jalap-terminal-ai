import subprocess
import sys
from typing import Optional, Tuple

from jalap_terminal_ai.context import get_context, format_context
from jalap_terminal_ai.history import CommandHistory
from jalap_terminal_ai.safety import CommandSafetyChecker
from jalap_terminal_ai.config import ConfigManager
from jalap_terminal_ai.ai_integration import AIIntegration, MockAI


class JalapTerminalAI:
    """Main class for the Jalap Terminal AI assistant."""
    
    def __init__(self):
        self.context = get_context()
        self.history = CommandHistory()
        self.config = ConfigManager()
        self.ai = None
        self._initialize_ai()
    
    def _initialize_ai(self):
        """Initialize AI integration with available API key or use mock."""
        api_key, provider = self.config.get_api_key()
        if api_key:
            try:
                self.ai = AIIntegration(api_key, provider)
                print(f"Using {provider.title()} AI provider")
            except Exception as e:
                print(f"Failed to initialize AI provider: {e}")
                self.ai = MockAI()
        else:
            # Use mock AI when no API key available
            self.ai = MockAI()
    
    def process_query(self, query: str) -> bool:
        """
        Process a user query and execute the suggested command if approved.
        
        Args:
            query: User's natural language request
        
        Returns:
            True if command was executed, False otherwise
        """
        # Show current context
        print(format_context())
        print()
        
        # Get command suggestion from AI
        print(f"Query: {query}")
        print("\nGenerating command suggestion...")
        command = self.ai.get_command_suggestion(query, self.context)
        
        if not command:
            print("Could not generate a command suggestion.")
            return False
        
        print(f"\nSuggested command: {command}")
        
        # Get explanation
        print("\nGenerating explanation...")
        explanation = self.ai.get_command_explanation(command)
        if explanation:
            print("\n" + explanation)
        
        # Check for dangerous patterns
        is_dangerous, danger_reason = CommandSafetyChecker.check(command)
        if is_dangerous:
            response = input(CommandSafetyChecker.format_warning(command, danger_reason))
            if response.lower() != "y":
                print("Command execution cancelled.")
                self.history.add(command, executed=False)
                return False
        
        # Ask for confirmation
        print()
        response = input(f"Run this command? (y/n): ").strip().lower()
        
        if response != "y":
            print("Command execution cancelled.")
            self.history.add(command, executed=False)
            return False
        
        # Execute the command
        print("\nExecuting...\n")
        exit_code = self._execute_command(command)
        
        # Record in history
        self.history.add(command, executed=True, exit_code=exit_code)
        
        if exit_code == 0:
            print("\nCommand executed successfully.")
        else:
            print(f"\nCommand exited with code {exit_code}.")
        
        return True
    
    def _execute_command(self, command: str) -> int:
        """
        Execute a shell command and return the exit code.
        
        Args:
            command: The command to execute
        
        Returns:
            Exit code from the command
        """
        try:
            # Use shell=True to allow pipes, redirects, etc.
            result = subprocess.run(
                command,
                shell=True,
                capture_output=False,  # Show output directly to user
                text=True,
            )
            return result.returncode
        except Exception as e:
            print(f"Error executing command: {e}")
            return 1
    
    def show_history(self, count: int = 5):
        """Display recent command history."""
        print(self.history.format_recent(count))
    
    def show_config_status(self):
        """Display configuration status."""
        self.config.print_config_status()
    
    def run_config_wizard(self):
        """Run interactive configuration wizard."""
        self.config.configure_api_key()


def main():
    """CLI entry point."""
    import sys
    from argparse import ArgumentParser
    
    # Check if the first argument is a known command
    known_commands = ["config", "status", "history"]
    
    if len(sys.argv) > 1 and sys.argv[1] in known_commands:
        # Use subcommand parsing
        parser = ArgumentParser(
            description="Jalap - Intelligent Terminal Assistant",
            prog="jalap",
        )
        
        subparsers = parser.add_subparsers(dest="command", help="Commands")
        
        # config command
        config_parser = subparsers.add_parser("config", help="Configure API key")
        
        # status command
        status_parser = subparsers.add_parser("status", help="Show configuration status")
        
        # history command
        history_parser = subparsers.add_parser("history", help="Show recent commands")
        history_parser.add_argument(
            "-n", "--number",
            type=int,
            default=5,
            help="Number of recent commands to show (default: 5)"
        )
        
        args = parser.parse_args()
        
        # Initialize the AI
        jalap = JalapTerminalAI()
        
        # Handle commands
        if args.command == "config":
            jalap.run_config_wizard()
        elif args.command == "status":
            jalap.show_config_status()
        elif args.command == "history":
            jalap.show_history(args.number)
    else:
        # Treat all arguments as a query
        parser = ArgumentParser(
            description="Jalap - Intelligent Terminal Assistant",
            prog="jalap",
        )
        parser.add_argument("query", nargs="+", help="Your question or request")
        
        args = parser.parse_args()
        
        # Initialize the AI
        jalap = JalapTerminalAI()
        
        # Process a query
        query = " ".join(args.query)
        jalap.process_query(query)


if __name__ == "__main__":
    main()
