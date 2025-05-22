from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    secret = os.getenv('APP_SECRET', 'No secret found')
    return f"👋 Hello from Flask! 🔐 Secret: {secret}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

---
