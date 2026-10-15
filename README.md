# Hospital Management System (HMS)

A full-stack, enterprise-grade Hospital Management System built with **Java**, **Spring Boot 3**, **Spring Security**, **Spring Data JPA/Hibernate**, **MySQL**, and **Thymeleaf** with custom responsive styling.

---

## Table of Contents
1. [Overview & Features](#overview--features)
2. [Tech Stack](#tech-stack)
3. [Prerequisites](#prerequisites)
4. [Step-by-Step Setup & How to Run](#step-by-step-setup--how-to-run)
   - [Step 1: Clone the Repository](#step-1-clone-the-repository)
   - [Step 2: Database Setup & Configuration](#step-2-database-setup--configuration)
   - [Step 3: Run the Application](#step-3-run-the-application)
   - [Step 4: Access the Web Portal](#step-4-access-the-web-portal)
5. [Default Login Credentials](#default-login-credentials)
6. [Project Structure](#project-structure)
7. [Environment & Security (.gitignore)](#environment--security-gitignore)
8. [Troubleshooting](#troubleshooting)

---

## Overview & Features

The Hospital Management System provides dedicated, secure workflows tailored to three distinct user roles:

- **Admin Portal**:
  - Complete operational dashboard with high-level hospital metrics.
  - User management (view, edit, manage doctors, patients, and staff).
  - System-wide appointment oversight and schedule monitoring.
- **Doctor Portal**:
  - Personal schedule management and upcoming appointment tracking.
  - Patient consultation notes and medical record entry.
  - Patient feedback review.
- **Patient Portal**:
  - Self-service appointment booking with specialization and doctor selection.
  - Live appointment status tracking (Pending, Confirmed, Completed, Cancelled).
  - Medical history and feedback submission.
- **Security & Architecture**:
  - Role-based authorization and session management via Spring Security.
  - Passwords hashed with BCrypt.
  - Automatic schema generation and seed data initialization on first boot.

---

## Tech Stack

- **Backend**: Java 17+ (compatible with Java 17, 21, and 25), Spring Boot 3.2.5
- **Security**: Spring Security 6 (BCrypt password encoding, role-based URL protection)
- **Persistence**: Spring Data JPA, Hibernate, MySQL Connector/J
- **Database**: MySQL 8.0+
- **Frontend**: Thymeleaf template engine, HTML5, Vanilla CSS3 / Bootstrap 5 components
- **Build Tool**: Maven 3.8+ (Maven Wrapper included)

---

## Prerequisites

Before running the application, ensure you have the following installed on your machine:

1. **Java Development Kit (JDK)**: Version 17 or higher
   - Verify with: `java -version`
2. **MySQL Server**: Version 8.0 or higher
   - Ensure the MySQL service is running locally on port `3306`.
3. **Maven**: Optional (Maven Wrapper `mvnw` / `mvnw.cmd` is bundled with the project).
   - If using global Maven, verify with: `mvn -version`
4. **Git**: To clone and manage the codebase.

---

## Step-by-Step Setup & How to Run

### Step 1: Clone the Repository

Clone the project to your local machine:

```bash
git clone https://github.com/Voxy-Taskflow/hospitalManagementsystem.git
cd hospitalManagementsystem
```

---

### Step 2: Database Setup & Configuration

1. **Start MySQL Service**:
   Make sure your MySQL service is active.

2. **Database Auto-Creation**:
   The application is configured with `createDatabaseIfNotExist=true`. The database `hospital_managment` will be created automatically upon startup if your MySQL user has creation privileges.
   
   *(Optional)* You can also create it manually in your MySQL terminal or MySQL Workbench:
   ```sql
   CREATE DATABASE IF NOT EXISTS hospital_managment;
   ```

3. **Configure Database Credentials**:
   To prevent committing sensitive personal credentials to Git, the application supports local configuration overrides through several convenient methods:

   #### Option A: Local Properties File (Recommended)
   Create a file named `application-local.properties` inside the `hms/` folder (this file is already ignored by `.gitignore`):
   
   **File location**: `hms/application-local.properties`
   ```properties
   spring.datasource.username=root
   spring.datasource.password=your_actual_mysql_password
   ```

   #### Option B: Environment Variables
   Set `DB_USERNAME` and `DB_PASSWORD` before running:

   - **Windows PowerShell**:
     ```powershell
     $env:DB_USERNAME="root"
     $env:DB_PASSWORD="your_actual_mysql_password"
     ```
   - **Linux / macOS**:
     ```bash
     export DB_USERNAME=root
     export DB_PASSWORD=your_actual_mysql_password
     ```

   #### Option C: Direct Modification
   Open `hms/src/main/resources/application.properties` and replace `${DB_PASSWORD:root}` with your MySQL password.

---

### Step 3: Run the Application

Navigate into the `hms` application directory:

```bash
cd hms
```

Run the application using the Maven Wrapper (no separate Maven install required):

- **On Windows (PowerShell or Command Prompt)**:
  ```powershell
  .\mvnw.cmd spring-boot:run
  ```

- **On macOS / Linux**:
  ```bash
  chmod +x mvnw
  ./mvnw spring-boot:run
  ```

- **Or with globally installed Maven**:
  ```bash
  mvn spring-boot:run
  ```

The Spring Boot application will start and initialize the database tables automatically.

---

### Step 4: Access the Web Portal

Once the console logs show `Started HmsApplication in ... seconds`, open your web browser and navigate to:

```
http://localhost:8080
```

You will be presented with the login screen.

---

## Default Login Credentials

On initial startup, `DataInitializer` seeds test accounts so you can immediately explore each role:

| Role | Email | Password | Access URL |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin@hospital.com` | `admin123` | `http://localhost:8080/admin/dashboard` |
| **Doctor** | `doctor@hospital.com` | `doctor123` | `http://localhost:8080/doctor/dashboard` |
| **Patient** | Register a new account | Any password | `http://localhost:8080/patient/dashboard` |

> [!NOTE]
> Public registration on `http://localhost:8080/register` assigns the **PATIENT** role by default. Doctor and Admin accounts can only be provisioned by an Administrator.

---

## Project Structure

```text
hospitalManagementsystem/
├── .gitignore                    # Root Git ignore rules (targets, local credentials, IDE configs)
├── README.md                     # Complete project documentation and run guide
├── plan.md                       # Project specification and architecture plan
├── scaffold.py                   # Code generator utilities
├── add_admin_logic.py
├── add_appointments.py
├── add_doctor_logic.py
├── generate_entities.py
├── generate_misc.py
├── generate_security.py
├── generate_templates.py
├── update_frontend.py
└── hms/                          # Spring Boot Application Root
    ├── mvnw                      # Maven Wrapper script (Linux/macOS)
    ├── mvnw.cmd                  # Maven Wrapper script (Windows)
    ├── pom.xml                   # Maven dependencies & build plugins
    ├── .env.example              # Template for environment variables
    ├── application-local.properties  # (Optional local override, git-ignored)
    ├── .mvn/                     # Maven Wrapper distribution configs
    └── src/
        ├── main/
        │   ├── java/com/hospital/hms/
        │   │   ├── HmsApplication.java
        │   │   ├── config/       # Security & Seed Data configurations
        │   │   ├── controller/   # Web & REST controllers (Admin, Doctor, Patient, Auth)
        │   │   ├── dto/          # Data Transfer Objects & form validation models
        │   │   ├── entity/       # JPA entities (User, Appointment, MedicalRecord, etc.)
        │   │   ├── repository/   # Spring Data JPA repositories
        │   │   ├── security/     # Spring Security configurations & UserDetailsService
        │   │   └── service/      # Business logic services & implementations
        │   └── resources/
        │       ├── application.properties  # Spring configuration
        │       ├── static/css/   # Custom CSS stylesheets
        │       └── templates/    # Thymeleaf HTML views (admin, doctor, patient, auth)
        └── test/                 # Test suites
```

---

## Environment & Security (.gitignore)

The project includes a `.gitignore` to safeguard personal data and keep the repository clean. The following files are intentionally excluded from Git:

- **Build Outputs**: `target/`, `build/`, `*.jar`
- **Sensitive Local Overrides**: `application-local.properties`, `*.local.properties`, `.env`, `*.env`
- **IDE & Tooling Cache**: `.idea/`, `.vscode/`, `*.iml`, `.settings/`, `.project`, `.classpath`
- **Python Cache**: `__pycache__/`, `*.pyc`
- **OS Files**: `Thumbs.db`, `.DS_Store`

---

## Troubleshooting

1. **MySQL Access Denied (`Access denied for user 'root'@'localhost'`)**:
   - Verify your MySQL password.
   - Create `hms/application-local.properties` with:
     ```properties
     spring.datasource.password=YOUR_PASSWORD
     ```
2. **Port 8080 Already in Use**:
   - Check if another service is using port 8080.
   - Run on another port by appending `--server.port=8081`:
     ```powershell
     .\mvnw.cmd spring-boot:run -Dspring-boot.run.arguments="--server.port=8081"
     ```
3. **Database Connection Refused**:
   - Ensure the MySQL service is running. On Windows, check `Services.msc` -> `MySQL80` (or `MySQL`).
