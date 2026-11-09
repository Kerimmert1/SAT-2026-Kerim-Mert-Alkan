from app import create_app
from database import get_db


def test_login_redirects_and_dashboard_loads():
    app = create_app({"TESTING": True, "DB_PATH": ":memory:"})
    client = app.test_client()

    login_response = client.post(
        "/login",
        data={"username": "admin", "password": "admin123"},
        follow_redirects=False,
    )

    assert login_response.status_code == 302

    dashboard_response = client.get("/dashboard")
    assert dashboard_response.status_code == 200


def test_student_attendance_record_can_be_created():
    app = create_app({"TESTING": True, "DB_PATH": ":memory:"})
    client = app.test_client()

    client.post("/login", data={"username": "admin", "password": "admin123"}, follow_redirects=False)
    student_response = client.post(
        "/students/add",
        data={"name": "Ayşe Demir", "student_number": "2024001", "class_name": "Bilişim 2"},
        follow_redirects=False,
    )

    assert student_response.status_code == 302

    attendance_response = client.post(
        "/attendance/mark",
        data={"student_id": "1", "status": "Var", "date": "2026-10-05"},
        follow_redirects=False,
    )

    assert attendance_response.status_code == 302


def test_invalid_attendance_date_is_rejected_without_saving():
    app = create_app({"TESTING": True, "DB_PATH": ":memory:"})
    client = app.test_client()

    client.post("/login", data={"username": "admin", "password": "admin123"})
    response = client.post(
        "/attendance/mark",
        data={"student_id": "1", "status": "Var", "date": "2026-99-99"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Geçerli bir tarih girmeniz gerekiyor." in response.get_data(as_text=True)

    conn = get_db()
    attendance_count = conn.execute("SELECT COUNT(*) FROM attendance").fetchone()[0]
    conn.close()
    assert attendance_count == 0


def test_health_check_returns_ok():
    app = create_app({"TESTING": True, "DB_PATH": ":memory:"})
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert data["database"] == "ok"
    assert "version" in data


def test_attendance_export_returns_csv():
    app = create_app({"TESTING": True, "DB_PATH": ":memory:"})
    client = app.test_client()

    client.post("/login", data={"username": "admin", "password": "admin123"}, follow_redirects=False)
    client.post(
        "/students/add",
        data={"name": "Test Ogrenci", "student_number": "9999", "class_name": "Test Sinif"},
        follow_redirects=False,
    )
    client.post(
        "/attendance/mark",
        data={"student_id": "1", "status": "Var", "date": "2026-10-05"},
        follow_redirects=False,
    )

    response = client.get("/attendance/export?date=2026-10-05")

    assert response.status_code == 200
    assert "text/csv" in response.content_type
    content = response.get_data(as_text=True)
    assert "9999" in content
    assert "Var" in content
