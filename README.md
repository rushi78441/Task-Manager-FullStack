# Task Manager Full-Stack Application

A robust, full-stack Task Management application featuring a decoupled architectural model. The backend is designed with FastAPI leveraging a Test-Driven Development (TDD) approach, and the frontend is a modern reactive UI engineered with React and Tailwind CSS. The project includes automated Continuous Integration (CI) workflows and containerized environments.

---

## 📋 Table of Contents
1. [Architectural Overview & Layout](#1-architectural-overview--layout)
2. [Backend Blueprint & System Design](#2-backend-blueprint--system-design)
3. [Authentication and Security Protocols](#3-authentication-and-security-protocols)
4. [SOLID Design Principles Applied](#4-solid-design-principles-applied)
5. [Test-Driven Development (TDD) Specification](#5-test-driven-development-tdd-specification)
6. [Continuous Integration (CI) Automation](#6-continuous-integration-ci-automation)
7. [Installation & Deployment](#7-installation--deployment)

---

## 1. Architectural Overview & Layout

The **Task Manager Full-Stack Application** is constructed using a decoupled architectural design pattern separating a stateless, highly optimized asynchronous RESTful API layer (**FastAPI**) from a rich, declarative single-page user interface (**React + Tailwind CSS**). 

### Directory Layout
```text
├── .github/
│   └── workflows/
│       └── python-app.yml       # Unified CI multi-context orchestration
├── backend/
│   ├── app/
│   │   ├── database/           # Connection engines and sessions
│   │   ├── domain/             # Core business entity logic layers
│   │   ├── routes/             # FastAPI routing modules (Endpoints)
│   │   ├── schemas/            # Data validation using Pydantic models
│   │   ├── security/           # Hashing and authentication implementations
│   │   ├── sql_repo/           # Data access repository layer implementations
│   │   ├── config.py           # Application environment configurations
│   │   ├── interfaces.py       # Core interface layer abstractions
│   │   └── main.py             # Main application entry point
│   ├── tests/
│   │   ├── test_auths.py       # TDD suites for security and login workflows
│   │   └── test_tasks.py       # TDD suites for CRUD task management
│   ├── .TaskManager.db         # SQLite dynamic datastore
│   ├── compose.yaml            # Docker Compose backend orchestrations
│   ├── Dockerfile              # Container building blueprints
│   └── requirements.txt        # Frozen dependencies manifest
└── frontend/
    ├── src/
    │   ├── assets/             # Static graphic assets and logos
    │   ├── components/         # Reusable presentation parts (TaskForm, TaskItem)
    │   ├── pages/              # Structural view routing (DashBoardPage, LoginPage, RegisterPage)
    │   ├── App.jsx             # Main Application layout context
    │   └── main.jsx            # DOM anchoring injection layer
    ├── compose.yaml            # Docker Compose frontend orchestrations
    ├── Dockerfile              # Container building blueprints
    ├── package.json            # Node configuration scripts
    └── vite.config.js          # Vite build tool optimizations
```

---

## 2. Backend Blueprint & System Design

The backend conforms strictly to a **Clean Layered Architecture**, separating concerns so changes in outer infrastructures (like databases) have minimal impact on core data policies.

### Backend Structural Diagram
```text
  ┌─────────────────────────────────────────────────────────┐
  │                   INTERFACE LAYER                       │
  │     [ app/routes/ & app/interfaces.py ]                 │
  │     - JSON Parsing          - HTTP Status Handling      │
  │     - Request/Response      - Dependency Injection      │
  └────────────────────────────┬────────────────────────────┘
                               │ (Validates via Pydantic Schemas)
                               ▼
  ┌─────────────────────────────────────────────────────────┐
  │                 BUSINESS / DOMAIN LAYER                 │
  │     [ app/domain/ & app/security/ ]                     │
  │     - Hashing (Passlib)     - Task State Logic          │
  │     - JWT Token Handling    - Query Filters             │
  └────────────────────────────┬────────────────────────────
                               │ (Abstracted data layer access)
                               ▼
  ┌─────────────────────────────────────────────────────────┐
  │                  DATABASE REPOSITORY LAYER              │
  │     [ app/sql_repo/ & app/database/ ]                   │
  │     - SQLAlchemy Models     - Session Local Lifecycle   │
  │     - Core Database Engine  - SQL Operations            │
  └─────────────────────────────────────────────────────────┘
```

* **Interface Layer:** Validates runtime HTTP payloads using strict Pydantic parsing types (`app/schemas/`) and processes endpoints via unified application interfaces.
* **Business / Domain Layer:** Encapsulates core structures inside the `app/domain/` scope, completely separating structural operational code from raw framework features.
* **Database Repository Layer:** Implements data queries inside `app/sql_repo/` to decouple external storage implementations from internal system behaviors.

---

## 3. Authentication and Security Protocols

User onboarding and task manipulation are fully protected by a cryptographically signed workflow:
1. **Password Hashing:** Passwords are never stored in plaintext. They are systematically processed using the `passlib` crypt suite using **Bcrypt** salts located inside the `app/security/` module.
2. **Tokenization Strategy:** Authentication is managed out-of-band via bearer access tokens using **HMAC SHA-256 signatures**.
3. **Guard Interceptors:** Secured paths include `Depends()` handlers injected into the FastAPI routes to intercept, decrypt, and load the active database-scoped identity before handling instructions.

---

## 4. SOLID Design Principles Applied

The backend enforces decoupled, scalable software engineering practices by adapting specific SOLID principles:

* **S - Single Responsibility Principle (SRP):**
  Every directory handles precisely one execution domain. Modules inside `app/database/` configure connection life-cycles, while database interactions are completely isolated inside `app/sql_repo/` so route handlers don't directly handle queries.
* **O - Open/Closed Principle (OCP):**
  System architectures define interfaces inside `app/interfaces.py`. New behavior can be appended by extending data validation abstractions without modifying existing core logic blocks.
* **D - Dependency Inversion Principle (DIP):**
  Instead of instantiating session variables globally, endpoints depend directly on an abstracted session yield runtime injected seamlessly via FastAPI’s native Dependency Injection framework (`Depends`), ensuring effortless database replacement and mocking during test setups.

---

## 5. Test-Driven Development (TDD) Specification

The system was developed under a strict TDD mindset using `pytest`. The integration test suite abstracts interactions away from standard development states by running against ephemeral session contexts.

### Test Function Catalog

#### 🔑 Authentication Specs (`tests/test_auths.py`)
* `test_user_registration_success`: Submits valid user schemas to verify successful password hashing and persistence within the DB engine.
* `test_user_login_and_jwt_generation`: Validates plain text credentials against hashed records, issuing an authentic Bearer JWT payload with expiration metrics.

#### 📝 Task Feature Specs (`tests/test_tasks.py`)
* `test_create_task_entry`: Validates payload instantiation, making sure that newly recorded tasks securely inherit the signed-in user's index ID.
* `test_fetch_user_tasks`: Validates that fetched indices belong strictly to the authorized request handle, guaranteeing absolute isolation between users.
* `test_toggle_task_status`: Mutates state configurations (e.g., flipping `is_completed` from `false` to `true`) and asserts structural consistency.
* `test_delete_task_execution`: Dispatches drop execution instructions to verify complete entry purging from persistent relational contexts.

---

## 6. Continuous Integration (CI) Automation

The workflow maps tasks directly to targeted repository contexts using automated environment pipelines (`.github/workflows/python-app.yml`).

### Workflow Mechanics
* **Isolation Mapping:** Sets directory targets specifically to the `backend/` path space.
* **Dependency Freezing:** Generates and validates Python locks to rule out structural deviations across build versions.
* **Automation Checks:** Runs the entire TDD test harness (`test_auths.py` and `test_tasks.py`) inside a temporary runtime environment on every patch integration.
* **Docker Registry Authorization Verification:** Validates registry connectivity, verifying absolute environment stability ahead of deployment.

---

## 7. Installation & Deployment

### Backend Spin-up
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload
```

### Frontend Spin-up
```bash
cd frontend
npm install
npm run dev
```