from django.apps import AppConfig
import sqlite3
import os
import threading

class ProducaoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'producao'

    def ready(self):
        # --- Criação das tabelas ---
        from django.conf import settings
        db_path = settings.DATABASES['default']['NAME']

        if os.path.exists(db_path):
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                # Tabela paradas_linha
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS paradas_linha (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome_linha TEXT NOT NULL,
                        inicio_parada TEXT NOT NULL,
                        fim_parada TEXT
                    );
                """)

                # Tabela motivos_paradas
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS motivos_paradas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome_linha TEXT NOT NULL,
                        inicio_parada TEXT NOT NULL,
                        fim_parada TEXT,
                        motivo TEXT NOT NULL
                    );
                """)

                conn.commit()
                print("✅ Tabelas 'paradas_linha' e 'motivos_paradas' verificadas/criadas com sucesso.")
            except sqlite3.Error as e:
                print(f"❌ Erro ao acessar o banco de dados: {e}")
            finally:
                conn.close()

        # --- Inicializa o monitor do PLC em thread ---
        try:
            from .plc_monitor import main  # plc_monitor.py deve estar dentro do app
            t = threading.Thread(target=main, daemon=True)
            t.start()
            print("✅ Thread do PLC Monitor iniciada.")
        except ImportError as e:
            print(f"❌ Não foi possível importar plc_monitor.py: {e}")
