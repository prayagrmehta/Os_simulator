# OS Simulator

## Overview
The **OS Simulator** is a web-based application built using **Python Flask** that simulates various operating system scheduling and memory management algorithms. This project provides an interactive way to understand and visualize fundamental OS concepts such as **CPU scheduling, disk scheduling, and concurrency control**.

## Features
### 1. **CPU Scheduling Algorithms**
   - **Priority Scheduling**: Implements priority-based CPU scheduling where processes with higher priority execute first.

### 2. **Concurrency Control**
   - **Reader-Writer Problem**: Simulates the classic **Readers-Writers** synchronization problem, demonstrating shared resource access control.

### 3. **Memory Management**
   - **Least Recently Used (LRU) Page Replacement**: Implements LRU page replacement algorithm for memory management.

### 4. **Disk Scheduling Algorithms**
   - **First-Come, First-Served (FCFS) Disk Scheduling**: Implements FCFS disk scheduling algorithm.

## Tech Stack
- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript

## Installation & Setup
1. **Clone the repository**
   ```sh
   git clone https://github.com/prayagrmehta/Os_simulator.git
   cd Os_simulator
   ```
2. **Create a virtual environment (optional but recommended)**
   ```sh
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate  # For Windows
   ```
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Run the Flask server**
   ```sh
   python os_app.py
   ```
5. **Access the web application**
   Open your browser and go to:  
   👉 `http://127.0.0.1:5000/`

## Usage
- Navigate to the web interface to choose between different OS algorithms.
- Input required parameters for the selected algorithm.
- View real-time scheduling simulations and results.

## Contributing
Feel free to submit issues and pull requests to improve the project. If you'd like to contribute:
1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to your branch (`git push origin feature-branch`)
5. Open a pull request

## Contact
For any queries, feel free to reach out:
- **GitHub**: [prayagrmehta](https://github.com/prayagrmehta)
- **Email**: prayagrmehta.1011@gmail.com (update with your actual email)

---
Enjoy exploring Operating System concepts with this simulator! 🚀

