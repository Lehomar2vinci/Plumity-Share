import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser

# Base contain for .gitignore Unity projects
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

# Installated packages via Unity Package Manager (if used..)
Packages/com.unity.*
"""

# Extensions for massive file contains
media_extensions = {
    "Textures (PNG, JPG, JPEG, TGA, TIFF)": ["*.png", "*.jpg", "*.jpeg", "*.tga", "*.tiff"],
    "Audio (WAV, MP3, OGG, FLAC)": ["*.wav", "*.mp3", "*.ogg", "*.flac"],
    "Vidéo (MP4, AVI, MOV, WMV, MKV)": ["*.mp4", "*.avi", "*.mov", "*.wmv", "*.mkv"],
    "Modèles 3D (FBX, OBJ, 3DS, BLEND)": ["*.fbx", "*.obj", "*.3ds", "*.blend"],
    "Autres fichiers volumineux (ZIP, EXE, RAR, DLL)": ["*.zip", "*.rar", "*.exe", "*.dll"],
    "Fichiers temporaires de sauvegarde": ["*.bak", "*.tmp"]
}

# Dictionnaries of multicontents things
{
  "translations": {
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
      "about_link": "https://example.com"
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
      "about_link": "https://example.com"
    },
    "es": {
      "title": "Generador de .gitignore para Unity",
      "select_project": "Selecciona la carpeta de tu proyecto de Unity:",
      "exclude_files": "Elige los tipos de archivos a excluir:",
      "generate_button": "Generar .gitignore y README",
      "ready": "Listo para generar.",
      "generating": "Generando... Por favor, espera.",
      "success": "Los archivos .gitignore y README.md se han generado con éxito.",
      "error": "La ruta del proyecto no es válida.",
      "about": "Nathan Chambrette - 2025",
      "about_link": "https://example.com"
    },
    "de": {
      "title": ".gitignore-Generator für Unity",
      "select_project": "Wählen Sie Ihren Unity-Projektordner aus:",
      "exclude_files": "Wählen Sie die auszuschließenden Dateitypen:",
      "generate_button": ".gitignore und README generieren",
      "ready": "Bereit zur Generierung.",
      "generating": "Wird generiert... Bitte warten.",
      "success": ".gitignore und README.md wurden erfolgreich generiert.",
      "error": "Der Projektpfad ist ungültig.",
      "about": "Nathan Chambrette - 2025",
      "about_link": "https://example.com"
    },
    "it": {
      "title": "Generatore di .gitignore per Unity",
      "select_project": "Seleziona la cartella del tuo progetto Unity:",
      "exclude_files": "Scegli i tipi di file da escludere:",
      "generate_button": "Genera .gitignore e README",
      "ready": "Pronto per generare.",
      "generating": "Generazione in corso... Attendere prego.",
      "success": "I file .gitignore e README.md sono stati generati con successo.",
      "error": "Il percorso del progetto non è valido.",
      "about": "Nathan Chambrette - 2025",
      "about_link": "https://example.com"
    },
    "pt": {
      "title": "Gerador de .gitignore para Unity",
      "select_project": "Selecione a pasta do seu projeto Unity:",
      "exclude_files": "Escolha os tipos de arquivo a serem excluídos:",
      "generate_button": "Gerar .gitignore e README",
      "ready": "Pronto para gerar.",
      "generating": "Gerando... Por favor, aguarde.",
      "success": "Os arquivos .gitignore e README.md foram gerados com sucesso.",
      "error": "O caminho do projeto é inválido.",
      "about": "Nathan Chambrette - 2025",
      "about_link": "https://example.com"
    },
    "zh": {
      "title": "Unity .gitignore 生成器",
      "select_project": "选择您的 Unity 项目文件夹：",
      "exclude_files": "选择要排除的文件类型：",
      "generate_button": "生成 .gitignore 和 README",
      "ready": "准备生成。",
      "generating": "正在生成... 请稍候。",
      "success": ".gitignore 和 README.md 文件已成功生成。",
      "error": "项目路径无效。",
      "about": "Nathan Chambrette - 2025",
      "about_link": "https://example.com"
    },
    "ja": {
      "title": "Unity .gitignore ジェネレーター",
      "select_project": "Unityプロジェクトのフォルダを選択してください:",
      "exclude_files": "除外するファイルタイプを選択してください:",
      "generate_button": ".gitignore と README を生成",
      "ready": "生成の準備ができました。",
      "generating": "生成中... お待ちください。",
      "success": ".gitignore と README.md が正常に生成されました。",
      "error": "プロジェクトのパスが無効です。",
      "about": "Nathan Chambrette - 2025",
      "about_link": "https://example.com"
    },
    "nl": {
      "title": ".gitignore-generator voor Unity",
      "select_project": "Selecteer de map van je Unity-project:",
      "exclude_files": "Kies de bestandstypen die je wilt uitsluiten:",
      "generate_button": ".gitignore en README genereren",
      "ready": "Klaar om te genereren.",
      "generating": "Bezig met genereren... Even geduld.",
      "success": ".gitignore en README.md-bestanden zijn succesvol gegenereerd.",
      "error": "Het projectpad is ongeldig.",
      "about": "Nathan Chambrette - 2025",
      "about_link": "https://example.com"
    },
    "pl": {
      "title": "Generator pliku .gitignore dla Unity",
      "select_project": "Wybierz folder projektu Unity:",
      "exclude_files": "Wybierz typy plików do wykluczenia:",
      "generate_button": "Generuj .gitignore i README",
      "ready": "Gotowe do generowania.",
      "generating": "Trwa generowanie... Proszę czekać.",
      "success": "Pliki .gitignore i README.md zostały pomyślnie wygenerowane.",
      "error": "Ścieżka projektu jest nieprawidłowa.",
      "about": "Nathan Chambrette - 2025",
      "about_link": "https://example.com"
    },
    "ru": {
      "title": "Генератор .gitignore для Unity",
      "select_project": "Выберите папку проекта Unity:",
      "exclude_files": "Выберите типы файлов для исключения:",
      "generate_button": "Сгенерировать .gitignore и README",
      "ready": "Готово к генерации.",
      "generating": "Генерация... Пожалуйста, подождите.",
      "success": "Файлы .gitignore и README.md успешно сгенерированы.",
      "error": "Неверный путь к проекту.",
      "about": "Nathan Chambrette - 2025",
      "about_link": "https://example.com"
    },
    "ar": {
      "title": "مولّد .gitignore لـ Unity",
      "select_project": "اختر مجلد مشروع Unity الخاص بك:",
      "exclude_files": "اختر أنواع الملفات التي تريد استبعادها:",
      "generate_button": "إنشاء .gitignore وREADME",
      "ready": "جاهز للإنشاء.",
      "generating": "جارٍ الإنشاء... يرجى الانتظار.",
      "success": "تم إنشاء ملفات .gitignore وREADME.md بنجاح.",
      "error": "مسار المشروع غير صالح.",
      "about": "Nathan Chambrette - 2025",
      "about_link": "https://example.com"
    }
  }
}


# Trad funcs
current_language = "fr"
def translate(key):
    return translations[current_language][key]

# Rotating lang function
def toggle_language():
    global current_language
    current_language = "en" if current_language == "fr" else "fr"
    update_ui_texts()

# UI Update textFunction
def update_ui_texts():
    root.title(translate("title"))
    title_label.config(text=translate("title"))
    path_label.config(text=translate("select_project"))
    options_label.config(text=translate("exclude_files"))
    generate_button.config(text=translate("generate_button"))
    status_label.config(text=translate("ready"))

# Fonction for "about_link" 
def open_about_link():
    webbrowser.open(translate("about_link"))

# Function for "about" screen
def show_about():
    about_window = tk.Toplevel(root)
    about_window.title("À propos")
    about_window.geometry("300x100")
    about_label = tk.Label(about_window, text=translate("about"), font=("Arial", 12))
    about_label.pack(pady=10)
    link = tk.Label(about_window, text=translate("about_link"), fg="blue", cursor="hand2")
    link.pack()
    link.bind("<Button-1>", lambda e: open_about_link())

# Function for generate .gitignore file
def generate_gitignore(project_path, selected_extensions):
    gitignore_path = os.path.join(project_path, ".gitignore")
    with open(gitignore_path, "w") as gitignore_file:
        gitignore_file.write(unity_gitignore_base)  # Write base rules
        for ext_list in selected_extensions:
            for ext in ext_list:
                gitignore_file.write(f"{ext}\n")  # Add each extension
    return gitignore_path

# Function to list packages
def list_packages(project_path):
    packages = []
    packages_path = os.path.join(project_path, "Packages")
    if os.path.exists(packages_path):
        for item in os.listdir(packages_path):
            if item.endswith(".json"):
                packages.append(item)
    return packages

# Function to list exclude files
def list_excluded_files(project_path, selected_extensions):
    excluded_files = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            for ext_list in selected_extensions:
                if any(file.endswith(ext.strip("*")) for ext in ext_list):
                    excluded_files.append(os.path.relpath(os.path.join(root, file), project_path))
    return excluded_files

# Function to generate  README
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

# Daltonian mode
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

# Function to listen directories
def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder_path)

# Create UI
root = tk.Tk()
root.title(translate("title"))
root.geometry("550x600")
root.configure(bg="#f4f4f4")

# Menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

options_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Options", menu=options_menu)
options_menu.add_command(label="Mode Daltonien", command=toggle_colorblind_mode)
options_menu.add_command(label="Changer de langue", command=toggle_language)
options_menu.add_separator()
options_menu.add_command(label="À propos", command=show_about)

# Interface content
title_label = tk.Label(root, text=translate("title"), font=("Arial", 16, "bold"), bg="#4CAF50", fg="white")
title_label.pack(pady=20)

# Projet route
path_label = tk.Label(root, text=translate("select_project"))
path_label.pack(pady=5)
path_entry = tk.Entry(root, width=40, font=("Arial", 10), relief="solid")
path_entry.pack(pady=5)

browse_button = ttk.Button(root, text="Parcourir", command=browse_folder)
browse_button.pack(pady=10)

# Frame for extensions options
options_frame = ttk.Frame(root)
options_frame.pack(pady=10)

# Label for extensions options
options_label = tk.Label(options_frame, text=translate("exclude_files"), bg="#f4f4f4")
options_label.pack()

# TODO extensions to apply
ext_vars = {}
for ext_name in media_extensions:
    var = tk.BooleanVar()
    ext_vars[ext_name] = var
    cb = ttk.Checkbutton(options_frame, text=ext_name, variable=var)
    cb.pack(anchor="w")

# Progression barr
progress_frame = ttk.Frame(root)
progress_frame.pack(pady=10)
progress_bar = ttk.Progressbar(progress_frame, length=300, mode="indeterminate")
progress_bar.pack()

# Label for generation state
status_label = tk.Label(root, text=translate("ready"), bg="#f4f4f4", font=("Arial", 10, "italic"))
status_label.pack(pady=20)

# Bouton for generate .gitignore and README file
generate_button = ttk.Button(root, text=translate("generate_button"), command=process_project)
generate_button.pack(pady=20)


root.mainloop()
