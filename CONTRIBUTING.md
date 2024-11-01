# Contributing to Code-Formatter-Advisor

Thank you for considering contributing to this project! Here are the guidelines to help you get started.

## ⚙️ Setup Instructions

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Elisassa/Code-Formatter-Advisor.git
    cd Code-Formatter-Advisor
    ```

2. **Create a Virtual Environment** (Optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 🛠️ Development Guidelines

- Use [Black](https://github.com/psf/black) for Python code formatting.
- Use [Flake8](https://flake8.pycqa.org/en/latest/) for linting.
- Run unit tests before submitting pull requests.

### Code Formatting with Black

- **Run Black to format the code**:
    ```bash
    black .
    ```
- Alternatively, use the provided script:
    ```bash
    ./run_formatter.sh
    ```
- Black will automatically format the code to follow consistent styling. Please run it before submitting code to ensure uniform code style.

### Linting with Flake8

- **Run Flake8 to check for issues**:
    ```bash
    flake8
    ```
- Or use the provided script:
    ```bash
    ./run_linter.sh
    ```
- Flake8 will highlight any coding style violations or potential issues. Please address all warnings and errors before submitting code.

## 🧑‍💻 Editor/IDE Integration

To improve the development experience, we recommend integrating Black and Flake8 with [Visual Studio Code (VSCode)](https://code.visualstudio.com/).

### VSCode Setup

1. **Install Extensions**:
    - Open VSCode and install the **Python** extension (provided by Microsoft), which supports Black and Flake8.
    - Optionally, install the **Black Formatter** extension if additional configuration is needed.

2. **Configure VSCode**:
    - This project includes a `.vscode/settings.json` file with the following settings:
      ```json
      {
          "python.formatting.provider": "black",
          "python.formatting.blackArgs": [
              "--line-length", "88"
          ],
          "editor.formatOnSave": true,
          "python.linting.enabled": true,
          "python.linting.flake8Enabled": true,
          "python.linting.flake8Args": [
              "--max-line-length=88"
          ]
      }
      ```
    - These settings enable Black formatting on save and Flake8 linting to provide real-time feedback on code quality.

3. **Manual Configuration** (if needed):
    - If the automatic configuration doesn’t work, add the above JSON settings manually to `.vscode/settings.json`.

## 📥 How to Contribute

1. Fork the repository.
2. Create a new feature branch:
    ```bash
    git checkout -b feature/your-feature-name
    ```
3. Commit your changes:
    ```bash
    git commit -m 'Add some feature'
    ```
4. Push to the branch:
    ```bash
    git push origin feature/your-feature-name
    ```
5. Open a pull request.