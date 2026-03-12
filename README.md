# Math Pro Marathon 🧠

An interactive math quiz application designed for kids to practice and master arithmetic skills through engaging problem-solving challenges.

## Overview

**Math Pro Marathon** is a Streamlit-based web application that helps children improve their mathematical abilities by presenting randomized math problems with immediate feedback. The app supports multiple operation types and difficulty levels, making it suitable for learners at different proficiency levels.

## Features

✨ **Multiple Math Operations**
- Addition ➕
- Subtraction ➖
- Multiplication ✕
- Division ➗

🎯 **Customizable Difficulty Levels**
- Adjustable min/max bounds for questions
- No-regrouping mode for simplified arithmetic
- Selectable number of questions per session

⏱️ **Performance Tracking**
- Timer for each question
- Session statistics (correct/incorrect answers)
- Results saved to JSON files
- Overall accuracy percentage

📊 **User Management**
- Multiple user profiles
- Individual result tracking
- Progress history

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`:
  - Streamlit
  - Pandas
  - Other utilities

## Installation

### Method 1: Automatic Setup (Windows)
Run the provided batch file:
```bash
setup_and_run.bat
```

### Method 2: Manual Setup

1. Clone the repository:
```bash
git clone https://github.com/adnan-ttj-1987/Math-Quiz-for-kids.git
cd Math-Quiz-for-kids
```

2. Create a virtual environment:
```bash
python -m venv math_marathon_env
```

3. Activate the virtual environment:
- **Windows:**
```bash
math_marathon_env\Scripts\activate
```
- **macOS/Linux:**
```bash
source math_marathon_env/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the application:
```bash
streamlit run app.py
```

## Usage

1. **Launch the Application:**
   - The app will open in your browser at `http://localhost:8501`
   - Or use the shortcut: `001-shortcut-python-env.bat`

2. **Enter Your Name:**
   - Type your name to create or access your user profile

3. **Configure Quiz Settings:**
   - Select which operations to practice
   - Set the minimum and maximum numbers for questions
   - Choose the number of questions for the session
   - Enable/disable no-regrouping mode for simpler problems

4. **Take the Quiz:**
   - Answer each math question
   - View immediate feedback on your answer
   - Watch the timer as you solve problems
   - Complete all questions in your session

5. **Review Results:**
   - See your performance summary
   - View accuracy percentage
   - Check your total session time
   - Results are automatically saved

## Project Structure

```
Math-Quiz-for-kids/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── setup_and_run.bat              # Automated setup script (Windows)
├── 001-shortcut-python-env.bat    # Quick launch shortcut
├── .streamlit/
│   └── config.toml                # Streamlit configuration
├── math_marathon_env/             # Python virtual environment
├── results/                       # User quiz results (auto-generated)
├── sample snapshot/               # Sample screenshots
└── README.md                      # This file
```

## Results Storage

Quiz results are automatically saved in the `results/` directory as JSON files with the following structure:
- Filename: `{username}_results.json`
- Contains: Quiz date, questions, answers, correctness, and timing data

## Configuration

### Streamlit Settings
The app configuration is defined in `.streamlit/config.toml`. You can customize:
- Theme (light/dark mode)
- Page layout
- Additional UI settings

## Troubleshooting

### Issue: Virtual environment not activating
- Ensure Python is installed and added to PATH
- Try using `python -m venv` instead of `venv`

### Issue: Streamlit not found
- Verify the virtual environment is activated
- Run `pip install -r requirements.txt` again

### Issue: Port 8501 already in use
- Use: `streamlit run app.py --server.port 8502`

## Future Enhancements

Planned features for future versions:
- 📈 Advanced analytics and progress tracking
- 🏆 Leaderboards and achievement badges
- 🎨 Theme customization
- 🌍 Multi-language support
- 📱 Mobile-responsive design
- 🔊 Audio feedback for answers

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Support

For issues, suggestions, or questions:
- Open an issue on [GitHub Issues](https://github.com/adnan-ttj-1987/Math-Quiz-for-kids/issues)
- Contact the project maintainer

## Author

**Adnan**  
- GitHub: [@adnan-ttj-1987](https://github.com/adnan-ttj-1987)

---

**Version:** 1.0.0  
**Last Updated:** March 2026

Enjoy learning math with Math Pro Marathon! 🚀
