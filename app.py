from flask import Flask, render_template, request

app = Flask(__name__)



# Index page
@app.route('/', methods=['GET', 'POST'])
def index():
    return "Hello World!"

    
if __name__ == '__main__':
    app.run(port=5000, debug=True)
