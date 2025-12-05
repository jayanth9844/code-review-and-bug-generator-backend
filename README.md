# 🔍 AI-Powered Code Review & Bug Generation Platform

> **Intelligent code analysis and automated bug injection system powered by advanced AI technology**

---

## 🌐 Live Deployment

- **🚀 Frontend**: [https://code-review-and-bug-generator-front.vercel.app/](https://code-review-and-bug-generator-front.vercel.app/)
- **⚙️ Backend API**: [https://code-review-and-bug-generator-backend-2.onrender.com](https://code-review-and-bug-generator-backend-2.onrender.com)

---

## 📖 What This Project Does

This platform is an **AI-driven code analysis and bug injection tool** designed to help developers, QA engineers, and software teams improve code quality and test robustness. It leverages cutting-edge artificial intelligence to automatically review code, identify potential issues, and generate realistic bugs for testing purposes.

### Core Capabilities:

✅ **Automated Code Review** - Instantly analyze code snippets to detect bugs, security vulnerabilities, code smells, and best practice violations

✅ **Intelligent Bug Injection** - Generate realistic bugs with customizable types, severity levels, and quantities for comprehensive testing

✅ **Code Quality Metrics** - Get detailed metrics including quality scores, security ratings, bug density, and issue distribution

---

## 👥 Who Is This For?

- **Software Developers** - Get instant code reviews and improve code quality before deployment
- **QA Engineers** - Generate realistic test cases and edge-case scenarios automatically
- **Code Reviewers** - Streamline the review process with AI-assisted analysis
- **Students & Learners** - Understand common coding mistakes and best practices
- **Tech Teams** - Establish consistent code quality standards across projects

---

## 🎯 Expected Output

### 1. **Code Analysis Results**
Receive comprehensive issue reports with:
- Issue title, type, and severity level (Low, Medium, High, Critical)
- Exact line numbers where issues occur
- Detailed descriptions of each problem
- Actionable suggestions for fixes

### 2. **Code Quality Metrics**
Get quantified insights including:
- Overall code quality score (0-100)
- Security rating (0-100)
- Bug density count
- Critical issue count
- Distribution by category (security, performance, code smells, best practices)

### 3. **Bug-Injected Code**
Generate modified code with:
- Intentionally injected bugs based on your specifications
- Complete documentation of each bug's type, location, and description
- Customizable severity levels (1-10 scale)
- Variable bug counts for comprehensive testing

---

## 🛠️ Technologies Used

### **Backend**
- **FastAPI** - High-performance Python web framework
- **Python 3.x** - Core programming language
- **LangChain** - AI orchestration and prompt engineering
- **Google Gemini AI** - Advanced language model for code analysis
- **Uvicorn** - ASGI server for production deployment

### **Infrastructure**
- **Render** - Cloud deployment platform for backend services
- **Vercel** - Frontend hosting and deployment
- **CORS** - Cross-origin resource sharing for secure API access

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key

### Installation

```bash
# Clone the repository
git clone https://github.com/jayanth9844/code-review-and-bug-generator-backend.git

# Navigate to project directory
cd code-review-and-bug-generator-backend

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create a .env file with your API key:
# API_KEY=your_gemini_api_key_here

# Run the server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

---

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## 💡 Use Cases

1. **Pre-Commit Code Review** - Scan code before committing to catch issues early
2. **Testing Automation** - Generate bug scenarios for comprehensive test coverage
3. **Security Audits** - Identify potential security vulnerabilities automatically
4. **Learning Tool** - Understand common coding mistakes and improve skills
5. **CI/CD Integration** - Incorporate automated code quality checks in pipelines

---

## 📦 Project Structure

```
code-review-and-bug-generator-backend/
├── app/
│   ├── main.py           # FastAPI application entry point
│   ├── services.py       # Core AI-powered analysis services
│   └── api/              # API route handlers
├── requirements.txt      # Python dependencies
├── .env                  # Environment configuration
└── README.md            # Project documentation
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve the platform.

---

## 📄 License

This project is available for educational and professional use.

---

## 👨‍💻 Developer

**Jayanth Raj G**  
*Backend Developer & AI Engineer*

---

**⭐ Star this repository if you find it helpful!**