# Workforce Tracking System

This project is a comprehensive workforce tracking solution consisting of two main components: a background tracking agent (**SLT-Agent**) and a valid visualization dashboard (**Workforce Dashboard**).

## 📂 Project Structure

```
hubstaff/
├── SLT-Agent/              # Background tracking agent (Python)
└── workforce-dashboard/    # Data visualization dashboard
    ├── backend/            # FastAPI backend
    └── frontend/           # React frontend
```

## 1. SLT-Agent (Background Tracker)

The **SLT-Agent** is a desktop application designed to run in the background. It monitors user activity, captures screenshots, and tracks time efficiency.

### Key Features
*   **One-time Sign-in**: Requires user authentication only on the first run.
*   **Auto-start**: Automatically registers itself to run on system startup.
*   **Background Operation**: Runs silently in the background after initialization.
*   **Data Collection**: Captures screenshots, activity levels, and logs them locally.

### 🚀 How to Run

1.  Navigate to the directory:
    ```bash
    cd SLT-Agent
    ```
2.  Install dependencies:
    ```bash
    pip install PySide6 pynput requests Pillow mss
    ```
3.  Run the agent:
    ```bash
    python main.py
    ```
    *   **First Run**: A login window will appear. Enter your credentials to register the device.
    *   **Subsequent Runs**: The agent will start directly in the background.

---

## 2. Workforce Dashboard

The **Workforce Dashboard** provides a user-friendly interface to view and manage the data collected by the SLT-Agent. It is built with a **FastAPI** backend and a **React** frontend.

### Key Features
*   **Performance Metrics**: View providing time efficiency and activity stats.
*   **Screenshot Gallery**: Browse automatically captured screenshots.
*   **Employee Management**: Monitor performance for different users.

### 🚀 How to Run

The dashboard requires both the backend and frontend to be running simultaneously.

#### Step 1: Start the Backend

1.  Navigate to the backend directory:
    ```bash
    cd workforce-dashboard/backend
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configuration**:
    *   Open `main.py` and ensure the `STORAGE_PATH` points to your `SLT-Agent/storage` directory.
    *   *Example:* `STORAGE_PATH = Path("../../SLT-Agent/storage")`
4.  Start the server:
    ```bash
    python main.py
    ```
    *   The backend will run at `http://localhost:8000`.

#### Step 2: Start the Frontend

1.  Open a new terminal and navigate to the frontend directory:
    ```bash
    cd workforce-dashboard/frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm run dev
    ```
    *   The dashboard will be accessible at `http://localhost:3000`.

## 🔄 Workflow

1.  **Run SLT-Agent**: Ensure the agent is running on the target machine to collect data.
2.  **Start Dashboard**: Launch the backend and frontend to visualize the collected data.
3.  **View Data**: Open `http://localhost:3000` in your browser to see real-time updates of employee performance and screenshots.

## 🛠️ Troubleshooting

*   **No Data in Dashboard**:
    *   Verify `SLT-Agent` is running.
    *   Check `STORAGE_PATH` in `workforce-dashboard/backend/main.py`.
*   **Agent Not Starting**:
    *   Check `debug_log.txt` in the `SLT-Agent` directory for errors.
