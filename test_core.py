import os
import shutil
import time
from core import SaveManager

def run_tests():
    print("Iniziando i test...")
    manager = SaveManager()
    
    # Setup dummy directories
    dummy_game = "DummyGameSaves"
    dummy_backup = "DummyBackups"
    
    if os.path.exists(dummy_game): shutil.rmtree(dummy_game)
    if os.path.exists(dummy_backup): shutil.rmtree(dummy_backup)
        
    os.makedirs(dummy_game)
    os.makedirs(dummy_backup)
    
    # Create dummy save file
    save_file = os.path.join(dummy_game, "save1.dat")
    with open(save_file, "w") as f:
        f.write("Dati di salvataggio originali")
        
    # Test configurazione
    print("Test: Salvataggio configurazione...")
    manager.save_config("Dummy", os.path.abspath(dummy_game), os.path.abspath(dummy_backup))
    
    # Test backup
    print("Test: Creazione backup...")
    success, msg = manager.create_backup()
    assert success, f"Backup fallito: {msg}"
    
    # Verifica che il backup esista
    backups = manager.get_backups()
    assert len(backups) == 1, "Nessun backup trovato"
    bck_name = backups[0]
    print(f"Backup creato: {bck_name}")
    
    # Modifica il salvataggio
    with open(save_file, "w") as f:
        f.write("Dati modificati (corrotti o andati avanti nel gioco)")
        
    # Test ripristino
    print("Test: Ripristino backup...")
    success, msg = manager.restore_backup(bck_name)
    assert success, f"Ripristino fallito: {msg}"
    
    # Verifica contenuto file
    with open(save_file, "r") as f:
        content = f.read()
    assert content == "Dati di salvataggio originali", "Contenuto del file non ripristinato correttamente"
    
    # Test eliminazione
    print("Test: Eliminazione backup...")
    success, msg = manager.delete_backup(bck_name)
    assert success, f"Eliminazione fallita: {msg}"
    
    backups = manager.get_backups()
    assert len(backups) == 0, "Il backup non è stato eliminato"

    # Cleanup finale
    if os.path.exists(dummy_game): shutil.rmtree(dummy_game)
    if os.path.exists(dummy_backup): shutil.rmtree(dummy_backup)
    if os.path.exists("config.json"): os.remove("config.json")
        
    print("Tutti i test completati con successo!")

if __name__ == "__main__":
    run_tests()
