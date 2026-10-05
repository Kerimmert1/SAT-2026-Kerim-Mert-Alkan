import os
from datetime import date
from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from database import get_db, init_db


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'ogrenci-devamsizlik-sistemi-key-2026'),
        TESTING=False,
    )

    if test_config:
        app.config.update(test_config)

    if app.config.get('DB_PATH'):
        configured = str(app.config['DB_PATH'])
        if configured == ':memory:':
            import tempfile
            import uuid
            configured = os.path.join(tempfile.gettempdir(), f'satproje_attendance_{uuid.uuid4().hex}.db')
        os.environ['ATTENDANCE_DB_PATH'] = configured

    if app.config.get('TESTING'):
        os.environ['ATTENDANCE_SEED'] = '0'
    else:
        os.environ.pop('ATTENDANCE_SEED', None)

    init_db()

    def login_required(view_func):
        @wraps(view_func)
        def wrapped(*args, **kwargs):
            if not session.get('admin_logged_in'):
                flash('Önce giriş yapmanız gerekiyor.', 'warning')
                return redirect(url_for('login'))
            return view_func(*args, **kwargs)

        return wrapped

    @app.route('/')
    def index():
        if session.get('admin_logged_in'):
            return redirect(url_for('dashboard'))
        return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if session.get('admin_logged_in'):
            return redirect(url_for('dashboard'))

        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')

            if not username or not password:
                flash('Kullanıcı adı ve şifre zorunludur.', 'warning')
                return render_template('login.html')

            conn = get_db()
            admin = conn.execute('SELECT * FROM admins WHERE username = ?', (username,)).fetchone()
            conn.close()

            if admin and check_password_hash(admin['password_hash'], password):
                session.clear()
                session['admin_logged_in'] = True
                session['username'] = admin['username']
                flash('Giriş başarılı.', 'success')
                return redirect(url_for('dashboard'))

            flash('Kullanıcı adı veya şifre hatalı.', 'danger')

        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.clear()
        flash('Çıkış yaptınız.', 'info')
        return redirect(url_for('login'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        today = date.today().isoformat()
        conn = get_db()

        total_students = conn.execute('SELECT COUNT(*) FROM students WHERE is_active = 1').fetchone()[0]
        total_present = conn.execute('SELECT COUNT(*) FROM attendance WHERE date = ? AND status = ?', (today, 'Var')).fetchone()[0]
        total_absent = conn.execute('SELECT COUNT(*) FROM attendance WHERE date = ? AND status = ?', (today, 'Yok')).fetchone()[0]
        total_late = conn.execute('SELECT COUNT(*) FROM attendance WHERE date = ? AND status = ?', (today, 'Geç Kaldı')).fetchone()[0]

        recent = conn.execute('''
            SELECT a.*, s.name, s.student_number, s.class_name
            FROM attendance a
            JOIN students s ON s.id = a.student_id
            ORDER BY a.date DESC, a.created_at DESC
            LIMIT 10
        ''').fetchall()
        conn.close()

        return render_template(
            'dashboard.html',
            total_students=total_students,
            total_present=total_present,
            total_absent=total_absent,
            total_late=total_late,
            recent=recent,
            today=today,
        )

    @app.route('/students')
    @login_required
    def students():
        conn = get_db()
        rows = conn.execute('SELECT * FROM students WHERE is_active = 1 ORDER BY name ASC').fetchall()
        conn.close()
        return render_template('students.html', students=rows)

    @app.route('/students/add', methods=['POST'])
    @login_required
    def add_student():
        name = request.form.get('name', '').strip()
        student_number = request.form.get('student_number', '').strip()
        class_name = request.form.get('class_name', '').strip()

        if not name or not student_number or not class_name:
            flash('Tüm alanlar zorunludur.', 'warning')
            return redirect(url_for('students'))

        conn = get_db()
        existing = conn.execute('SELECT id FROM students WHERE student_number = ?', (student_number,)).fetchone()
        if existing:
            conn.close()
            flash('Bu öğrenci numarası daha önce kaydedilmiş.', 'danger')
            return redirect(url_for('students'))

        conn.execute(
            'INSERT INTO students (name, student_number, class_name) VALUES (?, ?, ?)',
            (name, student_number, class_name),
        )
        conn.commit()
        conn.close()
        flash('Öğrenci başarıyla eklendi.', 'success')
        return redirect(url_for('students'))

    @app.route('/attendance')
    @login_required
    def attendance_records():
        selected_date = request.args.get('date') or date.today().isoformat()
        conn = get_db()
        rows = conn.execute('''
            SELECT a.*, s.name, s.student_number, s.class_name
            FROM attendance a
            JOIN students s ON s.id = a.student_id
            WHERE a.date = ?
            ORDER BY s.name ASC
        ''', (selected_date,)).fetchall()
        students = conn.execute('SELECT id, name, student_number, class_name FROM students WHERE is_active = 1 ORDER BY name ASC').fetchall()
        conn.close()
        return render_template('attendance.html', records=rows, students=students, selected_date=selected_date)

    @app.route('/attendance/mark', methods=['POST'])
    @login_required
    def mark_attendance():
        student_id = request.form.get('student_id')
        status = request.form.get('status', 'Var')
        date_value = request.form.get('date') or date.today().isoformat()
        note = request.form.get('note', '').strip()

        if not student_id or status not in ('Var', 'Yok', 'Geç Kaldı'):
            flash('Öğrenci ve durum seçimi zorunludur.', 'warning')
            return redirect(url_for('attendance_records', date=date_value))

        conn = get_db()
        existing = conn.execute(
            'SELECT id FROM attendance WHERE student_id = ? AND date = ?',
            (student_id, date_value),
        ).fetchone()

        if existing:
            conn.execute(
                'UPDATE attendance SET status = ?, note = ? WHERE id = ?',
                (status, note, existing['id']),
            )
        else:
            conn.execute(
                'INSERT INTO attendance (student_id, date, status, note) VALUES (?, ?, ?, ?)',
                (student_id, date_value, status, note),
            )

        conn.commit()
        conn.close()

        flash('Yoklama kaydı başarıyla güncellendi.', 'success')
        return redirect(url_for('attendance_records', date=date_value))

    @app.route('/health')
    def health_check():
        return {'status': 'ok'}

    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
