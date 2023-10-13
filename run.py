from app import create_app, db
import serverless_wsgi

app = create_app()

with app.app_context():
    db.create_all()


def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)


if __name__ == "__main__":
    app.run()
