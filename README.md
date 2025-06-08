# Tic Tac Toe Web Game

This is a simple Tic Tac Toe game implemented with Python (Flask) for the backend and HTML, CSS, and JavaScript for the frontend.

## Setup and Run

1.  **Clone the repository (or download the files).**

2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Flask application:**
    ```bash
    python app.py
    ```

5.  Open your web browser and go to `http://127.0.0.1:5000/` to play the game.

## Project Structure

-   `app.py`: The main Flask application with game logic and API endpoints.
-   `requirements.txt`: Python dependencies.
-   `templates/`: Contains HTML files.
    -   `index.html`: The main page for the game.
-   `static/`: Contains static assets.
    -   `style.css`: CSS for styling the game.
    -   `script.js`: JavaScript for frontend logic and interactivity.
-   `README.md`: This file. 