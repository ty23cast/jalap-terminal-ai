# Jalap Terminal AI

An intelligent terminal assistant that understands your system context and helps you run commands safely.

## Features

- **Context Awareness**: Automatically detects your OS (macOS, Linux, Windows) and shell (zsh, bash, PowerShell) to provide appropriate commands
- **Command Explainer**: Breaks down what each command and flag does so you learn as you go
- **History Aware**: Remembers your recent commands so you can ask questions like "how do I undo what I just did?"
- **Safety First**: Flags dangerous commands before execution (rm -rf, sudo, shell pipes, etc.)
- **One-Click Execute**: Prompts for confirmation before running any command
- **AI-Powered**: Uses OpenAI's API to understand natural language and suggest precise commands

## Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/jalap-terminal-ai.git
cd jalap-terminal-ai
```

2. Install in development mode:
```bash
pip install -e .
```

Or install with dev dependencies:
```bash
pip install -e ".[dev]"
```

## Configuration

### Setting Up Your API Key

Jalap supports multiple AI providers. You can use OpenAI, Anthropic (Claude), or Google Gemini. You have several options for configuration:

#### Option 1: Interactive Setup (Recommended)

```bash
jalap config
```

This will guide you through selecting a provider and setting up your API key, which will be stored securely in your home directory (`~/.jalap.env`).

#### Option 2: Environment Variables

Set the API key in your shell for your preferred provider:

**For zsh/bash:**
```bash
# OpenAI (default)
export OPENAI_API_KEY="sk-your-openai-key"

# Anthropic Claude
export ANTHROPIC_API_KEY="sk-ant-your-anthropic-key"

# Google Gemini
export GOOGLE_API_KEY="your-google-key"
```

Add this to your `~/.zshrc` or `~/.bashrc` to make it permanent.

**For PowerShell:**
```powershell
# OpenAI
$env:OPENAI_API_KEY = "sk-your-openai-key"

# Anthropic
$env:ANTHROPIC_API_KEY = "sk-ant-your-anthropic-key"

# Google
$env:GOOGLE_API_KEY = "your-google-key"
```

#### Option 3: Project .env File

Create a `.env` file in the project directory with one of these:
```
# OpenAI
OPENAI_API_KEY=sk-your-openai-key

# Anthropic
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key

# Google
GOOGLE_API_KEY=your-google-key
```

**Note:** `.env` is in `.gitignore` and won't be committed.

### Supported AI Providers

- **OpenAI**: GPT-3.5-turbo (default, most compatible)
- **Anthropic**: Claude 3 Sonnet (excellent reasoning)
- **Google**: Gemini Pro (fast and capable)

Jalap will auto-detect your provider based on the API key format, or you can specify it during setup.

### Check Configuration Status

```bash
jalap status
```

This will show your configured provider and API key status.

## Usage

### Basic Query

Ask Jalap to help you with terminal commands in natural language:

```bash
jalap "how do I list all files including hidden ones?"
jalap "create a new directory called myproject"
jalap "what's my current directory?"
```

### View Command History

See your recent commands:

```bash
# Show last 5 commands
jalap history

# Show last 10 commands
jalap history -n 10
```

### Run Configuration Wizard

Set up or update your API key:

```bash
jalap config
```

## Example Session

```
$ jalap "list all files"

Current Context:
- OS: macos
- Shell: zsh
- Working Directory: /Users/username/projects
- User: username

Query: list all files

Generating command suggestion...

Suggested command: ls -la

Generating explanation...

Command Description: List directory contents with details and hidden files

Flags:
  -l: Long listing format (shows permissions, owner, size, date)
  -a: Include hidden files (those starting with .)

Run this command? (y/n): y

Executing...

total 16
drwxr-xr-x  4 username  staff  128 Apr  2 10:30 .
drwxr-xr-x  3 username  staff   96 Apr  2 10:29 ..
-rw-r--r--  1 username  staff    0 Apr  2 10:30 .hidden
-rw-r--r--  1 username  staff    0 Apr  2 10:30 file.txt

✅ Command executed successfully.
```

### Safety Warning Example

If you type something dangerous, Jalap will warn you:

```
Potentially Dangerous Command Detected
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reason: Deleting root directory

Command: rm -rf /

This command could cause data loss or system damage.
Are you sure you want to proceed? (y/N): N
Command execution cancelled.
```

## Architecture

```
jalap_terminal_ai/
├── __init__.py              # Main JalapTerminalAI class and CLI entry point
├── __main__.py              # Package entry point
├── context.py               # OS/shell/environment detection
├── history.py               # Command history storage and retrieval
├── safety.py                # Dangerous command pattern detection
├── config.py                # API key configuration management
└── ai_integration.py        # OpenAI API integration (with MockAI fallback)
```

### Key Components

**context.py**
- Detects OS, shell, current directory, and username
- Provides context to AI for OS/shell-specific command suggestions

**history.py**
- Records all executed commands with timestamps
- Stores history in `~/.jalap_history` (JSON format)
- Allows retrieval of recent commands

**safety.py**
- Scans commands for dangerous patterns (rm -rf, sudo, pipes to shell, etc.)
- Requires explicit user confirmation before running flagged commands

**config.py**
- Manages API key configuration
- Checks multiple sources: environment variables, .env files, home directory
- Provides interactive configuration wizard

**ai_integration.py**
- Integrates with OpenAI's GPT API
- Generates command suggestions and explanations

## Development

### Running Tests

```bash
pytest
```

### Code Style

We use Black for code formatting and Flake8 for linting:

```bash
black jalap_terminal_ai/
flake8 jalap_terminal_ai/
```

### Current Implementation Status

✅ Context awareness (OS/shell detection)  
✅ Command explainer with AI-powered explanations  
✅ History tracking and display  
✅ Safety warnings for dangerous commands  
✅ One-click execution with confirmation  
✅ AI integration with OpenAI API  
✅ Fallback to mock AI when API key unavailable  
✅ Interactive configuration wizard  

### Future Enhancements

1. **Multiple AI Providers**: Support Anthropic, Google, and other LLM providers
2. **Command Undo**: Implement safe undo for reversible operations
3. **Aliases**: Create custom command aliases and shortcuts
4. **Offline Mode**: Improved suggestions when internet is unavailable
5. **Shell Integration**: tighter integration with zsh/bash plugins
6. **Interactive Mode**: Conversational follow-ups and command chaining
7. **Logging**: Detailed audit logs of executed commands

## Troubleshooting

### "No API key configured"

Run `jalap config` to set up your OpenAI API key.

### Commands not executing

1. Check your API key: `jalap status`
2. Verify internet connection
3. Ensure the command is safe (not flagged by safety checks)

### History not saving

Check write permissions on `~/.jalap_history`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and add tests
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Disclaimer

This tool executes shell commands with user confirmation. While we include safety checks for dangerous patterns, always review suggested commands before execution.
