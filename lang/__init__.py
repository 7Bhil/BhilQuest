"""
Language System for BhilQuest
Internationalization (i18n) system
"""

import os
from typing import Dict, Any

class LanguageManager:
    """Manages language loading and text retrieval"""
    
    def __init__(self, language: str = "en"):
        self.language = language
        self.translations = {}
        self.load_language(language)
    
    def load_language(self, language: str):
        """Load language pack"""
        try:
            if language == "fr":
                from . import fr as lang_module
            else:
                from . import en as lang_module
            
            # Load all constants from the language module
            self.translations = {
                attr: getattr(lang_module, attr)
                for attr in dir(lang_module)
                if not attr.startswith('_') and not callable(getattr(lang_module, attr))
            }
            
            self.language = language
            
        except ImportError as e:
            print(f"Error loading language {language}: {e}")
            # Fallback to English
            try:
                from . import en as lang_module
                self.translations = {
                    attr: getattr(lang_module, attr)
                    for attr in dir(lang_module)
                    if not attr.startswith('_') and not callable(getattr(lang_module, attr))
                }
                self.language = "en"
            except ImportError:
                print("Critical error: Cannot load any language pack!")
                self.translations = {}
                self.language = "en"
    
    def get(self, key: str, **kwargs) -> str:
        """Get translated text with optional formatting"""
        text = self.translations.get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except (KeyError, ValueError):
                return text
        return text
    
    def t(self, key: str, **kwargs) -> str:
        """Shortcut for get()"""
        return self.get(key, **kwargs)

# Global language manager instance
_current_language = "en"
_lang_manager = None

def set_language(language: str):
    """Set the current language"""
    global _current_language, _lang_manager
    _current_language = language
    _lang_manager = LanguageManager(language)

def get_language() -> str:
    """Get the current language"""
    return _current_language

def t(key: str, **kwargs) -> str:
    """Get translated text (shortcut)"""
    global _lang_manager
    if _lang_manager is None:
        _lang_manager = LanguageManager(_current_language)
    return _lang_manager.get(key, **kwargs)

# Initialize with default language
set_language("en")
