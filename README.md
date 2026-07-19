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
│   │   ├── core/               # Security, configurations, and JWT handlers
│   │   ├── database/           # Engine setup, session management, and DB models
│   │   ├── schemas/            # Data validation using Pydantic
│   │   ├── crud/               # Isolated Database access logic 
│   │   ├── api/                # FastAPI routing paths (Endpoints)
│   │   └── main.py             # Main Application Initialization
│   ├── tests/                  # Test-Driven Development (TDD) Suite
│   ├── Dockerfile
│   └── requirements.txt
└── frontend/
    ├── src/                    # UI Components and state integration
    ├── package.json
    ├── tailwind.config.js
    └── vite.config.js
```

---

## 2. Backend Blueprint & System Design

The backend conforms strictly to a **Clean Layered Architecture**, separating concerns so changes in outer infrastructures (like databases) have minimal impact on core data policies.

### Backend Structural Diagram
```text
  ┌─────────────────────────────────────────────────────────┐
  │                   INTERFACE LAYER                       │
  │     [ FastAPI Routers / Endpoints ]                     │
  │     - JSON Parsing          - HTTP Status Handling      │
  │     - Request/Response      - Dependency Injection      │
  └────────────────────────────┬────────────────────────────┘
                               │ (Validates via Pydantic Schemas)
                               ▼
  ┌─────────────────────────────────────────────────────────┐
  │                 BUSINESS / DOMAIN LAYER                 │
  │     [ CRUD Execution Engine & Security Logic ]          │
  │     - Hashing (Passlib)     - Task State Logic          │
  │     - JWT Token Handling    - Query Filters             │
  └────────────────────────────┬────────────────────────────
                               │ (Communicates via SQLAlchemy ORM)
                               ▼
  ┌─────────────────────────────────────────────────────────┐
  │                  DATABASE LAYER                         │
  │     [ Core Engine & Relational Storage ]                │
  │     - SQLAlchemy Models     - Session Local Lifecycle   │
  │     - Core Database Engine  - SQL Operations            │
  └─────────────────────────────────────────────────────────┘
```

* **Interface Layer:** Validates runtime HTTP payloads using strict Pydantic parsing types and passes inputs down securely.
* **Business / Domain Layer:** Encapsulates the operations governing tasks and access identity.
* **Database Layer:** Manages physical records mapped dynamically over an abstracted engine instance using SQLAlchemy.

---

## 3. Authentication and Security Protocols

User onboarding and task manipulation are fully protected by a cryptographically signed workflow:
1. **Password Hashing:** Passwords are never stored in plaintext. They are systematically processed using the `passlib` crypt suite using **Bcrypt** salts.
2. **Tokenization Strategy:** Authentication is managed out-of-band via bearer access tokens using **HMAC SHA-256 signatures**.
3. **Guard Interceptors:** Secured paths include `Depends()` handlers injected into the FastAPI router to intercept, decrypt, and load the active database-scoped identity before handling instructions.

---

## 4. SOLID Design Principles Applied

The backend enforces decoupled, scalable software engineering practices by adapting specific SOLID principles:

* **S - Single Responsibility Principle (SRP):**
  Every file handles precisely one execution domain. `models.py` strictly handles schema-to-table physical maps; `schemas.py` acts exclusively as input data enforcement; `crud.py` isolation means routing pathways never directly query or append raw modifications into backend stores.
* **O - Open/Closed Principle (OCP):**
  API parameters and models extend dynamic validation parameters via Pydantic model inheritance. Features can easily configure custom serialization criteria without breaking core endpoint behaviors.
* **D - Dependency Inversion Principle (DIP):**
  Instead of instantiating session variables globally, endpoints depend directly on an abstracted session yield runtime (`get_db`) injected seamlessly via FastAPI’s native Dependency Injection framework (`Depends(get_db)`), ensuring effortless database replacement and mocking during test setups.

---

## 5. Test-Driven Development (TDD) Specification

The system was developed under a strict TDD mindset using `pytest`. The integration test suite abstracts interactions away from standard development states by running against ephemeral session contexts.

### Test Function Catalog

| Test Function | Target Scope | Description |
| :--- | :--- | :--- |
| `test_user_registration_success` | Auth / Core | Submits valid user schemas to verify successful password hashing and persistence within the DB engine. |
| `test_user_login_and_jwt_generation` | Auth / Core | Validates plain text credentials against hashed records, issuing an authentic Bearer JWT payload with expiration metrics. |
| `test_create_task_entry` | Task Feature | Validates payload instantiation, making sure that newly recorded tasks securely inherit the signed-in user's index ID. |
| `test_fetch_user_tasks` | Task Feature | Validates that fetched indices belong strictly to the authorized request handle, guaranteeing absolute isolation between users. |
| `test_toggle_task_status` | Task Feature | Mutates state configurations (e.g., flipping `is_completed` from `false` to `true`) and asserts structural consistency. |
| `test_delete_task_execution` | Task Feature | Dispatches drop execution instructions to verify complete entry purging from persistent relational contexts. |

---

## 6. Continuous Integration (CI) Automation

The workflow maps tasks directly to targeted repository contexts using automated environment pipelines (`.github/workflows/python-app.yml`).

### Workflow Mechanics
* **Isolation Mapping:** Sets directory targets specifically to the `backend/` path space.
* **Dependency Freezing:** Generates and validates Python locks to rule out structural deviations across build versions.
* **Automation Checks:** Runs the entire TDD test harness inside a temporary runtime environment on every patch integration.
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