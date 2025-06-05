
# 🧠 E-Learning Platform - Complete Documentation

A modular and fully RESTful backend for an e-learning platform built using Django and Django REST Framework (DRF), supporting multi-role users, hierarchical course management, diverse assessments, real-time collaboration, and more.

---

## 📁 Project Structure

```
project/
├── account/         # User authentication and profiles
├── formation/       # Course system (formations, levels, lessons)
├── examen/          # Exams and responses
├── feedback/        # Feedback from students
├── questions/       # Q&A system
├── quiz/            # Quizzes
├── test/            # Tests and evaluations
├── reunion/         # Real-time meetings
├── config/          # Settings and URL routing
└── manage.py        # Django management CLI
```

---

## 🔐 Authentication & Users (`/account/`)
- `POST /account/register/`: Register new user  
- `POST /account/login/`: Login (JWT)  
- `POST /account/refresh/`: Refresh JWT  
- `GET /account/profile/`: Get current user profile  
- CRUD endpoints for `etudiants`, `formateurs`, `points`, and `diplomes`

---

## 📚 Courses & Content (`/formation/`)
- **Formations, Niveaux, Cours**: Full CRUD for courses and lessons  
- **Enrollments**: Add/remove students to/from levels  
- **Mots-Clés**: Manage course keywords  
- Supports deeply nested structures for content delivery

---

## 📝 Exams (`/examen/`)
- Manage exams and questions  
- Submit auto/manuel responses  
- Evaluate results

---

## ❓ Quizzes (`/quiz/`)
- Create quizzes with questions and choices  
- Submit and review responses  
- Full quiz lifecycle management

---

## 🧪 Tests (`/test/`)
- Manage test banks  
- Handle automatic/manual responses and evaluations

---

## 💬 Q&A System (`/questions/`)
- Post, update, and delete student questions

---

## 📥 Feedback (`/feedback/`)
- Students post feedback  
- Admins respond and manage feedback records

---

## 📅 Meetings (`/reunion/`)
- Schedule meetings  
- Add/remove participants

---

## 🔧 Core Models

### 👤 Account
- `Compte`, `Utilisateur`, `Etudiant`, `Formateur`, `Gerant`
- `PointInterest`, `Diplome`

### 🎓 Formation
- `Formation`, `Niveaux`, `Cours`, `Inscrit`, `Requirement`, `MoteCles`

### 🧾 Assessments
- `Exam`, `Quiz`, `Test` + their `Question`, `Choix`, `Reponse`, `Evaluation` models

### 💬 Collaboration
- `Feedback`, `Question`, `Reunion`, `ParticiperReunion`

---

## ✨ Key Features

- ✅ Multi-role JWT Authentication
- 🧱 Modular & Nested REST API
- 🧠 Smart grading with auto/manual assessment
- 🔁 Realtime-friendly Q&A and meetings
- 🎯 Strong model relations for data consistency

---

## ⚙️ Installation

```bash
# Create virtual env
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt  # or manually:
pip install django djangorestframework djangorestframework-simplejwt psycopg2

# Migrate DB
python manage.py migrate

# Run server
python manage.py runserver
```

---

## 🧪 Testing

```bash
python manage.py test account formation examen feedback questions quiz test
```

---

## 🔐 Environment Variables

Create a `.env` file with:

```ini
SECRET_KEY=your_django_secret_key
DB_NAME=elearning
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DEBUG=True
```

---

## 🧰 Tech Stack

- **Backend:** Django 4.x, Django REST Framework  
- **Auth:** JWT via SimpleJWT  
- **Database:** PostgreSQL  
- **Docs:** OpenAPI / Swagger UI (recommended)  
- **Deployment:** Docker + Gunicorn + Nginx (optional)

---

## 📄 License

This project is under the MIT License.

---

## 🙌 Contributions

Feel free to fork the repo, submit issues, or contribute via pull requests!

---

## 📫 Contact

Built with ❤️ by [ayoub]. For questions, contact: ayoubled43@gmail.com


