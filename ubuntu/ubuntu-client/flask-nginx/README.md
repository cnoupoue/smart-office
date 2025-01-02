# Flask Authentication API (Access control)

## Concept

This project implements an authentication system to control access to the Node-RED `/ui` interface. Users are required to log in through a Flask API that validates their credentials against a MongoDB database. Only authenticated users can access the Node-RED `/ui`.

## Architecture

### Components

1. **Flask API**  
   - Provides a login page where users can authenticate.  
   - Validates user credentials against a MongoDB database.  
   - Issues a session or token (e.g., JWT) upon successful login.  
   - Redirects authenticated users to the Node-RED `/ui`.

2. **Nginx Reverse Proxy**  
   - Acts as a gatekeeper between users, Flask, and Node-RED.  
   - Routes all requests to `/ui` through the Flask API for authentication.  
   - Forwards valid requests to the Node-RED `/ui` interface.

3. **Node-RED**  
   - Hosts the `/ui` dashboard.  
   - Secured by the Nginx proxy to ensure only authenticated users can access it.

### Workflow

1. The user accesses the login page hosted by Flask.
2. Flask validates the user's credentials using MongoDB.
3. If the credentials are valid:
   - Flask issues a session or token.
   - Flask redirects the user to the `/ui` interface.
4. Nginx checks if the session/token is valid before forwarding the request to Node-RED.
5. If the session/token is invalid, the user is denied access and redirected to the login page.

## Installation

### Flask

`pip install flask flask-cors flask-jwt-extended`

