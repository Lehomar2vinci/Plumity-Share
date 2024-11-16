import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser

# Contenu de base pour le .gitignore des projets Unity
unity_gitignore_base = """
# Fichiers et dossiers générés par Unity
[Ll]ibrary/
[Tt]emp/
[Oo]bj/
[Bb]uild/
[Bb]uilds/
[Ll]ogs/
[Mm]emoryCaptures/
sysinfo.xml
*.csproj
*.sln
*.suo
*.tmp
*.user
*.userprefs
*.pidb
*.booproj
*.svd
*.pdb
*.mdb
*.opendb
*.VC.db
.idea/
.vs/

# Packages installés via Unity Package Manager (si utilisés)
Packages/com.unity.*
"""

# Extensions de fichiers médias et volumineux
media_extensions = {
    "Textures (PNG, JPG, JPEG, TGA, TIFF)": ["*.png", "*.jpg", "*.jpeg", "*.tga", "*.tiff"],
    "Audio (WAV, MP3, OGG, FLAC)": ["*.wav", "*.mp3", "*.ogg", "*.flac"],
    "Vidéo (MP4, AVI, MOV, WMV, MKV)": ["*.mp4", "*.avi", "*.mov", "*.wmv", "*.mkv"],
    "Modèles 3D (FBX, OBJ, 3DS, BLEND)": ["*.fbx", "*.obj", "*.3ds", "*.blend"],
    "Autres fichiers volumineux (ZIP, EXE, RAR, DLL)": ["*.zip", "*.rar", "*.exe", "*.dll"],
    "Fichiers temporaires de sauvegarde": ["*.bak", "*.tmp"]
}

# Dictionnaire de traduction pour le multilingue
translations = {
    "fr": {
        "title": "Générateur de .gitignore pour Unity",
        "select_project": "Sélectionnez le dossier de votre projet Unity :",
        "exclude_files": "Choisissez les types de fichiers à exclure :",
        "generate_button": "Générer .gitignore et README",
        "ready": "Prêt à générer.",
        "generating": "Génération en cours... Veuillez patienter.",
        "success": "Les fichiers .gitignore et README.md ont été générés avec succès.",
        "error": "Le chemin du projet est invalide.",
        "about": "Nathan Chambrette - 2025",
        "about_link": "https://example.com",
    },
    "en": {
        "title": "Unity .gitignore Generator",
        "select_project": "Select your Unity project folder:",
        "exclude_files": "Choose file types to exclude:",
        "generate_button": "Generate .gitignore and README",
        "ready": "Ready to generate.",
        "generating": "Generating... Please wait.",
        "success": ".gitignore and README.md files generated successfully.",
        "error": "The project path is invalid.",
        "about": "Nathan Chambrette - 2025",
        "about_link": "https://example.com",
    }
}

# Fonction de traduction
current_language = "fr"
def translate(key):
    return translations[current_language][key]

# Fonction pour basculer la langue
def toggle_language():
    global current_language
    current_language = "en" if current_language == "fr" else "fr"
    update_ui_texts()

# Fonction pour mettre à jour les textes de l'UI
def update_ui_texts():
    root.title(translate("title"))
    title_label.config(text=translate("title"))
    path_label.config(text=translate("select_project"))
    options_label.config(text=translate("exclude_files"))
    generate_button.config(text=translate("generate_button"))
    status_label.config(text=translate("ready"))

# Fonction pour ouvrir le lien "à propos"
def open_about_link():
    webbrowser.open(translate("about_link"))

# Fonction pour afficher la fenêtre "À propos"
def show_about():
    about_window = tk.Toplevel(root)
    about_window.title("À propos")
    about_window.geometry("300x100")
    about_label = tk.Label(about_window, text=translate("about"), font=("Arial", 12))
    about_label.pack(pady=10)
    link = tk.Label(about_window, text=translate("about_link"), fg="blue", cursor="hand2")
    link.pack()
    link.bind("<Button-1>", lambda e: open_about_link())

# Fonction pour générer le .gitignore
def generate_gitignore(project_path, selected_extensions):
    gitignore_path = os.path.join(project_path, ".gitignore")
    with open(gitignore_path, "w") as gitignore_file:
        gitignore_file.write(unity_gitignore_base)  # Écrire les règles de base
        for ext_list in selected_extensions:
            for ext in ext_list:
                gitignore_file.write(f"{ext}\n")  # Ajouter chaque extension
    return gitignore_path

# Fonction pour lister les packages
def list_packages(project_path):
    packages = []
    packages_path = os.path.join(project_path, "Packages")
    if os.path.exists(packages_path):
        for item in os.listdir(packages_path):
            if item.endswith(".json"):
                packages.append(item)
    return packages

# Fonction pour lister les fichiers exclus
def list_excluded_files(project_path, selected_extensions):
    excluded_files = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            for ext_list in selected_extensions:
                if any(file.endswith(ext.strip("*")) for ext in ext_list):
                    excluded_files.append(os.path.relpath(os.path.join(root, file), project_path))
    return excluded_files

# Fonction pour générer le README
def generate_readme(project_path, packages, excluded_files):
    readme_path = os.path.join(project_path, "README.md")
    with open(readme_path, "w") as readme_file:
        readme_file.write("# Instructions de rechargement de packages et fichiers exclus\n\n")
        readme_file.write("## Packages nécessaires :\n\n")
        for package in packages:
            readme_file.write(f"- {package}\n")
        
        readme_file.write("\n## Fichiers exclus du suivi Git :\n\n")
        for file in excluded_files:
            readme_file.write(f"- {file}\n")
    return readme_path

def process_project():
    project_path = path_entry.get()
    if not os.path.isdir(project_path):
        messagebox.showerror("Erreur", translate("error"))
        return
    
    selected_extensions = [media_extensions[ext] for ext in ext_vars if ext_vars[ext].get()]
    
    status_label.config(text=translate("generating"))
    gitignore_path = generate_gitignore(project_path, selected_extensions)
    packages = list_packages(project_path)
    excluded_files = list_excluded_files(project_path, selected_extensions)
    readme_path = generate_readme(project_path, packages, excluded_files)
    
    status_label.config(text=f"{translate('success')}\n.gitignore : {gitignore_path}\nREADME.md: {readme_path}")
    messagebox.showinfo("Succès", f"{translate('success')}\n.gitignore : {gitignore_path}\nREADME.md: {readme_path}")

# Mode daltonien
is_colorblind_mode = False
def toggle_colorblind_mode():
    global is_colorblind_mode
    is_colorblind_mode = not is_colorblind_mode
    if is_colorblind_mode:
        root.config(bg="#000000")
        title_label.config(bg="#333333", fg="#FFD700")
        status_label.config(fg="#FFD700")
    else:
        root.config(bg="#f4f4f4")
        title_label.config(bg="#4CAF50", fg="white")
        status_label.config(fg="black")

# Fonction pour parcourir les dossiers
def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder_path)

# Création de l'interface graphique
root = tk.Tk()
root.title(translate("title"))
root.geometry("550x600")
root.configure(bg="#f4f4f4")

# Menu pour options supplémentaires
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

options_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Options", menu=options_menu)
options_menu.add_command(label="Mode Daltonien", command=toggle_colorblind_mode)
options_menu.add_command(label="Changer de langue", command=toggle_language)
options_menu.add_separator()
options_menu.add_command(label="À propos", command=show_about)

# Contenu de l'interface
title_label = tk.Label(root, text=translate("title"), font=("Arial", 16, "bold"), bg="#4CAF50", fg="white")
title_label.pack(pady=20)

# Champ pour le chemin du projet
path_label = tk.Label(root, text=translate("select_project"))
path_label.pack(pady=5)
path_entry = tk.Entry(root, width=40, font=("Arial", 10), relief="solid")
path_entry.pack(pady=5)

browse_button = ttk.Button(root, text="Parcourir", command=browse_folder)
browse_button.pack(pady=10)

# Frame pour les options d'extensions
options_frame = ttk.Frame(root)
options_frame.pack(pady=10)

# Label pour les options d'extensions
options_label = tk.Label(options_frame, text=translate("exclude_files"), bg="#f4f4f4")
options_label.pack()

# Cases à cocher pour les extensions
ext_vars = {}
for ext_name in media_extensions:
    var = tk.BooleanVar()
    ext_vars[ext_name] = var
    cb = ttk.Checkbutton(options_frame, text=ext_name, variable=var)
    cb.pack(anchor="w")

# Barre de progression
progress_frame = ttk.Frame(root)
progress_frame.pack(pady=10)
progress_bar = ttk.Progressbar(progress_frame, length=300, mode="indeterminate")
progress_bar.pack()

# Label pour l'état de la génération
status_label = tk.Label(root, text=translate("ready"), bg="#f4f4f4", font=("Arial", 10, "italic"))
status_label.pack(pady=20)

# Bouton pour générer le .gitignore et README
generate_button = ttk.Button(root, text=translate("generate_button"), command=process_project)
generate_button.pack(pady=20)

# Boucle principale de l'interface
root.mainloop()
