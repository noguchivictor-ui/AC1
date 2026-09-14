

import sqlite3
import os


def conectar_banco():
    
    os.makedirs('dados', exist_ok=True)
    conn = sqlite3.connect('dados/banco.db')
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')

    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS animais (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            nome            TEXT    NOT NULL,
            especie         TEXT    NOT NULL,
            raca            TEXT,
            data_nascimento TEXT    NOT NULL,
            tutor_nome      TEXT    NOT NULL,
            UNIQUE (nome, tutor_nome)
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS atendimentos (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            animal_id   INTEGER NOT NULL,
            descricao   TEXT    NOT NULL,
            data        TEXT    NOT NULL,
            valor       REAL    NOT NULL,
            veterinario TEXT    NOT NULL,
            FOREIGN KEY (animal_id) REFERENCES animais (id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    return conn


# --------------------------------------------------------------- CONSULTAS

def listar_animais(conn, termo=None):
    """Lista animais; se 'termo' for passado, filtra por nome ou tutor."""
    if termo:
        return conn.execute(
            'SELECT * FROM animais'
            ' WHERE LOWER(nome) LIKE ? OR LOWER(tutor_nome) LIKE ?'
            ' ORDER BY nome',
            (f'%{termo}%', f'%{termo}%')
        ).fetchall()
    return conn.execute('SELECT * FROM animais ORDER BY nome').fetchall()


def buscar_animal(conn, id_animal):
    return conn.execute('SELECT * FROM animais WHERE id = ?',
                        (id_animal,)).fetchone()


def animal_duplicado(conn, nome, tutor_nome, id_atual=None):

    if id_atual is None:
        existente = conn.execute(
            'SELECT id FROM animais WHERE LOWER(nome) = ? AND LOWER(tutor_nome) = ?',
            (nome.lower(), tutor_nome.lower())
        ).fetchone()
    else:
        existente = conn.execute(
            'SELECT id FROM animais'
            ' WHERE LOWER(nome) = ? AND LOWER(tutor_nome) = ? AND id <> ?',
            (nome.lower(), tutor_nome.lower(), id_atual)
        ).fetchone()
    return existente is not None


def listar_atendimentos_do_animal(conn, id_animal):
    return conn.execute(
        'SELECT * FROM atendimentos WHERE animal_id = ? ORDER BY data DESC',
        (id_animal,)
    ).fetchall()
