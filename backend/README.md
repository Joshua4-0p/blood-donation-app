# Blood Donation Application Backend

## Project Overview

This is the backend for a blood donation application built with FastAPI and PostgreSQL. The application connects donors and hospitals to prevent blood shortages, with an AI-driven eligibility check for donors using Langchain and an LLM.

### Key Features

- **User Management**: Users (donors) can register, log in, update profiles, and opt to donate blood
- **Hospital Management**: Hospitals register (pending verification), create blood requests, and view donors/requests
- **Donation Management**: Users submit a health questionnaire, processed by AI to determine eligibility. Eligible donors are listed for hospitals to contact
- **Request Management**: Only verified hospitals can create blood requests (blood type, quantity, urgency, location)
- **Search and Matching**: Hospitals search donors by blood type and location, with known blood types prioritized
- **Privacy**: Only hospitals handle requests to ensure confidentiality of medical data

The database uses PostgreSQL with SQLAlchemy ORM, and routes are modularized for parallel development.

## Project Structure

```
blood-donation-backend/
├── routes/              # Route modules for each feature
│   ├── users.py        # User-related endpoints
│   ├── hospitals.py    # Hospital-related endpoints
│   ├── donations.py    # Donation-related endpoints
│   ├── requests.py     # Request-related endpoints
│   └── auth.py         # Authentication endpoint
|   
├── models/               
│   └── eligibility.py  # AI eligibility check logic
|   ├── models.py       # SQLAlchemy ORM models
|   ├── schema.py       # PostgreSQL schema definitions
|   ├── auth.py         # Auth models
├── database.py         # Database connection and session setup
├── crud.py          
├── main.py            # FastAPI app entry point
├── .env               # Template for environment variables
├── README.md          # This file
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- PostgreSQL 13+
- Git
- Virtualenv (recommended)

### Installation

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd blood-donation-backend
   ```

2. **Set Up Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Create `requirements.txt` with:
   ```
   fastapi==0.115.0
   sqlalchemy==2.0.36
   psycopg2-binary==2.9.9
   python-dotenv==1.0.1
   pydantic==2.9.2
   bcrypt==4.2.0
   python-jose[cryptography]==3.3.0
   langchain==0.3.1
   uvicorn==0.31.1
   pytest==8.3.3
   ```

4. **Set Up PostgreSQL Database:**
   - Create a database: `createdb blood_donation`
   - Run the schema: `psql -d blood_donation -f schema.sql`

5. **Configure Environment:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Update `.env` with your PostgreSQL credentials:
     ```
     DATABASE_URL=postgresql://username:password@localhost:5432/blood_donation
     ```

6. **Run the Application:**
   ```bash
   uvicorn main:app --reload
   ```

   Access the API at http://localhost:8000 and Swagger docs at http://localhost:8000/docs.

## Task Assignments

The backend is divided into feature areas, each assigned to a developer. Implement your routes in the respective `routes/` module and integrate them into `main.py`.

### Developer 1: User Management (`routes/users.py`)

**Endpoints:**
- `POST /users/register`: Register a new user (name, email, password, blood type, etc.)
- `POST /users/login`: Authenticate user (return JWT token)
- `GET /users/me`: Get current user's profile (authenticated)
- `PUT /users/me`: Update user profile (authenticated)

**Tasks:**
- Use bcrypt for password hashing
- Implement JWT authentication (python-jose)
- Create Pydantic schemas (e.g., UserCreate, UserResponse)
- Validate blood type using BloodType enum from models.py

### Developer 2: Hospital Management (`routes/hospitals.py`)

**Endpoints:**
- `POST /hospitals/register`: Register a hospital (pending verification)
- `PUT /hospitals/{id}/verify`: Admin verifies hospital (sets verified=True)
- `GET /hospitals/{id}`: Get hospital details (public or authenticated)
- `PUT /hospitals/{id}`: Update hospital details (authenticated hospital only)

**Tasks:**
- Ensure only verified hospitals can create requests
- Implement hospital-specific authentication

### Developer 3: Donation Management (`routes/donations.py`)

**Endpoints:**
- `POST /donations`: Submit donation form (health questionnaire, processed by AI)
- `GET /donations`: Search available donors (filter by blood type, location; sort known blood types first)
- `PUT /donations/{id}/status`: Update donation status (e.g., 'in_progress', 'completed') by hospital

**Tasks:**
- Call AI eligibility check from `ai/eligibility.py` for `POST /donations`
- Implement geospatial search (e.g., `LIKE '%city%'` or use PostGIS for advanced queries)
- Sort donors with known blood types first (`CASE WHEN blood_type = 'Unknown' THEN 1 ELSE 0 END`)

### Developer 4: Request Management (`routes/requests.py`)

**Endpoints:**
- `POST /requests`: Create a blood request (hospital only)
- `GET /requests`: List requests (filter by blood type, location, urgency)
- `PUT /requests/{id}`: Update request (hospital only)
- `DELETE /requests/{id}`: Cancel request (hospital only)

**Tasks:**
- Restrict endpoints to verified hospitals
- Validate blood type and urgency using enums from models.py

### Developer 5: AI Integration and Admin Tasks (`routes/admin.py`, `ai/eligibility.py`)

**Endpoints:**
- `POST /admin/verify-hospital/{id}`: Admin verifies hospital

**Tasks:**
- Implement AI eligibility check in `ai/eligibility.py` using Langchain + LLM (e.g., Grok or OpenAI)
- Example AI logic:
  ```python
  from langchain import LLMChain, PromptTemplate
  from langchain.llms import OpenAI  # or Grok

  prompt = PromptTemplate(
      input_variables=["questionnaire"],
      template="Analyze this donor questionnaire: {questionnaire}. Check against WHO eligibility criteria. Return eligibility status and reasons."
  )
  llm = OpenAI(api_key="your-api-key")  # or Grok
  chain = LLMChain(llm=llm, prompt=prompt)

  async def check_eligibility(questionnaire: dict):
      result = await chain.run(questionnaire=str(questionnaire))
      return result
  ```
- Provide this function for Developer 3 to use in `POST /donations`

## Development Guidelines

### Route Implementation

Use FastAPI's APIRouter in your module (e.g., `routes/users.py`).

**Example:**
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from pydantic import BaseModel

router = APIRouter()

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email, password_hash="hashed")
    db.add(db_user)
    db.commit()
    return {"message": "User registered"}
```

- Use `get_db` dependency for database sessions
- Define Pydantic schemas for request/response validation

### Authentication

- Implement JWT for users and hospitals (Developer 1 can create a shared `auth.py`)
- Example: `get_current_user` dependency to check JWT tokens

### Error Handling

Use HTTPException for errors (e.g., `HTTPException(status_code=400, detail="Email already exists")`).

### Testing

Write unit tests in `tests/` using pytest and `fastapi.testclient`.

**Example:**
```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/users/register", json={
        "name": "John Doe",
        "email": "john@example.com",
        "password": "secure123"
    })
    assert response.status_code == 200
```

### Integration

Add your router to `main.py`:
```python
from routes.users import router as users_router
app.include_router(users_router, prefix="/users", tags=["users"])
```

Test locally before pushing.

### Version Control

- Work on a feature branch (e.g., `git checkout -b feature/users`)
- Commit often with clear messages (e.g., "Add user registration endpoint")
- Push to your branch and create a pull request for review

## Contributing

- Follow PEP 8 for Python code
- Document endpoints in FastAPI's OpenAPI (use tags and description)
- Test your routes thoroughly with a local PostgreSQL instance
- Coordinate with the team for shared dependencies (e.g., auth.py, AI logic)
- Report issues or blockers in the team's communication channel (e.g., Slack, Discord)

## Notes

- **Database**: Use `schema.sql` to set up tables. Add indexes as needed for performance
- **AI**: Developer 5 will provide the AI eligibility function. Others can assume it returns a JSON like `{"eligible": true, "reason": "Meets WHO criteria"}`
- **Security**: Encrypt sensitive data (e.g., `password_hash`, `health_questionnaire`). Restrict endpoints to authenticated/verified users/hospitals
- **Future Enhancements**: Add geospatial search with PostGIS, notifications, or patient tracking (hospital-only)

For questions, contact the team lead or check the repository's issue tracker.