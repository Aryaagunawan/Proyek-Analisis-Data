## Project Deployment Guide

This guide provides instructions on how to manage and work with the `Proyek-Analisis-Data` project.

## Installation

1. Clone the repository:
    ```sh
   https://github.com/Aryaagunawan/Proyek-Analisis-Data.git
    ```
2. Navigate to the project directory:
    ```sh
    cd Proyek-Analisis-Data
    ```
3. Create a virtual environment:
    ```sh
    python -m venv venv
    ```
4. Activate the virtual environment:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```
5. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Deployment

To deploy this project using Streamlit, follow these steps:

1. Run the application:
    ```sh
    streamlit run dashboard/dashboard.py
    ```
2. By default, you can access your Streamlit project at
   `http://localhost:8501`
