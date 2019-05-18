from app import db


def create_all():
    db.create_all()


if __name__ == '__main__':
    create_all()
