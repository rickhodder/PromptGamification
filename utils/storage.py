"""
JSON-based storage utility for Promptification
Handles CRUD operations for prompts and users with file locking
"""

import json
import os
from typing import List, Optional, Dict, Any
from pathlib import Path
from datetime import datetime
import threading

from models import Prompt, User


class JSONStorage:
    """Thread-safe JSON storage handler"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.prompts_file = self.data_dir / "prompts.json"
        self.users_file = self.data_dir / "users.json"
        self._lock = threading.Lock()
        
        # Initialize files if they don't exist
        self._initialize_files()
    
    def _initialize_files(self):
        """Create empty JSON files if they don't exist"""
        if not self.prompts_file.exists():
            self._write_json(self.prompts_file, [])
        if not self.users_file.exists():
            self._write_json(self.users_file, [])
    
    def _read_json(self, file_path: Path) -> List[Dict[str, Any]]:
        """Read JSON file with error handling"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _write_json(self, file_path: Path, data: List[Dict[str, Any]]):
        """Write JSON file with pretty formatting"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    
    # Prompt Operations
    
    def save_prompt(self, prompt: Prompt) -> Prompt:
        """Save or update a prompt"""
        with self._lock:
            prompts = self._read_json(self.prompts_file)
            prompt.updated_at = datetime.now()
            prompt_dict = prompt.model_dump(mode='json')
            
            # Update existing or append new
            updated = False
            for i, p in enumerate(prompts):
                if p.get('id') == prompt.id:
                    prompts[i] = prompt_dict
                    updated = True
                    break
            
            if not updated:
                prompts.append(prompt_dict)
            
            self._write_json(self.prompts_file, prompts)
            return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Get a single prompt by ID"""
        prompts = self._read_json(self.prompts_file)
        for p in prompts:
            if p.get('id') == prompt_id:
                return Prompt(**p)
        return None
    
    def get_user_prompts(self, user_id: str) -> List[Prompt]:
        """Get all prompts for a user"""
        prompts = self._read_json(self.prompts_file)
        user_prompts = [Prompt(**p) for p in prompts if p.get('user_id') == user_id]
        # Sort by created_at descending
        user_prompts.sort(key=lambda x: x.created_at, reverse=True)
        return user_prompts
    
    def search_prompts(self, user_id: str, query: str = "", tags: List[str] = None) -> List[Prompt]:
        """Search prompts by text and/or tags"""
        prompts = self.get_user_prompts(user_id)
        
        if query:
            query_lower = query.lower()
            prompts = [
                p for p in prompts
                if query_lower in p.prompt_text.lower()
                or (p.description and query_lower in p.description.lower())
            ]
        
        if tags:
            prompts = [
                p for p in prompts
                if any(tag in p.tags for tag in tags)
            ]
        
        return prompts
    
    def get_templates(self, user_id: str) -> List[Prompt]:
        """Get all prompts marked as templates"""
        prompts = self.get_user_prompts(user_id)
        return [p for p in prompts if p.is_template]
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Delete a prompt by ID"""
        with self._lock:
            prompts = self._read_json(self.prompts_file)
            original_length = len(prompts)
            prompts = [p for p in prompts if p.get('id') != prompt_id]
            
            if len(prompts) < original_length:
                self._write_json(self.prompts_file, prompts)
                return True
            return False
    
    # User Operations
    
    def save_user(self, user: User) -> User:
        """Save or update a user"""
        with self._lock:
            users = self._read_json(self.users_file)
            user.last_active_at = datetime.now()
            user_dict = user.model_dump(mode='json')
            
            # Update existing or append new
            updated = False
            for i, u in enumerate(users):
                if u.get('user_id') == user.user_id:
                    users[i] = user_dict
                    updated = True
                    break
            
            if not updated:
                users.append(user_dict)
            
            self._write_json(self.users_file, users)
            return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get a user by ID"""
        users = self._read_json(self.users_file)
        for u in users:
            if u.get('user_id') == user_id:
                return User(**u)
        return None
    
    def get_or_create_user(self, user_id: str, username: str = None) -> User:
        """Get existing user or create new one"""
        user = self.get_user(user_id)
        if user:
            return user
        
        # Create new user
        user = User(user_id=user_id, username=username or user_id)
        return self.save_user(user)


# Global storage instance
storage = JSONStorage()
