from app import create_app


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
