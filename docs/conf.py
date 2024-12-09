import os
import sys

# Dodanie ścieżki do katalogu AvanTIc
sys.path.insert(0, "/home/tkielak/AvanTIc")  # Zmień na rzeczywistą ścieżkę, jeśli jest inna

# Ustawienie zmiennej środowiskowej Django
os.environ["DJANGO_SETTINGS_MODULE"] = "test1.settings"

# Inicjalizacja Django
import django
django.setup()

# Konfiguracja logowania
import logging
logging.basicConfig(level=logging.WARNING)

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Aprobo"
copyright = "2024, Tadeusz Kielak"
author = "Tadeusz Kielak"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.imgconverter",
    "sphinx.ext.autosummary",
]

templates_path = ["_templates"]
exclude_patterns = ["**/migrations/**", "_build", "Thumbs.db", ".DS_Store"]

language = "pl"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]

autosummary_generate = True  # Włącza generowanie autosummary

# -- Options for LaTeX output ------------------------------------------------
latex_elements = {
    "papersize": "a4paper",
    "pointsize": "10pt",
    "preamble": r"""
    \usepackage{amsmath}
    \usepackage{graphicx}
    \usepackage{hyperref}
    """,
    "figure_align": "htbp",
}

latex_documents = [
    ("index", "MyProject.tex", "My Project Documentation", "Author Name", "manual"),
]

# -- Options for EPUB output -------------------------------------------------
epub_show_urls = "footnote"

# Motyw dokumentacji
html_theme = "alabaster"

# Własne pliki CSS
html_css_files = ["custom.css"]

import socket

# Pobranie nazwy hosta
hostname = socket.gethostname()

# Konfiguracja motywu Alabaster
html_theme_options = {
    "fixed_sidebar": True,  # Stałe menu boczne
 #   "description": "Dokumentacja systemu AvanTIc",
    "github_banner": False,
    "page_width": "1500px",
    "sidebar_width": "300px",
    "font_family": "'Times New Roman', Times, serif, sans-serif",
    "extra_nav_links": {
        # Dynamiczne ustawienie adresu URL
        "Przejdź do projektu": f"https://{hostname}/",  
    },
}


# Funkcja generująca nginx_config.rst
def generate_nginx_includes(root_dir, output_rst):
    """
    Generuje wpisy literalinclude dla wszystkich plików w katalogu root_dir
    i zapisuje je w pliku output_rst.
    """
    # Obliczamy katalog bazowy dla ścieżek relatywnych
    base_dir = os.path.dirname(output_rst)

    with open(output_rst, 'w') as rst_file:
        rst_file.write("Struktura katalogów i zawartość plików:\n\n")
        
        # Sortowanie katalogów i plików w os.walk
        for subdir, dirs, files in os.walk(root_dir):
            # Sortowanie katalogów (opcjonalne, nie wpływa na pliki)
            dirs.sort()
            # Sortowanie plików w bieżącym katalogu
            files.sort()
            
            for file in files:
                file_path = os.path.join(subdir, file)
                # Generujemy ścieżkę relatywną względem pliku wynikowego
                relative_path = os.path.relpath(file_path, start=base_dir)
                rst_file.write(f"### {file}\n\n")
                rst_file.write(f".. literalinclude:: {relative_path}\n")
                rst_file.write("   :language: nginx\n")
                rst_file.write(f"   :caption: {file}\n\n")


# Wywołanie funkcji
generate_nginx_includes(
    root_dir=os.path.abspath(os.path.join(os.path.dirname(__file__), "../configs/prod/nginx/")),
    output_rst=os.path.abspath(os.path.join(os.path.dirname(__file__), "./enviroment/nginx_config.rst"))
)
