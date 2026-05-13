# 🏋️ Habit Tracking Application

A comprehensive Django-based REST API for tracking workout habits, managing fitness goals, and generating personalized workout plans. Built with modern technologies for scalability, performance, and user engagement.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Architecture](#project-architecture)
- [Module Structure](#module-structure)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Database Models](#database-models)
- [Workflow](#workflow)
- [Management Commands](#management-commands)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

The Habit Tracking Application is designed to help users build and maintain consistent fitness habits. It intelligently generates personalized workout plans based on user fitness levels and categories, tracks progress through daily workouts, and gamifies the experience with a points-based system.

**Key Capabilities:**
- User authentication with JWT tokens
- Dynamic workout plan generation
- Progress tracking with gamification
- Multi-level difficulty support (Beginner, Intermediate, Advanced)
- Location-based features
- Community interactions

---

## ✨ Features

### 🔐 Authentication
- User registration and login
- JWT token-based authentication
- Refresh token mechanism
- Secure password handling

### 💪 Workout Management
- Intelligent workout plan generation
- Multi-category exercise support
- Difficulty levels (Beginner, Intermediate, Advanced)
- Daily workout assignment
- Exercise variety rotation

### 📊 Progress Tracking
- Workout completion tracking
- Daily progress monitoring
- Points-based gamification
- History preservation
- Workout statistics

### 👤 User Profiles
- User profile management
- Bio and personal information
- Goal setting integration
- Location tracking

### 🌍 Community & Location
- Location-based features
- Community interactions
- Social engagement

---

## 🛠️ Tech Stack

### Backend
- **Framework:** Django 5.1.3
- **REST API:** Django REST Framework 3.15.2
- **Authentication:** Django REST Framework SimpleJWT 5.3.1
- **Database:** PostgreSQL (psycopg2)
- **Task Queue:** Celery 5.4.0
- **Cache:** Redis 5.2.1

### Frontend Integration
- **Mobile:** React Native (Android support via `react-native run-android`)
- **Server:** Gunicorn 23.0.0
- **CORS:** django-cors-headers 4.7.0

### Cloud & Storage
- **Cloud Storage:** Cloudinary
- **Cloud Integration:** django-cloudinary-storage 0.3.0

### Additional Libraries
- **Data Processing:** Pandas 2.2.3, NumPy 1.26.4
- **Serialization:** djangorestframework-simplejwt 5.3.1
- **Database URL:** dj-database-url 2.3.0
- **Image Processing:** Pillow 10.0+

---

## 🏗️ Project Architecture

```
habit-tracking/
├── main_hbt/                   # Django Project Root
│   ├── main_hbt/              # Project Settings
│   │   ├── settings.py        # Django configuration
│   │   ├── urls.py            # Main URL router
│   │   ├── asgi.py            # ASGI configuration
│   │   └── wsgi.py            # WSGI configuration
│   │
│   ├── authn_user/            # Authentication Module
│   │   ├── models.py          # User model
│   │   ├── views.py           # Auth endpoints
│   │   ├── serializers.py     # Auth serializers
│   │   ├── token_generate.py  # JWT token generation
│   │   ├── urls.py            # Auth routes
│   │   └── permissions.py     # Auth permissions
│   │
│   ├── profile_app/           # User Profile Module
│   │   ├── models.py          # UserProfile model
│   │   ├── views.py           # Profile endpoints
│   │   ├── serializers.py     # Profile serializers
│   │   └── urls.py            # Profile routes
│   │
│   ├── quest_app/             # Workout Management Module
│   │   ├── models.py          # Workout models (DayPlan, Exercise, etc.)
│   │   ├── views.py           # Workout endpoints
│   │   ├── serializers.py     # Workout serializers
│   │   ├── utils.py           # Utility functions
│   │   ├── urls.py            # Workout routes
│   │   └── apps.py            # App configuration
│   │
│   ├── location_app/          # Location Features Module
│   │   ├── models.py          # Location models
│   │   ├── views.py           # Location endpoints
│   │   ├── serializers.py     # Location serializers
│   │   └── urls.py            # Location routes
│   │
│   ├── community_app/         # Community Module
│   │   ├── models.py          # Community models
│   │   ├── views.py           # Community endpoints
│   │   └── urls.py            # Community routes
│   │
│   ├── manage.py              # Django management script
│   └── requirements.txt        # Python dependencies
│
├── requirements.txt           # Root requirements (optional)
└── README.md                  # This file
```

---

## 📦 Module Structure

### 1. **Authentication Module** (`authn_user`)
Handles all user authentication operations.

**Models:**
- `User` - Custom user model with email-based authentication

**Views:**
- `Registerviwe` - User registration endpoint
- `Loginview` - User login endpoint
- `RefershAccessToken` - Token refresh endpoint

**Key Files:**
- `token_generate.py` - JWT token generation and refresh logic

**API Routes:**
```
POST   /signup/                    - User registration
POST   /signin/                    - User login
POST   /refershaccesstoken/        - Refresh access token
```

---

### 2. **Profile Module** (`profile_app`)
Manages user profiles and biographical information.

**Models:**
- `UserProfile` - Extended user profile with bio and metadata

**Views:**
- `ProfileUpdate` - User profile update endpoint
- `BioRetrieveUpdate` - Bio retrieve and update endpoint

**API Routes:**
```
GET    /profile/userprofile/      - Get user profile
PUT    /profile/userprofile/      - Update user profile
GET    /profile/bio/              - Get user bio
PUT    /profile/bio/              - Update user bio
```

---

### 3. **Quest/Workout Module** (`quest_app`) - **Core Module**
The central module managing workout plans and progress.

**Models:**
- `DayPlan` - Daily workout schedules (e.g., Day 1-7)
- `ExerciseCategory` - Categories of exercises (e.g., Cardio, Strength)
- `Exercise` - Individual exercises with metadata
- `Level` - Difficulty levels with reps and sets
- `Status` - User's current workout status and goals
- `WorkoutPlan` - Generated workout plans for users
- `WorkoutProgress` - Daily progress tracking

**Views:**
- `StatusCreate` - Create and list user status
- `StatusUpdate` - Update user status and regenerate plans
- `WorkoutPlanList` - Get workout plans for specific day
- `UpdateWorkoutProgress` - Track workout completion

**Key Utilities** (`utils.py`):
- `generate_workoutplan()` - Dynamically generates workout plans
- `check_workout_progress()` - Validates and updates progress

**API Routes:**
```
GET    /profile/quest/status/                    - List statuses
POST   /profile/quest/status/                    - Create status
GET    /profile/quest/status/<id>/               - Get status
PUT    /profile/quest/status/<id>/               - Update status
GET    /profile/quest/<day_id>/workoutplan/      - Get daily workout
POST   /profile/quest/workoutprogress/           - Update progress
```

---

### 4. **Location Module** (`location_app`)
Handles location-based features.

**Models:**
- `Location` - User location data

**Views:**
- `LocationView` - Create/list locations
- `UpdateLocationView` - Update location details

**API Routes:**
```
GET    /location/                 - List locations
POST   /location/                 - Create location
GET    /location/<id>/            - Get location
PUT    /location/<id>/            - Update location
```

---

### 5. **Community Module** (`community_app`)
Manages community interactions and social features.

---

## 🚀 Installation & Setup

### Prerequisites
- **Python 3.9+**
- **PostgreSQL 12+** (or MySQL 5.7+)
- **Redis** (for caching)
- **Node.js & npm** (for React Native)
- **Git**

### Step 1: Clone Repository
```bash
git clone https://github.com/DheenadhayalanR/habit-tracking.git
cd habit-tracking
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
cd main_hbt
pip install -r requirements.txt
```

### Step 4: Environment Configuration
Create a `.env` file in the `main_hbt` directory:
```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/habit_tracking

# JWT Settings
JWT_SECRET=your-jwt-secret

# Cloudinary
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Redis
REDIS_URL=redis://localhost:6379/0

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Step 5: Database Setup
```bash
# Create database
createdb habit_tracking

# Run migrations
python manage.py migrate

# Load fixture data
python manage.py loaddata quest_app/fixtures/default_data.json
```

### Step 6: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

---

## 🎮 Running the Application

### Backend Server

**Development Mode:**
```bash
cd main_hbt
python manage.py runserver
```
Access API at: `http://localhost:8000/`

**Production Mode:**
```bash
gunicorn main_hbt.wsgi:application --bind 0.0.0.0:8000
```

### Frontend (React Native)

**Android Development:**
```bash
npx react-native run-android
```

**iOS Development (macOS only):**
```bash
npx react-native run-ios
```

### Celery (Background Tasks)

**Start Celery Worker:**
```bash
celery -A main_hbt worker -l info
```

**Start Celery Beat (Scheduler):**
```bash
celery -A main_hbt beat -l info
```

### Redis (Caching)

```bash
# Start Redis server
redis-server

# Or via Docker
docker run -d -p 6379:6379 redis:latest
```

---

## 🔌 API Endpoints

### Authentication Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/signup/` | Register new user |
| POST | `/signin/` | Login user |
| POST | `/refershaccesstoken/` | Refresh JWT token |

### Profile Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/PUT | `/profile/userprofile/` | Manage user profile |
| GET/PUT | `/profile/bio/` | Manage user bio |

### Workout Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/profile/quest/status/` | Manage user status |
| GET/PUT | `/profile/quest/status/<id>/` | Get/update specific status |
| GET | `/profile/quest/<day_id>/workoutplan/` | Get workout plan for day |
| POST | `/profile/quest/workoutprogress/` | Update workout progress |

### Location Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/location/` | Manage locations |
| GET/PUT | `/location/<id>/` | Get/update location |

---

## 🗄️ Database Models

### Quest App Models

**DayPlan**
```
- day_name (CharField): Day identifier (e.g., "Day 1")
```

**ExerciseCategory**
```
- category_name (CharField): Name of exercise category
- category_description (TextField): Category details
```

**Exercise**
```
- exercise_id (AutoField): Primary key
- exercise_name (CharField): Name of exercise
- category (ManyToMany): Associated categories
- description (TextField): Exercise instructions
- target_zones_major (CharField): Primary muscle groups
- target_zones_minor (CharField): Secondary muscle groups
- equipment (CharField): Required equipment
```

**Level**
```
- level (CharField): Level name (Beginner, Intermediate, Advanced)
- reps (IntegerField): Recommended repetitions
- sets (IntegerField): Recommended sets
```

**Status**
```
- user (ForeignKey → UserProfile): User reference
- level (ForeignKey → Level): User's fitness level
- exe_category (ForeignKey → ExerciseCategory): Chosen category
- points (IntegerField): Gamification points
```

**WorkoutPlan**
```
- user_status (ForeignKey → Status): Associated status
- day (ForeignKey → DayPlan): Planned day
- exercises (ForeignKey → Exercise): Exercise to perform
```

**WorkoutProgress**
```
- user_status (ForeignKey → Status): User status
- day (ForeignKey → DayPlan): Current day
- total_day (IntegerField): Total days completed
- workout_completed (BooleanField): Completion status
```

---

## 🔄 Workflow

### User Workout Journey

```
1. USER REGISTRATION
   └─ POST /signup/
      └─ Create User account
      └─ Generate JWT tokens

2. USER LOGIN
   └─ POST /signin/
      └─ Authenticate credentials
      └─ Return access/refresh tokens

3. CREATE PROFILE
   └─ PUT /profile/userprofile/
      └─ Set user details

4. START FITNESS JOURNEY
   └─ POST /profile/quest/status/
      ├─ Select fitness level
      ├─ Choose exercise category
      └─ Trigger generate_workoutplan()
         ├─ Create 7-day workout plan
         ├─ Randomly select 2 exercises per day
         └─ Initialize WorkoutProgress

5. VIEW DAILY WORKOUT
   └─ GET /profile/quest/<day_id>/workoutplan/
      └─ Retrieve:
         ├─ Exercise names for the day
         ├─ Reps and sets based on level
         └─ Exercise details

6. TRACK PROGRESS
   └─ POST /profile/quest/workoutprogress/
      ├─ Mark workout as completed
      ├─ Update progress record
      ├─ check_workout_progress()
      │  └─ Increment day counter
      │  └─ Reset completion flag
      └─ Award points

7. UPDATE GOALS
   └─ PUT /profile/quest/status/<id>/
      ├─ Change fitness level/category
      └─ Regenerate workout plans

8. TRACK LOCATION
   └─ POST/PUT /location/
      └─ Save user location data
```

### Core Workflow Functions

**`generate_workoutplan(category, user, status_id)`**
```
Function: Generate personalized workout plans
Input:
  - category: Exercise category selected
  - user: UserProfile instance
  - status_id: Status ID for the plan
Process:
  1. Fetch all exercises in category
  2. Create plans for each day (7 days)
  3. Randomly select 2 exercises per day
  4. Initialize progress tracker
Output: WorkoutPlan instances created
```

**`check_workout_progress(status_id)`**
```
Function: Update workout progress and advance days
Input:
  - status_id: Status ID to update
Process:
  1. Fetch current progress record
  2. Mark workout as completed
  3. Advance to next day
  4. Increment total day counter
  5. Reset workout_completed flag
Output: Updated progress record
```

---

## 🛠️ Management Commands

### Database Management

**Remove migrations:**
```bash
# Windows
for /d /r . %i in (migrations) do if exist "%i" rd /s /q "%i"

# Linux/macOS
find . -type d -name migrations -exec rm -rf {} +
```

**Load fixture data:**
```bash
python manage.py loaddata app_name/fixtures/name.json

# Example
python manage.py loaddata quest_app/fixtures/default_data.json
```

**Example Fixture Format:**
```json
[
  {
    "model": "quest_app.DayPlan",
    "pk": 1,
    "fields": {
      "day_name": "Day 1"
    }
  },
  {
    "model": "quest_app.DayPlan",
    "pk": 2,
    "fields": {
      "day_name": "Day 2"
    }
  }
]
```

### Custom Commands

**Create custom management command:**
```bash
# Create structure
python manage.py startapp your_app

# Create command file
mkdir -p main_hbt/your_app/management/commands
touch main_hbt/your_app/management/__init__.py
touch main_hbt/your_app/management/commands/__init__.py
touch main_hbt/your_app/management/commands/your_command.py
```

**Command file template:**
```python
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Your command description'
    
    def add_arguments(self, parser):
        parser.add_argument('arg_name', type=str)
    
    def handle(self, *args, **options):
        # Your command logic here
        self.stdout.write('Success!')
```

**Run custom command:**
```bash
python manage.py your_command
```

---

## ⚙️ Configuration

### Django Settings (`settings.py`)

**Installed Apps:**
```python
INSTALLED_APPS = [
    # Django defaults
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'cloudinary',
    'cloudinary_storage',
    
    # Custom apps
    'authn_user',
    'profile_app',
    'community_app',
    'quest_app',
    'location_app',
]
```

**Middleware:**
```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]
```

**REST Framework Configuration:**
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

---

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Write unit tests for new features

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📞 Support & Contact

For issues, questions, or suggestions:
- **Open an Issue** on GitHub
- **Email:** dhayadhaya444@gmail.com
- **GitHub:** [@DheenadhayalanR](https://github.com/DheenadhayalanR)

---

## 🚀 Future Enhancements

- [ ] Machine learning for personalized workout recommendations
- [ ] Social workout challenges
- [ ] Wearable device integration
- [ ] Advanced analytics dashboard
- [ ] Nutrition tracking integration
- [ ] Real-time notifications
- [ ] Video exercise tutorials

---

**Built with ❤️ by DheenadhayalanR**
