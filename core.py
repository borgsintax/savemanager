import os
import shutil
import json
from datetime import datetime
from i18n import i18n, _

CONFIG_FILE = "config.json"

class SaveManager:
    def __init__(self):
        self.config = {
            "language": "it",
            "current_game": "",
            "games": {}
        }
        self.load_config()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    file_conf = json.load(f)
                    
                # Migration from legacy format
                if "game_name" in file_conf:
                    old_game = file_conf.get("game_name", "").strip()
                    if old_game:
                        self.config["current_game"] = old_game
                        self.config["games"][old_game] = {
                            "source_path": file_conf.get("source_path", ""),
                            "backup_path": file_conf.get("backup_path", "")
                        }
                    # Keep language
                    if "language" in file_conf:
                        self.config["language"] = file_conf["language"]
                        
                    # Save the migrated config immediately
                    self._save_config_file()
                else:
                    self.config.update(file_conf)
                
                # Apply language from config
                loaded_lang = self.config.get("language", "it")
                i18n.set_language(loaded_lang)
            except Exception as e:
                print(f"Error loading configuration: {e}")

    def _save_config_file(self):
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving configuration: {e}")
            return False

    def get_games(self):
        return list(self.config.get("games", {}).keys())

    def get_game_config(self, game_name):
        return self.config.get("games", {}).get(game_name, {"source_path": "", "backup_path": ""})

    def save_config(self, game_name, source_path, backup_path, language=None):
        game_name = game_name.strip()
        if not game_name:
            return False
            
        self.config["current_game"] = game_name
        self.config["games"][game_name] = {
            "source_path": source_path,
            "backup_path": backup_path
        }
        
        if language:
            self.config["language"] = language
            i18n.set_language(language)
            
        return self._save_config_file()

    def _migrate_old_backups(self, root_backup_dir, game_name):
        if not os.path.exists(root_backup_dir):
            return
            
        target_dir = os.path.join(root_backup_dir, game_name)
        
        for item in os.listdir(root_backup_dir):
            item_path = os.path.join(root_backup_dir, item)
            if os.path.isdir(item_path) and item.startswith(f"{game_name}_Backup_"):
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir, exist_ok=True)
                try:
                    new_path = os.path.join(target_dir, item)
                    os.rename(item_path, new_path)
                except Exception as e:
                    print(f"Error migrating backup {item}: {e}")

    def create_backup(self):
        game_name = self.config.get("current_game")
        if not game_name:
            return False, _("err_invalid_source")
            
        game_conf = self.get_game_config(game_name)
        source = game_conf.get("source_path")
        root_backup_dir = game_conf.get("backup_path")

        if not source or not os.path.exists(source):
            return False, _("err_invalid_source")
        
        if not root_backup_dir or not os.path.exists(root_backup_dir):
            return False, _("err_invalid_backup")

        backup_dir = os.path.join(root_backup_dir, game_name)
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_name = f"{game_name}_Backup_{timestamp}"
        target_path = os.path.join(backup_dir, backup_name)

        try:
            shutil.copytree(source, target_path)
            return True, _("msg_backup_success", target_path)
        except Exception as e:
            return False, _("err_backup_exception", str(e))

    def get_backups(self):
        game_name = self.config.get("current_game")
        if not game_name:
            return []
            
        game_conf = self.get_game_config(game_name)
        root_backup_dir = game_conf.get("backup_path")
        
        if not root_backup_dir or not os.path.exists(root_backup_dir):
            return []
            
        self._migrate_old_backups(root_backup_dir, game_name)

        backup_dir = os.path.join(root_backup_dir, game_name)
        backups = []

        if os.path.exists(backup_dir):
            for item in os.listdir(backup_dir):
                item_path = os.path.join(backup_dir, item)
                if os.path.isdir(item_path) and item.startswith(f"{game_name}_Backup_"):
                    backups.append({"name": item, "path": item_path})
            
            backups.sort(key=lambda x: x["name"], reverse=True)
            
        return [b["name"] for b in backups]

    def restore_backup(self, backup_name):
        game_name = self.config.get("current_game")
        if not game_name or not backup_name:
            return False, _("err_config_restore")
            
        game_conf = self.get_game_config(game_name)
        source = game_conf.get("source_path")
        root_backup_dir = game_conf.get("backup_path")

        if not source or not root_backup_dir:
            return False, _("err_config_restore")

        backup_path = os.path.join(root_backup_dir, game_name, backup_name)
        if not os.path.exists(backup_path):
            return False, _("err_backup_missing")

        try:
            if os.path.exists(source):
                shutil.rmtree(source)
            shutil.copytree(backup_path, source)
            return True, _("msg_restore_success")
        except Exception as e:
            return False, _("err_restore_exception", str(e))

    def delete_backup(self, backup_name):
        game_name = self.config.get("current_game")
        if not game_name or not backup_name:
            return False, _("err_config_restore")
            
        game_conf = self.get_game_config(game_name)
        root_backup_dir = game_conf.get("backup_path")
        if not root_backup_dir:
            return False, _("err_config_restore")

        backup_path = os.path.join(root_backup_dir, game_name, backup_name)
        if not os.path.exists(backup_path):
            return False, _("err_delete_missing")

        try:
            shutil.rmtree(backup_path)
            return True, _("msg_delete_success")
        except Exception as e:
            return False, _("err_delete_exception", str(e))

    def rename_backup(self, old_name, new_name_suffix):
        game_name = self.config.get("current_game")
        if not game_name or not old_name or not new_name_suffix:
            return False, _("err_config_restore")
            
        game_conf = self.get_game_config(game_name)
        root_backup_dir = game_conf.get("backup_path")
        
        if not root_backup_dir:
            return False, _("err_config_restore")
            
        new_name_suffix = "".join([c for c in new_name_suffix if c.isalpha() or c.isdigit() or c in [' ', '-', '_']]).strip()
        if not new_name_suffix:
            return False, _("err_rename_invalid")

        prefix = f"{game_name}_Backup_"
        base_name = old_name
        
        if old_name.startswith(prefix):
            rest = old_name[len(prefix):]
            if len(rest) >= 19:
                timestamp = rest[:19]
                base_name = prefix + timestamp

        new_name = f"{base_name} - {new_name_suffix}"

        if old_name == new_name:
            return False, _("err_rename_invalid")

        backup_dir = os.path.join(root_backup_dir, game_name)
        old_path = os.path.join(backup_dir, old_name)
        new_path = os.path.join(backup_dir, new_name)
        
        if not os.path.exists(old_path):
            return False, _("err_backup_missing")

        if os.path.exists(new_path):
            return False, _("err_rename_invalid")

        try:
            os.rename(old_path, new_path)
            return True, _("msg_rename_success")
        except Exception as e:
            return False, _("err_rename_exception", str(e))
