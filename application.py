from ApplicationFactory import create_app

# Create the Flask application using the factory function
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
