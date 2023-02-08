from app import create_app

# With prefix /lettres (also update in __init__.py & in VUE_APP var_env):
flask_app = create_app(config_name="dev", with_hardcoded_prefix=True)

# Without prefix /lettres (also update in __init__.py & in VUE_APP var_env):
# flask_app = create_app(config_name="dev")

if __name__ == "__main__":
    flask_app.run(debug=True, port=5004, host='0.0.0.0')

