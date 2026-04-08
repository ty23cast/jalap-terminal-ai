import requests
import json
from typing import Dict, Optional
from abc import ABC, abstractmethod


class AIProvider(ABC):
    """Abstract base class for AI providers."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    @abstractmethod
    def get_command_suggestion(self, query: str, context: Dict) -> Optional[str]:
        """Get a command suggestion based on user query and context."""
        pass
    
    @abstractmethod
    def get_command_explanation(self, command: str) -> Optional[str]:
        """Get an explanation of what a command does."""
        pass


class OpenAIProvider(AIProvider):
    """OpenAI API integration."""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://api.openai.com/v1"
        self.model = "gpt-3.5-turbo"
    
    def get_command_suggestion(self, query: str, context: Dict) -> Optional[str]:
        """Get a command suggestion from OpenAI."""
        try:
            prompt = self._build_prompt(query, context)
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a helpful terminal assistant. Respond with ONLY the command to run, no explanation.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    "max_tokens": 150,
                    "temperature": 0.3,
                },
                timeout=10,
            )
            
            if response.status_code == 200:
                result = response.json()
                command = result["choices"][0]["message"]["content"].strip()
                # Remove markdown code blocks if present
                command = command.replace("```bash", "").replace("```", "").strip()
                return command
            else:
                print(f"OpenAI API Error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"OpenAI Connection Error: {e}")
            return None
        except (KeyError, json.JSONDecodeError) as e:
            print(f"OpenAI Response Parse Error: {e}")
            return None
    
    def get_command_explanation(self, command: str) -> Optional[str]:
        """Get an explanation from OpenAI."""
        try:
            prompt = f"""Explain this command in detail, breaking down each flag and option:

Command: {command}

Format your response like this:
Command Description: [one line description]

Flags:
-flag1: [explanation]
-flag2: [explanation]
...

Do not include anything else in the response."""
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a helpful terminal assistant. Explain commands clearly and concisely.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    "max_tokens": 300,
                    "temperature": 0.3,
                },
                timeout=10,
            )
            
            if response.status_code == 200:
                result = response.json()
                explanation = result["choices"][0]["message"]["content"].strip()
                return explanation
            else:
                return None
                
        except (requests.exceptions.RequestException, KeyError, json.JSONDecodeError):
            return None
    
    def _build_prompt(self, query: str, context: Dict) -> str:
        """Build a detailed prompt based on user query and system context."""
        shell = context.get("shell", "unknown")
        os_type = context.get("os", "unknown")
        cwd = context.get("cwd", "unknown")
        
        return f"""The user is on {os_type} with {shell} shell, in directory: {cwd}

User request: {query}

Provide ONLY the command to run, nothing else. Make sure it's compatible with {shell}."""


class AnthropicProvider(AIProvider):
    """Anthropic Claude API integration."""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.model = "claude-3-sonnet-20240229"
    
    def get_command_suggestion(self, query: str, context: Dict) -> Optional[str]:
        """Get a command suggestion from Anthropic."""
        try:
            shell = context.get("shell", "unknown")
            os_type = context.get("os", "unknown")
            cwd = context.get("cwd", "unknown")
            
            prompt = f"""The user is on {os_type} with {shell} shell, in directory: {cwd}

User request: {query}

Provide ONLY the command to run, nothing else. Make sure it's compatible with {shell}."""
            
            response = requests.post(
                self.base_url,
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "max_tokens": 150,
                    "temperature": 0.3,
                    "system": "You are a helpful terminal assistant. Respond with ONLY the command to run, no explanation.",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                },
                timeout=10,
            )
            
            if response.status_code == 200:
                result = response.json()
                command = result["content"][0]["text"].strip()
                # Remove markdown code blocks if present
                command = command.replace("```bash", "").replace("```", "").strip()
                return command
            else:
                print(f"Anthropic API Error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Anthropic Connection Error: {e}")
            return None
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Anthropic Response Parse Error: {e}")
            return None
    
    def get_command_explanation(self, command: str) -> Optional[str]:
        """Get an explanation from Anthropic."""
        try:
            prompt = f"""Explain this command in detail, breaking down each flag and option:

Command: {command}

Format your response like this:
Command Description: [one line description]

Flags:
-flag1: [explanation]
-flag2: [explanation]
...

Do not include anything else in the response."""
            
            response = requests.post(
                self.base_url,
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "max_tokens": 300,
                    "temperature": 0.3,
                    "system": "You are a helpful terminal assistant. Explain commands clearly and concisely.",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                },
                timeout=10,
            )
            
            if response.status_code == 200:
                result = response.json()
                explanation = result["content"][0]["text"].strip()
                return explanation
            else:
                return None
                
        except (requests.exceptions.RequestException, KeyError, json.JSONDecodeError):
            return None


class GoogleProvider(AIProvider):
    """Google Gemini API integration."""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    
    def get_command_suggestion(self, query: str, context: Dict) -> Optional[str]:
        """Get a command suggestion from Google Gemini."""
        try:
            shell = context.get("shell", "unknown")
            os_type = context.get("os", "unknown")
            cwd = context.get("cwd", "unknown")
            
            prompt = f"""The user is on {os_type} with {shell} shell, in directory: {cwd}

User request: {query}

Provide ONLY the command to run, nothing else. Make sure it's compatible with {shell}."""
            
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                headers={
                    "Content-Type": "application/json",
                },
                json={
                    "contents": [
                        {
                            "parts": [
                                {
                                    "text": f"You are a helpful terminal assistant. Respond with ONLY the command to run, no explanation.\n\n{prompt}"
                                }
                            ]
                        }
                    ],
                    "generationConfig": {
                        "temperature": 0.3,
                        "maxOutputTokens": 150,
                    }
                },
                timeout=10,
            )
            
            if response.status_code == 200:
                result = response.json()
                command = result["candidates"][0]["content"]["parts"][0]["text"].strip()
                # Remove markdown code blocks if present
                command = command.replace("```bash", "").replace("```", "").strip()
                return command
            else:
                print(f"Google API Error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Google Connection Error: {e}")
            return None
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Google Response Parse Error: {e}")
            return None
    
    def get_command_explanation(self, command: str) -> Optional[str]:
        """Get an explanation from Google Gemini."""
        try:
            prompt = f"""Explain this command in detail, breaking down each flag and option:

Command: {command}

Format your response like this:
Command Description: [one line description]

Flags:
-flag1: [explanation]
-flag2: [explanation]
...

Do not include anything else in the response."""
            
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                headers={
                    "Content-Type": "application/json",
                },
                json={
                    "contents": [
                        {
                            "parts": [
                                {
                                    "text": f"You are a helpful terminal assistant. Explain commands clearly and concisely.\n\n{prompt}"
                                }
                            ]
                        }
                    ],
                    "generationConfig": {
                        "temperature": 0.3,
                        "maxOutputTokens": 300,
                    }
                },
                timeout=10,
            )
            
            if response.status_code == 200:
                result = response.json()
                explanation = result["candidates"][0]["content"]["parts"][0]["text"].strip()
                return explanation
            else:
                return None
                
        except (requests.exceptions.RequestException, KeyError, json.JSONDecodeError):
            return None


class AIIntegration:
    """
    Generic AI integration that can handle multiple providers.
    Automatically detects the provider based on API key format or environment variables.
    """
    
    def __init__(self, api_key: str, provider: str = None):
        self.api_key = api_key
        self.provider_name = provider or self._detect_provider(api_key)
        self.provider = self._create_provider(self.provider_name, api_key)
    
    def _detect_provider(self, api_key: str) -> str:
        """
        Detect the AI provider based on API key format.
        This is a heuristic and may not be 100% accurate.
        """
        if api_key.startswith("sk-"):
            return "openai"
        elif api_key.startswith("sk-ant-"):
            return "anthropic"
        elif len(api_key) == 39 and api_key.replace("-", "").isalnum():
            # Google API keys are typically 39 characters with dashes
            return "google"
        else:
            # Default to OpenAI if can't detect
            return "openai"
    
    def _create_provider(self, provider_name: str, api_key: str) -> AIProvider:
        """Create the appropriate provider instance."""
        providers = {
            "openai": OpenAIProvider,
            "anthropic": AnthropicProvider,
            "google": GoogleProvider,
        }
        
        provider_class = providers.get(provider_name.lower())
        if provider_class:
            return provider_class(api_key)
        else:
            # Default to OpenAI if provider not recognized
            print(f"Unknown provider '{provider_name}', defaulting to OpenAI")
            return OpenAIProvider(api_key)
    
    def get_command_suggestion(self, query: str, context: Dict) -> Optional[str]:
        """Get a command suggestion from the configured AI provider."""
        return self.provider.get_command_suggestion(query, context)
    
    def get_command_explanation(self, command: str) -> Optional[str]:
        """Get an explanation from the configured AI provider."""
        return self.provider.get_command_explanation(command)


# Mock AI for testing (fallback when API is unavailable)
class MockAI:
    """Fallback mock AI for demonstration/testing without API key."""
    
    @staticmethod
    def get_command_suggestion(query: str, context: Dict) -> Optional[str]:
        """Return a mock command based on keywords in query."""
        query_lower = query.lower()
        os_type = context.get("os", "unknown")
        shell = context.get("shell", "unknown")
        
        # Simple keyword matching for demo
        if "list" in query_lower or "show" in query_lower or "all files" in query_lower:
            return "ls -la"
        elif "create" in query_lower or "new" in query_lower or "directory" in query_lower or "mkdir" in query_lower:
            return "mkdir -p"
        elif "remove" in query_lower or "delete" in query_lower or "rm" in query_lower:
            return "rm -i"
        elif "search" in query_lower or "grep" in query_lower or "find" in query_lower:
            return "grep -r"
        elif "current" in query_lower or "directory" in query_lower or "pwd" in query_lower:
            return "pwd"
        elif "history" in query_lower or "last" in query_lower:
            return "history | tail -20"
        else:
            return "echo 'Command suggestion unavailable'"
    
    @staticmethod
    def get_command_explanation(command: str) -> Optional[str]:
        """Return a mock explanation."""
        return f"""Command Description: {command}

Note: This is a generic explanation since the AI API is not configured.
For detailed explanations, please set up your OpenAI API key with 'jalap config'."""
