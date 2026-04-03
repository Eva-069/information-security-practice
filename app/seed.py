from app.database import SessionLocal
from app.models import Role, Permission, User, Group, Subject
from app.security import hash_password


def seed():
    db = SessionLocal()
    try:
        if db.query(Role).first():
            print("Database already seeded.")
            return

        admin = Role(name="admin", description="Administrator")
        teacher = Role(name="teacher", description="Teacher")
        student = Role(name="student", description="Student")
        db.add_all([admin, teacher, student])
        db.flush()

        perms = [
            Permission(name="read_grades", description="View grades"),
            Permission(name="edit_grades", description="Edit grades"),
            Permission(name="read_schedule", description="View schedule"),
            Permission(name="manage_users", description="Manage users"),
            Permission(name="manage_groups", description="Manage groups"),
            Permission(name="manage_subjects", description="Manage subjects"),
            Permission(name="view_reports", description="View reports"),
        ]
        db.add_all(perms)
        db.flush()

        admin.permissions.extend(perms)
        teacher.permissions.extend([p for p in perms if p.name in ("read_grades", "edit_grades", "read_schedule", "view_reports")])
        student.permissions.extend([p for p in perms if p.name in ("read_grades", "read_schedule")])

        group = Group(name="KN-31", department="Computer Science", year=3)
        db.add(group)
        db.flush()

        subject = Subject(name="Information Security", credits=4.0, semester=5)
        db.add(subject)

        admin_user = User(username="admin", email="admin@university.edu", full_name="System Administrator", password_hash=hash_password("Admin123!@#"), is_active=True)
        admin_user.roles.append(admin)

        teacher_user = User(username="teacher01", email="teacher@university.edu", full_name="Petrov Ivan", password_hash=hash_password("Teacher123!"))
        teacher_user.roles.append(teacher)

        student_user = User(username="student01", email="student@university.edu", full_name="Petrenko Maria", password_hash=hash_password("Student123!"), group_id=group.id)
        student_user.roles.append(student)

        db.add_all([admin_user, teacher_user, student_user])
        db.commit()
        print("Seed completed successfully!")
        print(f"  Roles: {db.query(Role).count()}")
        print(f"  Permissions: {db.query(Permission).count()}")
        print(f"  Users: {db.query(User).count()}")

    except Exception as e:
        db.rollback()
        print(f"Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()