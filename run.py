print("RUN.PY IS STARTING")
from app import create_app
from app.routes.expenses import expenses_bp

app = create_app()
app.register_blueprint(expenses_bp)

if __name__ == "__main__":
    app.run(debug=True)