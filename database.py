import os
import sqlite3

from werkzeug.security import generate_password_hash


DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), 'attendance_system.db')


def _resolve_db_path():
    configured = os.environ.get('ATTENDANCE_DB_PATH')
    if configured in (None, ''):
        return DEFAULT_DB_PATH
    return configured


def get_db():
    db_path = _resolve_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            student_number TEXT UNIQUE NOT NULL,
            class_name TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('Var', 'Yok', 'Geç Kaldı')),
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(student_id, date),
            FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()

    admin_exists = conn.execute('SELECT 1 FROM admins LIMIT 1').fetchone()
    if not admin_exists:
        conn.execute(
            'INSERT INTO admins (username, password_hash) VALUES (?, ?)',
            ('admin', generate_password_hash('admin123')),
        )

    if os.environ.get('ATTENDANCE_SEED', '1') != '0':
        sample_student_exists = conn.execute('SELECT 1 FROM students LIMIT 1').fetchone()
        if not sample_student_exists:
            sample_students = [
                ('Ayşe Demir', '2024001', 'Bilişim 2'),
                ('Mehmet Yılmaz', '2024002', 'Bilişim 2'),
                ('Elif Kaya', '2024003', 'Bilişim 1'),
            ]
            conn.executemany(
                'INSERT INTO students (name, student_number, class_name) VALUES (?, ?, ?)',
                sample_students,
            )

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
    print('Öğrenci devamsızlık veritabanı hazır.')
