# Flask Application

This is a Flask application that performs CRUD operations on a User resource using a REST API. It is built using Flask and PyMongo, and runs inside a Docker container.

## Requirements

- Docker

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/Dasari-Bhovan/flask_assignment.git
   ```


2. Build the Docker image:

   ```bash
   docker build -t flask-app .
   ```
3. Run the Docker container:

   ```bash
   docker run -p 5000:5000 flask-app
   ```

   The Flask application will be accessible at [http://localhost:5000](http://localhost:5000/).

## API Endpoints

* `GET /users` - Returns a list of all users.
* `GET /users/<user_id>` - Returns the user with the specified ID.
* `POST /users` - Creates a new user with the specified data.
* `PUT /users/<user_id>` - Updates the user with the specified ID with the new data.
* `DELETE /users/<user_id>` - Deletes the user with the specified ID.

## Customization

You can customize the Flask application by modifying the following files:

* `app.py` - Contains the Flask application code.
* `requirements.txt` - Specifies the Python dependencies required by the application.
