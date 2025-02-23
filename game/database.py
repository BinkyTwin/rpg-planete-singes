import sqlite3
import os
from typing import List, Dict, Optional, Tuple
from .items import Item, ItemType

class GameDatabase:
    def __init__(self, db_path: str = "game.db"):
        """Initialise la connexion à la base de données"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Établit la connexion à la base de données"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            print(f"Connexion établie avec {self.db_path}")
        except sqlite3.Error as e:
            print(f"Erreur lors de la connexion à la base de données : {e}")

    def create_tables(self):
        """Crée les tables nécessaires si elles n'existent pas"""
        try:
            # Table des joueurs
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    race TEXT NOT NULL,
                    faction TEXT NOT NULL,
                    hp INTEGER NOT NULL,
                    x INTEGER NOT NULL,
                    y INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Table de l'inventaire
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_id INTEGER,
                    item_name TEXT NOT NULL,
                    item_type TEXT NOT NULL,
                    item_value INTEGER,
                    equipped BOOLEAN DEFAULT 0,
                    FOREIGN KEY (player_id) REFERENCES players(id)
                )
            ''')

            # Table des durées de vie
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS lifespan (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_id INTEGER,
                    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    end_time TIMESTAMP,
                    duration_seconds INTEGER,
                    FOREIGN KEY (player_id) REFERENCES players(id)
                )
            ''')

            self.conn.commit()
            print("Tables créées avec succès")
        except sqlite3.Error as e:
            print(f"Erreur lors de la création des tables : {e}")

    def save_player(self, player) -> int:
        """Sauvegarde les données du joueur et retourne son ID"""
        try:
            self.cursor.execute('''
                INSERT INTO players (name, race, faction, hp, x, y)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (player.name, player.race, player.faction.value, player.hp, player.x, player.y))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erreur lors de la sauvegarde du joueur : {e}")
            return None

    def save_inventory(self, player_id: int, inventory):
        """Sauvegarde l'inventaire du joueur"""
        try:
            # Supprime l'ancien inventaire
            self.cursor.execute('DELETE FROM inventory WHERE player_id = ?', (player_id,))
            
            # Sauvegarde les nouveaux items
            for item in inventory.get_items():
                equipped = item == inventory.get_equipped_item()
                self.cursor.execute('''
                    INSERT INTO inventory (player_id, item_name, item_type, item_value, equipped)
                    VALUES (?, ?, ?, ?, ?)
                ''', (player_id, item.name, item.item_type.value, item.value, equipped))
            
            self.conn.commit()
            print(f"Inventaire sauvegardé pour le joueur {player_id}")
        except sqlite3.Error as e:
            print(f"Erreur lors de la sauvegarde de l'inventaire : {e}")

    def save_lifespan(self, player_id: int, duration_seconds: int):
        """Enregistre la durée de vie d'un joueur"""
        try:
            self.cursor.execute('''
                INSERT INTO lifespan (player_id, duration_seconds, end_time)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (player_id, duration_seconds))
            self.conn.commit()
            print(f"Durée de vie enregistrée pour le joueur {player_id}")
        except sqlite3.Error as e:
            print(f"Erreur lors de l'enregistrement de la durée de vie : {e}")

    def load_player(self, player_name: str) -> Optional[Dict]:
        """Charge les données d'un joueur par son nom"""
        try:
            self.cursor.execute('''
                SELECT id, name, race, faction, hp, x, y
                FROM players
                WHERE name = ?
                ORDER BY created_at DESC
                LIMIT 1
            ''', (player_name,))
            result = self.cursor.fetchone()
            
            if result:
                return {
                    'id': result[0],
                    'name': result[1],
                    'race': result[2],
                    'faction': result[3],
                    'hp': result[4],
                    'x': result[5],
                    'y': result[6]
                }
            return None
        except sqlite3.Error as e:
            print(f"Erreur lors du chargement du joueur : {e}")
            return None

    def load_inventory(self, player_id: int) -> List[Dict]:
        """Charge l'inventaire d'un joueur"""
        try:
            self.cursor.execute('''
                SELECT item_name, item_type, item_value, equipped
                FROM inventory
                WHERE player_id = ?
            ''', (player_id,))
            
            items = []
            for row in self.cursor.fetchall():
                items.append({
                    'name': row[0],
                    'type': row[1],
                    'value': row[2],
                    'equipped': bool(row[3])
                })
            return items
        except sqlite3.Error as e:
            print(f"Erreur lors du chargement de l'inventaire : {e}")
            return []

    def get_player_lifespan_stats(self, player_id: int) -> Dict:
        """Récupère les statistiques de durée de vie d'un joueur"""
        try:
            self.cursor.execute('''
                SELECT 
                    COUNT(*) as games_played,
                    AVG(duration_seconds) as avg_duration,
                    MAX(duration_seconds) as max_duration,
                    MIN(duration_seconds) as min_duration
                FROM lifespan
                WHERE player_id = ?
            ''', (player_id,))
            
            result = self.cursor.fetchone()
            return {
                'games_played': result[0],
                'avg_duration': result[1],
                'max_duration': result[2],
                'min_duration': result[3]
            }
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des statistiques : {e}")
            return {
                'games_played': 0,
                'avg_duration': 0,
                'max_duration': 0,
                'min_duration': 0
            }

    def close(self):
        """Ferme la connexion à la base de données"""
        if self.conn:
            self.conn.close()
            print("Connexion à la base de données fermée") 