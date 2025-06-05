# e_learining_backend
This Django backend powers a sophisticated e-learning platform with multi-role users, hierarchical course structures, diverse assessment systems, and real-time collaboration features. The system follows a modular design with clear separation of concerns between different educational components.
# E-Learning Platform - Django Backend

## Project Overview
This Django backend powers an e-learning platform with comprehensive features:
- Multi-role user authentication (students, trainers, managers)
- Course management with hierarchical structure
- Multiple assessment systems (exams, quizzes, tests)
- Live meetings functionality
- Q&A system
- Feedback management
- RESTful API for frontend integration

## Models Structure

### Core Modules
1. **Account Management**
   - `Compte`: Custom user model (email-based authentication)
   - `Utilisateur`: Base user profile with subtypes:
     - `Etudiant` (Student)
     - `Formateur` (Trainer)
     - `Gerant` (Manager)
   - Interest points (`PointInterest`) and diplomas (`Diplome`)

2. **Formation System**
   - `Formation`: Courses with prerequisites
   - `Niveaux`: Difficulty levels within courses
   - `Cours`: Learning content (videos/PDFs/audio)
   - `Inscrit`: Enrollment records
   - `MoteCles`: Course keywords/tags

3. **Assessment Systems**
   - **Exams**:
     - `Exam`: Exams with state management
     - `QuestionExam`: Auto/manual corrected questions
     - Response and evaluation models
   - **Quizzes**:
     - `Quiz`: Level-specific quizzes
     - `QuestionQuiz`: Quiz questions
     - `ChoixQuiz`: Quiz options
     - `ReponseQuiz`: Student responses
   - **Tests**:
     - `Test`: Formation-level tests
     - `QuestionTest`: Test questions
     - `ReponseTestAuto/ReponseTestManuel`: Student responses
     - `EvaluationResultTest`: Manual evaluations

4. **Collaboration Modules**
   - `Reunion`: Live meetings organized by trainers
   - `ConcerneReunion`: Meeting-level relationships
   - `ParticiperReunion`: Meeting participants
   - `Question`: Student questions with trainer responses

5. **Feedback Module**
   - `Feedback`: Student/trainer feedback with admin responses

## API Endpoints

### Account App
```http
POST /account/register/        # User registration
POST /account/login/           # JWT authentication
POST /account/refresh/         # Token refresh
GET  /account/profile/         # User profile
GET  /account/etudiants/       # Student list
GET  /account/formateurs/      # Trainer list

and for more information contect me 
