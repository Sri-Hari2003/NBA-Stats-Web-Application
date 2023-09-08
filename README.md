# NBA Stats Web Application

This is a web application built using Flask that allows users to select NBA teams, view game statistics, and visualize the Plus-Minus stats between two teams.

## Table of Contents

- [Demo](#demo)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Contributing](#contributing)


## Demo

Provide a link to a live demo of your application if available.

## Features

- Select NBA teams and view game statistics.
- Visualize Plus-Minus stats between two teams using interactive graphs.
- Easy navigation with a user-friendly web interface.

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/Sri-Hari2003/nba-stats-app.git
   ```

2. Navigate to the project directory:

   ```bash
   cd nba-stats-app
   ```

3. Create a virtual environment (recommended):

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   - **On Windows:**

     ```bash
     venv\Scripts\activate
     ```

   - **On macOS and Linux:**

     ```bash
     source venv/bin/activate
     ```

5. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Start the Flask application:

   ```bash
   python app.py
   ```

7. Open your web browser and visit [http://localhost:5000/](http://localhost:5000/) to use the application.

## Usage

1. Launch the application by following the installation steps above.

2. Select the NBA teams you want to compare.

3. Choose the type of statistics you want to view (e.g., "Get Stats" or "Get Stats graph").

4. Explore game statistics and visualize Plus-Minus stats using the provided features.

## Dependencies

- Flask
- pandas
- numpy
- matplotlib
- nba_api

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.

2. Create a new branch for your feature or bug fix.

3. Make your changes and test thoroughly.

4. Submit a pull request with a detailed description of your changes.
