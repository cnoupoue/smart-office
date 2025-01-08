# Flask Authentication API (Access control)

## Concept

This project implements an authentication system to control access to the Node-RED `/ui` interface. Users are required to log in through a Flask API that validates their credentials against a MongoDB database. Only authenticated users can access the Node-RED `/ui`.

## Architecture

### Components

1. **Flask API**  
   - Provides a login page where users can authenticate.  
   - Validates user credentials against a MongoDB database.  
   - Issues a session or token (e.g., JWT) upon successful login.  

## Installation

```bash
./install.sh
```
