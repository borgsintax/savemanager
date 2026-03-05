import json
import os

class I18N:
    def __init__(self):
        # Default language
        self.language = "it"
        
        # Translation dictionary
        self.translations = {
            "en": {
                "window_title": "Save Manager",
                "lbl_game_name": "Game Name:",
                "ent_game_name_placeholder": "Example: Elden Ring",
                "lbl_source": "Game Folder:",
                "ent_source_placeholder": "Save file path (e.g. C:\\Users\\...\\Saves)",
                "btn_browse_source": "Browse",
                "lbl_backup": "Backup Folder:",
                "ent_backup_placeholder": "Where to save backups (e.g. D:\\Games\\Backups)",
                "btn_browse_backup": "Browse",
                "btn_open_folder": "Open",
                "lbl_language": "Language:",
                "btn_new_game": "New",
                "about_title": "About Save Manager",
                "about_text": "Save Manager v{}\n\nDeveloped by {}",
                "btn_save_config": "Save Configuration",
                "btn_refresh": "Refresh List",
                "btn_create_backup": "Create New Backup",
                "btn_rename_backup": "Rename Selected",
                "btn_delete_backup": "Delete Selected",
                "btn_restore": "Restore Selected",
                "msg_success_title": "Success",
                "msg_config_saved": "Configuration saved successfully.",
                "msg_error_title": "Error",
                "msg_config_error": "Unable to save configuration.",
                "msg_backup_completed": "Backup Completed",
                "msg_backup_error": "Backup Error",
                "msg_warning_title": "Warning",
                "msg_select_backup_restore": "Select a backup from the list before restoring.",
                "msg_confirm_restore_title": "Confirm Restore",
                "msg_confirm_restore_text": "Are you sure you want to restore the backup:\n{}\n\nThe current save folder will be OVERWRITTEN.",
                "msg_restore_completed": "Restore Completed",
                "msg_restore_error": "Restore Error",
                "msg_select_backup_delete": "Select a backup from the list before deleting.",
                "msg_confirm_delete_title": "Confirm Deletion",
                "msg_confirm_delete_text": "Do you really want to permanently delete the backup:\n{}?",
                "msg_delete_completed_title": "Deletion",
                "msg_delete_error": "Deletion Error",
                "msg_select_backup_rename": "Select a backup from the list before renaming.",
                "dlg_rename_title": "Rename Backup",
                "dlg_rename_prompt": "Enter new name for:\n{}",
                "msg_rename_completed_title": "Renamed",
                "msg_rename_error": "Rename Error",
                
                # Core messages
                "err_invalid_source": "Invalid save path (source).",
                "err_invalid_backup": "Invalid backup path (destination).",
                "msg_backup_success": "Backup successfully created at:\n{}",
                "err_backup_exception": "Error during backup: {}",
                "err_config_restore": "Incomplete configuration or backup not selected.",
                "err_backup_missing": "The selected backup folder no longer exists.",
                "msg_restore_success": "Backup restored successfully!",
                "err_restore_exception": "Error during restore: {}",
                "err_delete_missing": "The selected backup does not exist.",
                "msg_delete_success": "Backup deleted successfully.",
                "err_delete_exception": "Error during deletion: {}",
                "err_rename_invalid": "Invalid name or name already exists in backup directory.",
                "msg_rename_success": "Backup renamed successfully.",
                "err_rename_exception": "Error during renaming: {}"
            },
            "it": {
                "window_title": "Save Manager",
                "lbl_game_name": "Nome Gioco:",
                "ent_game_name_placeholder": "Esempio: Elden Ring",
                "lbl_source": "Cartella Gioco:",
                "ent_source_placeholder": "Percorso file di salvataggio (es. C:\\Users\\...\\Saves)",
                "btn_browse_source": "Sfoglia",
                "lbl_backup": "Cartella Backup:",
                "ent_backup_placeholder": "Dove salvare i backup (es. D:\\Giochi\\Backups)",
                "btn_browse_backup": "Sfoglia",
                "btn_open_folder": "Apri",
                "lbl_language": "Lingua:",
                "btn_new_game": "Nuovo",
                "about_title": "Informazioni su Save Manager",
                "about_text": "Save Manager v{}\n\nSviluppato da {}",
                "btn_save_config": "Salva Configurazione",
                "btn_refresh": "Aggiorna Lista",
                "btn_create_backup": "Crea Nuovo Backup",
                "btn_rename_backup": "Rinomina Selezionato",
                "btn_delete_backup": "Elimina Selezionato",
                "btn_restore": "Ripristina Selezionato",
                "msg_success_title": "Successo",
                "msg_config_saved": "Configurazione salvata correttamente.",
                "msg_error_title": "Errore",
                "msg_config_error": "Impossibile salvare la configurazione.",
                "msg_backup_completed": "Backup Completato",
                "msg_backup_error": "Errore Backup",
                "msg_warning_title": "Attenzione",
                "msg_select_backup_restore": "Seleziona un backup dalla lista prima di ripristinare.",
                "msg_confirm_restore_title": "Conferma Ripristino",
                "msg_confirm_restore_text": "Sei sicuro di voler ripristinare il backup:\n{}\n\nLa cartella dei salvataggi attuale verrà SOVRASCRITTA.",
                "msg_restore_completed": "Ripristino Completato",
                "msg_restore_error": "Errore Ripristino",
                "msg_select_backup_delete": "Seleziona un backup dalla lista prima di eliminarlo.",
                "msg_confirm_delete_title": "Conferma Eliminazione",
                "msg_confirm_delete_text": "Vuoi davvero eliminare definitivamente il backup:\n{}?",
                "msg_delete_completed_title": "Eliminazione",
                "msg_delete_error": "Errore Eliminazione",
                "msg_select_backup_rename": "Seleziona un backup dalla lista prima di rinominarlo.",
                "dlg_rename_title": "Rinomina Backup",
                "dlg_rename_prompt": "Inserisci il nuovo nome per:\n{}",
                "msg_rename_completed_title": "Rinominato",
                "msg_rename_error": "Errore Rinomina",
                
                # Core messages
                "err_invalid_source": "Percorso dei salvataggi (origine) non valido.",
                "err_invalid_backup": "Percorso di backup (destinazione) non valido.",
                "msg_backup_success": "Backup creato con successo in:\n{}",
                "err_backup_exception": "Errore durante il backup: {}",
                "err_config_restore": "Configurazione incompleta o backup non selezionato.",
                "err_backup_missing": "La cartella di backup selezionata non esiste più.",
                "msg_restore_success": "Backup ripristinato con successo!",
                "err_restore_exception": "Errore durante il ripristino: {}",
                "err_delete_missing": "Il backup selezionato non esiste.",
                "msg_delete_success": "Backup eliminato con successo.",
                "err_delete_exception": "Errore durante l'eliminazione: {}",
                "err_rename_invalid": "Nome non valido o nome già esistente nella cartella di backup.",
                "msg_rename_success": "Backup rinominato con successo.",
                "err_rename_exception": "Errore durante il ripristino del nome: {}"
            }
        }

    def set_language(self, lang_code):
        if lang_code in self.translations:
            self.language = lang_code
            
    def get_language(self):
        return self.language

    def _(self, key, *args):
        """Returns the translated string for the given key in the current language."""
        text = self.translations.get(self.language, {}).get(key, key)
        if args:
            return text.format(*args)
        return text

# Global instance for easy import
i18n = I18N()
_ = i18n._
