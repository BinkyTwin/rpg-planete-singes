#!/usr/bin/env python3
"""
Utilitaires pour l'installation automatique des dépendances
"""

import os
import sys
import venv
import subprocess
import platform
from pathlib import Path

def get_python_executable():
    """Retourne le chemin de l'exécutable Python en fonction du système d'exploitation."""
    if platform.system() == "Windows":
        return os.path.join("venv", "Scripts", "python.exe")
    return os.path.join("venv", "bin", "python")

def get_pip_executable():
    """Retourne le chemin de l'exécutable pip en fonction du système d'exploitation."""
    if platform.system() == "Windows":
        return os.path.join("venv", "Scripts", "pip.exe")
    return os.path.join("venv", "bin", "pip")

def create_venv():
    """Crée un environnement virtuel s'il n'existe pas déjà."""
    if not os.path.exists("venv"):
        print("Création de l'environnement virtuel...")
        try:
            venv.create("venv", with_pip=True)
            print("[OK] Environnement virtuel créé avec succès")
            return True
        except Exception as e:
            print(f"[ERREUR] Erreur lors de la création de l'environnement virtuel : {e}")
            return False
    return True

def install_dependencies():
    """Installe les dépendances depuis requirements.txt dans l'environnement virtuel."""
    pip_path = get_pip_executable()
    requirements_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")
    
    if not os.path.exists(requirements_path):
        print("[ERREUR] Le fichier requirements.txt est introuvable")
        return False
    
    print("Installation des dépendances...")
    try:
        subprocess.check_call([pip_path, "install", "-r", requirements_path])
        print("[OK] Dépendances installées avec succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERREUR] Erreur lors de l'installation des dépendances : {e}")
        return False

def setup_environment():
    """Configure l'environnement de développement."""
    if not create_venv():
        return False
    
    if not install_dependencies():
        return False
    
    return True
