from app import create_app


if __name__ == "__main__":
    flask_app = create_app(with_hardcoded_prefix=True,)
    flask_app.run(debug=True, port=5004, host='0.0.0.0')
else:
    flask_app = create_app()

