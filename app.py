import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from core import SaveManager
from i18n import i18n, _

VERSION = "1.0"
AUTHOR = "Francesco Duraccio - Aka Odo"
# Basic theme and color settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SaveManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.manager = SaveManager()
        
        # Apply title and geometry
        self.title(f"{_('window_title')} v{VERSION}")
        self.geometry("700x550")
        self.minsize(600, 500)

        self.setup_ui()
        self.load_ui_data()

    def setup_ui(self):
        # Main grid config
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # ---------------- FRAME TOP: Configurations ----------------
        self.config_frame = ctk.CTkFrame(self)
        self.config_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.config_frame.grid_columnconfigure(1, weight=1)

        # Game Name
        self.lbl_game_name = ctk.CTkLabel(self.config_frame, text=_("lbl_game_name"), font=("Helvetica", 14, "bold"))
        self.lbl_game_name.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        self.cmb_game_name = ctk.CTkComboBox(self.config_frame, command=self.on_game_select)
        self.cmb_game_name.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="ew", columnspan=2)
        
        self.btn_new_game = ctk.CTkButton(self.config_frame, text=_("btn_new_game"), width=60, command=self.new_game_profile)
        self.btn_new_game.grid(row=0, column=3, padx=(0, 10), pady=(10, 5))

        # Source Folder (Game)
        self.lbl_source = ctk.CTkLabel(self.config_frame, text=_("lbl_source"), font=("Helvetica", 14, "bold"))
        self.lbl_source.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.ent_source = ctk.CTkEntry(self.config_frame, placeholder_text=_("ent_source_placeholder"))
        self.ent_source.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.btn_browse_source = ctk.CTkButton(self.config_frame, text=_("btn_browse_source"), width=80, command=self.browse_source)
        self.btn_browse_source.grid(row=1, column=2, padx=(10, 5), pady=5)
        self.btn_open_source = ctk.CTkButton(self.config_frame, text=_("btn_open_folder"), width=60, fg_color="#5B5B5B", hover_color="#4B4B4B", command=self.open_source_folder)
        self.btn_open_source.grid(row=1, column=3, padx=(0, 10), pady=5)

        # Backup Folder (Destination)
        self.lbl_backup = ctk.CTkLabel(self.config_frame, text=_("lbl_backup"), font=("Helvetica", 14, "bold"))
        self.lbl_backup.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="w")
        self.ent_backup = ctk.CTkEntry(self.config_frame, placeholder_text=_("ent_backup_placeholder"))
        self.ent_backup.grid(row=2, column=1, padx=10, pady=(5, 10), sticky="ew")
        self.btn_browse_backup = ctk.CTkButton(self.config_frame, text=_("btn_browse_backup"), width=80, command=self.browse_backup)
        self.btn_browse_backup.grid(row=2, column=2, padx=(10, 5), pady=(5, 10))
        self.btn_open_backup = ctk.CTkButton(self.config_frame, text=_("btn_open_folder"), width=60, fg_color="#5B5B5B", hover_color="#4B4B4B", command=self.open_backup_folder)
        self.btn_open_backup.grid(row=2, column=3, padx=(0, 10), pady=(5, 10))
        
        # Language Selector
        self.lbl_language = ctk.CTkLabel(self.config_frame, text=_("lbl_language"), font=("Helvetica", 12))
        self.lbl_language.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        
        # Use a mapping dict for display vs internal value
        self.lang_map = {"Italiano": "it", "English": "en"}
        self.lang_reverse_map = {"it": "Italiano", "en": "English"}
        
        initial_lang_display = self.lang_reverse_map.get(i18n.get_language(), "Italiano")
        
        self.opt_language = ctk.CTkOptionMenu(self.config_frame, values=["Italiano", "English"], command=self.change_language)
        self.opt_language.set(initial_lang_display)
        self.opt_language.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        
        # Info / About Button
        self.btn_about = ctk.CTkButton(self.config_frame, text="?", width=30, fg_color="transparent", border_width=1, text_color=("gray10", "gray90"), command=self.show_about)
        self.btn_about.grid(row=3, column=3, padx=(0, 10), pady=5, sticky="e")

        # Save Config Button
        self.btn_save_config = ctk.CTkButton(self.config_frame, text=_("btn_save_config"), fg_color="green", hover_color="darkgreen", command=self.save_config)
        self.btn_save_config.grid(row=4, column=0, columnspan=4, padx=10, pady=(10, 10), sticky="ew")

        # ---------------- FRAME BOTTOM: List and Actions ----------------
        self.action_frame = ctk.CTkFrame(self)
        self.action_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.action_frame.grid_columnconfigure(0, weight=1)
        self.action_frame.grid_rowconfigure(1, weight=1)

        # Top Action Buttons (Refresh / Create)
        self.top_action_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.top_action_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.top_action_frame.grid_columnconfigure(0, weight=1)

        self.btn_refresh = ctk.CTkButton(self.top_action_frame, text=_("btn_refresh"), width=120, command=self.refresh_backup_list)
        self.btn_refresh.pack(side="left", padx=(0, 10))

        self.btn_create_backup = ctk.CTkButton(self.top_action_frame, text=_("btn_create_backup"), fg_color="#3A7EBF", hover_color="#2B5D8C", command=self.create_backup)
        self.btn_create_backup.pack(side="right")

        # Backup List (Listbox in standard tk wrapped in ctk frame)
        self.listbox_frame = ctk.CTkFrame(self.action_frame)
        self.listbox_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        self.backup_listbox = tk.Listbox(self.listbox_frame, bg="#2B2B2B", fg="#FFFFFF", selectbackground="#1F538D", 
                                         font=("Helvetica", 12), highlightthickness=0, borderwidth=0)
        self.backup_listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Scrollbar
        self.scrollbar = ctk.CTkScrollbar(self.listbox_frame, command=self.backup_listbox.yview)
        self.scrollbar.pack(side="right", fill="y", padx=2, pady=5)
        self.backup_listbox.configure(yscrollcommand=self.scrollbar.set)

        # Bottom Action Buttons (Delete / Restore)
        self.bottom_action_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.bottom_action_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        # Configure columns to distribute buttons evenly
        self.bottom_action_frame.grid_columnconfigure(0, weight=1)
        self.bottom_action_frame.grid_columnconfigure(1, weight=1)
        self.bottom_action_frame.grid_columnconfigure(2, weight=1)
        
        self.btn_delete_backup = ctk.CTkButton(self.bottom_action_frame, text=_("btn_delete_backup"), 
                                               fg_color="#A32424", hover_color="#7A1B1B", command=self.delete_backup)
        self.btn_delete_backup.grid(row=0, column=0, padx=5, sticky="ew")

        self.btn_rename_backup = ctk.CTkButton(self.bottom_action_frame, text=_("btn_rename_backup"), 
                                               fg_color="#4B4B4B", hover_color="#333333", command=self.rename_backup_ui)
        self.btn_rename_backup.grid(row=0, column=1, padx=5, sticky="ew")

        self.btn_restore = ctk.CTkButton(self.bottom_action_frame, text=_("btn_restore"), 
                                         fg_color="#D97A11", hover_color="#AB600D", command=self.restore_backup)
        self.btn_restore.grid(row=0, column=2, padx=5, sticky="ew")
        
    def refresh_ui_texts(self):
        """Updates all dynamic texts based on the selected language."""
        self.title(f"{_('window_title')} v{VERSION}")
        self.lbl_game_name.configure(text=_("lbl_game_name"))
        self.btn_new_game.configure(text=_("btn_new_game"))
        self.lbl_source.configure(text=_("lbl_source"))
        self.ent_source.configure(placeholder_text=_("ent_source_placeholder"))
        self.btn_browse_source.configure(text=_("btn_browse_source"))
        self.btn_open_source.configure(text=_("btn_open_folder"))
        self.lbl_backup.configure(text=_("lbl_backup"))
        self.ent_backup.configure(placeholder_text=_("ent_backup_placeholder"))
        self.btn_browse_backup.configure(text=_("btn_browse_backup"))
        self.btn_open_backup.configure(text=_("btn_open_folder"))
        self.lbl_language.configure(text=_("lbl_language"))
        self.btn_save_config.configure(text=_("btn_save_config"))
        self.btn_refresh.configure(text=_("btn_refresh"))
        self.btn_create_backup.configure(text=_("btn_create_backup"))
        self.btn_rename_backup.configure(text=_("btn_rename_backup"))
        self.btn_delete_backup.configure(text=_("btn_delete_backup"))
        self.btn_restore.configure(text=_("btn_restore"))

    def change_language(self, language_choice):
        lang_code = self.lang_map.get(language_choice, "it")
        i18n.set_language(lang_code)
        
        # We save language to config silently
        game = self.cmb_game_name.get().strip()
        if game:
            self.manager.save_config(
                game,
                self.ent_source.get().strip(),
                self.ent_backup.get().strip(),
                language=lang_code
            )
        self.refresh_ui_texts()

    def load_ui_data(self):
        """Populate fields with read config data"""
        games = self.manager.get_games()
        if games:
            self.cmb_game_name.configure(values=games)
            
        current = self.manager.config.get("current_game", "")
        if current:
            self.cmb_game_name.set(current)
            self.on_game_select(current)
        elif games:
            self.cmb_game_name.set(games[0])
            self.on_game_select(games[0])
        else:
            self.cmb_game_name.set("")
            
        self.refresh_backup_list()

    def on_game_select(self, choice):
        # Update fields based on selected game
        config = self.manager.get_game_config(choice)
        
        self.ent_source.delete(0, tk.END)
        self.ent_source.insert(0, config.get("source_path", ""))
        
        self.ent_backup.delete(0, tk.END)
        self.ent_backup.insert(0, config.get("backup_path", ""))
        
        # Update active game in manager so list refreshes properly
        self.manager.config["current_game"] = choice
        self.refresh_backup_list()

    def new_game_profile(self):
        self.cmb_game_name.set("")
        self.ent_source.delete(0, tk.END)
        self.ent_backup.delete(0, tk.END)
        self.manager.config["current_game"] = ""
        self.refresh_backup_list()

    def browse_source(self):
        folder = filedialog.askdirectory()
        if folder:
            self.ent_source.delete(0, tk.END)
            self.ent_source.insert(0, folder)

    def open_source_folder(self):
        folder = self.ent_source.get().strip()
        if folder and os.path.exists(folder):
            os.startfile(folder)
        else:
            messagebox.showwarning(_("msg_warning_title"), _("err_invalid_source"))

    def browse_backup(self):
        folder = filedialog.askdirectory()
        if folder:
            self.ent_backup.delete(0, tk.END)
            self.ent_backup.insert(0, folder)

    def open_backup_folder(self):
        folder = self.ent_backup.get().strip()
        if folder and os.path.exists(folder):
            os.startfile(folder)
        else:
            messagebox.showwarning(_("msg_warning_title"), _("err_invalid_backup"))

    def save_config(self):
        game = self.cmb_game_name.get().strip()
        src = self.ent_source.get().strip()
        bck = self.ent_backup.get().strip()
        
        # Get selected language code
        lang_code = self.lang_map.get(self.opt_language.get(), "it")
        
        if self.manager.save_config(game, src, bck, language=lang_code):
            messagebox.showinfo(_("msg_success_title"), _("msg_config_saved"))
            # Update combobox values in case a new game was added
            games = self.manager.get_games()
            if games:
                self.cmb_game_name.configure(values=games)
            self.refresh_backup_list()
        else:
            messagebox.showerror(_("msg_error_title"), _("msg_config_error"))

    def refresh_backup_list(self):
        self.backup_listbox.delete(0, tk.END)
        backups = self.manager.get_backups()
        for b in backups:
            self.backup_listbox.insert(tk.END, b)

    def create_backup(self):
        # Implicit save before acting
        self.save_config() 
        success, msg = self.manager.create_backup()
        if success:
            messagebox.showinfo(_("msg_backup_completed"), msg)
            self.refresh_backup_list()
        else:
            messagebox.showwarning(_("msg_backup_error"), msg)

    def get_selected_backup(self):
        selected_indices = self.backup_listbox.curselection()
        if not selected_indices:
            return None
        return self.backup_listbox.get(selected_indices[0])
        
    def rename_backup_ui(self):
        selected = self.get_selected_backup()
        if not selected:
            messagebox.showwarning(_("msg_warning_title"), _("msg_select_backup_rename"))
            return
            
        dialog = ctk.CTkInputDialog(text=_("dlg_rename_prompt", selected), title=_("dlg_rename_title"))
        new_name = dialog.get_input()
        
        if new_name is not None and new_name.strip() != "":
            success, msg = self.manager.rename_backup(selected, new_name)
            if success:
                messagebox.showinfo(_("msg_rename_completed_title"), msg)
                self.refresh_backup_list()
            else:
                messagebox.showerror(_("msg_rename_error"), msg)

    def restore_backup(self):
        selected = self.get_selected_backup()
        if not selected:
            messagebox.showwarning(_("msg_warning_title"), _("msg_select_backup_restore"))
            return
            
        confirm = messagebox.askyesno(_("msg_confirm_restore_title"), _("msg_confirm_restore_text", selected))
        if confirm:
            success, msg = self.manager.restore_backup(selected)
            if success:
                messagebox.showinfo(_("msg_restore_completed"), msg)
            else:
                messagebox.showerror(_("msg_restore_error"), msg)

    def delete_backup(self):
        selected = self.get_selected_backup()
        if not selected:
            messagebox.showwarning(_("msg_warning_title"), _("msg_select_backup_delete"))
            return

        confirm = messagebox.askyesno(_("msg_confirm_delete_title"), _("msg_confirm_delete_text", selected))
        if confirm:
            success, msg = self.manager.delete_backup(selected)
            if success:
                messagebox.showinfo(_("msg_delete_completed_title"), msg)
                self.refresh_backup_list()
            else:
                messagebox.showerror(_("msg_delete_error"), msg)

    def show_about(self):
        messagebox.showinfo(_("about_title"), _("about_text", VERSION, AUTHOR))

if __name__ == "__main__":
    app = SaveManagerApp()
    app.mainloop()
