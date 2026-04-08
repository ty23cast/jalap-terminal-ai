import os
from pathlib import Path
from dotenv import load_dotenv, set_key


class ConfigManager:
    """Manages API key configuration and environment variables for multiple AI providers."""
    
    SUPPORTED_PROVIDERS = {
        "openai": {
            "name": "OpenAI",
            "env_vars": ["OPENAI_API_KEY"],
            "key_prefix": "sk-",
            "description": "OpenAI GPT models (ChatGPT)"
        },
        "anthropic": {
            "name": "Anthropic",
            "env_vars": ["ANTHROPIC_API_KEY", "CLAUDE_API_KEY"],
            "key_prefix": "sk-ant-",
            "description": "Anthropic Claude models"
        },
        "google": {
            "name": "Google",
            "env_vars": ["GOOGLE_API_KEY", "GEMINI_API_KEY"],
            "key_prefix": None,  # Google keys don't have a specific prefix
            "description": "Google Gemini models"
        }
    }
    
    def __init__(self):
        self.env_path = Path.home() / ".jalap.env"
        self.project_env_path = Path(".env")
        # Load both project .env and user's .env
        if self.project_env_path.exists():
            load_dotenv(self.project_env_path)
        if self.env_path.exists():
            load_dotenv(self.env_path)
    
    def get_api_key(self, provider: str = None) -> tuple[str, str]:
        """
        Get API key and provider from environment.
        
        Returns:
            Tuple of (api_key, provider_name) or (None, None) if not found
        """
        # If provider is specified, look for that specific provider
        if provider:
            provider_config = self.SUPPORTED_PROVIDERS.get(provider.lower())
            if provider_config:
                for env_var in provider_config["env_vars"]:
                    api_key = os.environ.get(env_var)
                    if api_key:
                        return api_key, provider.lower()
        
        # Auto-detect provider based on available keys
        for provider_name, provider_config in self.SUPPORTED_PROVIDERS.items():
            for env_var in provider_config["env_vars"]:
                api_key = os.environ.get(env_var)
                if api_key:
                    return api_key, provider_name
        
        # Legacy support for JALAP_API_KEY
        api_key = os.environ.get("JALAP_API_KEY")
        if api_key:
            return api_key, "openai"  # Default to OpenAI for legacy keys
        
        return None, None
    
    def get_provider(self) -> str:
        """Get the configured AI provider name."""
        _, provider = self.get_api_key()
        return provider
    
    def has_api_key(self) -> bool:
        """Check if an API key is configured."""
        api_key, _ = self.get_api_key()
        return api_key is not None
    
    def configure_api_key(self) -> bool:
        """
        Interactive setup for API key configuration.
        
        Returns:
            True if configuration was successful
        """
        print("\n" + "="*60)
        print("Jalap Terminal AI - API Key Configuration")
        print("="*60)
        print("\nTo use Jalap, you need to configure an API key.")
        print("This key will be stored securely in your home directory.\n")
        
        print("Available AI Providers:")
        for i, (key, config) in enumerate(self.SUPPORTED_PROVIDERS.items(), 1):
            print(f"{i}. {config['name']} - {config['description']}")
        print("4. Use environment variable (manual)")
        print("5. Skip for now (won't be able to use AI features)\n")
        
        choice = input("Choose option (1-5): ").strip()
        
        if choice in ["1", "2", "3"]:
            provider_idx = int(choice) - 1
            provider_names = list(self.SUPPORTED_PROVIDERS.keys())
            provider_name = provider_names[provider_idx]
            provider_config = self.SUPPORTED_PROVIDERS[provider_name]
            
            api_key = input(f"\nEnter your {provider_config['name']} API key: ").strip()
            if not api_key:
                print("No API key provided.")
                return False
            
            # Save to user's home directory .jalap.env
            env_var = provider_config["env_vars"][0]  # Use the first env var name
            set_key(str(self.env_path), env_var, api_key)
            load_dotenv(self.env_path)
            print(f"API key saved to {self.env_path}")
            print(f"   Provider: {provider_config['name']}")
            print("   This file is NOT committed to git and is kept secure.\n")
            return True
        
        elif choice == "4":
            print("\nManual setup:")
            print("Add one of these lines to your ~/.zshrc or ~/.bashrc:")
            for provider_config in self.SUPPORTED_PROVIDERS.values():
                env_var = provider_config["env_vars"][0]
                print(f'  export {env_var}="your-key-here"  # {provider_config["name"]}')
            print("\nThen restart your terminal.\n")
            return False
        
        else:
            print("\nSkipping API key configuration.")
            print("You can run 'jalap config' later to set it up.\n")
            return False
    
    def print_config_status(self):
        """Print current configuration status."""
        print("\n" + "="*60)
        print("Jalap Configuration Status")
        print("="*60)
        
        api_key, provider = self.get_api_key()
        if api_key and provider:
            provider_config = self.SUPPORTED_PROVIDERS.get(provider, {})
            provider_name = provider_config.get("name", provider.title())
            
            # Show masked key for security
            masked_key = api_key[:7] + "*" * (len(api_key) - 10) + api_key[-3:]
            print(f"API Key configured: {masked_key}")
            print(f"Provider: {provider_name}")
        else:
            print("No API key configured")
            print("   Run 'jalap config' to set one up")
        
        print(f"\nConfig file location: {self.env_path}")
        print(f"\nChecked locations:")
        for provider_config in self.SUPPORTED_PROVIDERS.values():
            for env_var in provider_config["env_vars"]:
                print(f"  - Environment variable: {env_var}")
        print(f"  - Environment variable: JALAP_API_KEY (legacy)")
        if self.project_env_path.exists():
            print(f"  - Project .env: {self.project_env_path}")
        print(f"  - User config: {self.env_path}")
        print()
