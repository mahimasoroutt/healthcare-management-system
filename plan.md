# Hospital Management System (HMS) — Antigravity Build Specification

## Project status

This is a **greenfield project**. There is no existing HMS product, application, backend, or codebase to repair or preserve. Build the application from scratch in the current workspace.

Do not ask for an existing codebase. Do not assume files already exist. Do not overwrite unrelated workspace files. Inspect the workspace only to determine a safe project location, then create the complete application.

## 1. Mission

Build a functional, secure, responsive Hospital Management System for three roles:

- **Admin:** manages users, appointments, system settings, and operational analytics.
- **Doctor:** manages their schedule, appointments, authorized patient records, medical records, and relevant feedback.
- **Patient:** books appointments, manages their profile, views their appointments, and accesses their own medical history.

This is a working full-stack application, not a static mockup. All core workflows must connect to a real backend and database. Do not claim a feature works unless it is implemented and tested.

## 2. Resolve the technology-stack ambiguity first

The supplied requirements specify Java, Spring Boot, Spring Data JPA/Hibernate, MySQL, HTML/CSS/Thymeleaf, and Maven. The project instruction also says to use **uv, not pip**.

`uv` is a Python project/dependency manager; it does not replace Maven or manage Java dependencies. Do not silently mix incompatible stacks or use `uv` as a substitute for Maven.

Use the following decision rule:

1. **If Java/Spring Boot is mandatory for the course or evaluator:** use Java + Spring Boot + Maven for the HMS backend, with Thymeleaf and MySQL as specified. Do not use pip. If a Python utility is genuinely needed, manage that separate utility with `uv` and `pyproject.toml`; do not add a Python backend unnecessarily.
2. **If the user has explicitly changed the backend to Python and wants `uv`:** use Python + FastAPI (or another justified Python web framework), SQLAlchemy, Alembic, MySQL, server-rendered Jinja2 templates or a clearly justified frontend, and manage Python dependencies exclusively with `uv`. Do not use pip commands. In that case, explain that this deviates from the original Java/Spring Boot requirements.

Before implementation, check the available workspace and development environment. If the required backend choice is still ambiguous, ask one concise question: **“Does your evaluator require Java/Spring Boot, or are you switching the backend to Python with uv?”** Do not build the wrong stack based on an assumption.

## 3. Greenfield project initialization

Once the backend choice is confirmed, create a complete project in the current workspace.

### If Java/Spring Boot is selected

Create a Maven project with:
- Java
- Spring Boot
- Spring MVC
- Spring Security
- Spring Data JPA
- Hibernate
- MySQL Connector/J
- Thymeleaf
- Bean Validation
- Maven Wrapper where practical

Create a coherent package structure for configuration, controllers, DTOs/forms, entities, repositories, services, exceptions, and security.

### If Python + uv is selected

Initialize a Python project using `uv init` and manage dependencies with `uv add` / `uv sync`. Use `pyproject.toml` and `uv.lock`. **Never use `pip install`, `python -m pip`, or requirements-only workflows.**

A reasonable starting stack is:
- Python
- FastAPI
- SQLAlchemy 2.x
- Alembic migrations
- MySQL driver compatible with SQLAlchemy
- Jinja2 templates for server-rendered pages, unless a different frontend is explicitly justified
- Pydantic validation
- A secure session/authentication approach
- Pytest for tests

Keep `uv.lock` committed. Document commands using `uv run` (for example, `uv run pytest` and the chosen server command).

Create all required application files, templates, styles, tests, database migrations, `.gitignore`, `.env.example`, README, and deployment configuration. Do not delete unrelated workspace files.

## 4. Required features

### A. Authentication and registration

- Register with name, email, and password.
- Log in using email and password.
- Hash passwords securely; never store plaintext passwords.
- Log out and invalidate the session correctly.
- Redirect each authenticated role to its correct dashboard.
- Validate inputs on the server and show useful errors.
- Protect routes and data with server-side authorization.

Roles:
- `PATIENT`
- `DOCTOR`
- `ADMIN`

Public registration must create Patient accounts by default. Doctor and Admin accounts must be created or authorized by an Admin. Never trust a role submitted by a public registration form.

### B. Admin dashboard

**Overview**
- Total users, patients, and doctors.
- Today's and upcoming appointments.
- Useful recent activity if supported by persisted data.

**User management**
- List, search, and filter users.
- Add and edit users.
- Assign roles only to authorized administrators.
- Activate/deactivate accounts.
- Handle deletion safely when foreign-key relationships or record history exist; use deactivation when deletion would break integrity.

**Appointment management**
- Display patient, doctor, date/time, and status.
- Filter by date, doctor, and status.
- View details and update permitted statuses.
- Persist changes in the database.

**System settings**
- Hospital/clinic name.
- Appointment duration.
- Booking window and other reasonable settings.
- Restrict settings changes to Admin.

**Performance analytics**
- Appointment trends and status distribution.
- Patient and doctor counts.
- Date-range filters.
- Metrics must come from database queries. Show an honest empty state when there is no data. Never invent numbers.

### C. Doctor dashboard

- Today's and upcoming appointments.
- Appointment history.
- Doctor availability and schedule management.
- View assigned/relevant patient records only.
- Create and update medical records within the project's scope.
- View feedback linked to that doctor.

Prevent overlapping schedules and appointment conflicts. A doctor must not be able to access unrelated patient records by changing a URL or record ID.

### D. Patient dashboard

- Book an appointment with a doctor.
- Select a date and genuinely available time slot.
- View booking confirmation.
- View upcoming and past appointments.
- Cancel appointments only when permitted by the rules.
- View their own medical history.
- View and edit allowed profile fields.
- View doctor and appointment details.
- Submit feedback for eligible appointments, if implemented.

Patients must never be able to view another patient's profile, appointments, feedback, or medical records.

### E. Interface states

Implement meaningful:
- Empty states
- Loading indicators where relevant
- Field-level validation errors
- Success and failure messages
- Access-denied and not-found pages
- Confirmation dialogs for destructive actions
- Responsive navigation
- Database and server error handling

Every visible button, link, form, filter, and menu item must work. Remove or clearly disable anything that is not implemented.

## 5. Database requirements

Use MySQL with the requested database name:

`hospital_managment`

Preserve this spelling because it is part of the supplied requirement. Do not silently rename it.

Create suitable entities/tables and relationships for:

### Users
- ID
- Name
- Unique email
- Password hash
- Role
- Enabled status
- Created/updated timestamps

### Doctor schedules
- ID
- Doctor reference
- Day of week or specific schedule date
- Start time
- End time
- Active status

### Appointments
- ID
- Patient reference
- Doctor reference
- Start and end timestamps
- Status
- Optional reason for visit
- Created timestamp

### Medical records
- ID
- Patient reference
- Doctor reference
- Optional appointment reference
- Relevant medical information
- Created/updated timestamps

### Patient feedback
- ID
- Patient reference
- Doctor reference
- Appointment reference
- Rating
- Comment
- Created timestamp

### System settings
- ID
- Unique setting key
- Setting value
- Updated timestamp
- Updating administrator

Add appropriate foreign keys, indexes, unique constraints, validation, and transaction handling. Prevent orphaned records. Use migrations or a documented schema initialization process; do not rely on undocumented manual database edits.

## 6. Appointment booking correctness

Appointment booking must be enforced by the backend, not merely by the UI.

1. Display only slots derived from doctor schedules and existing appointments.
2. Revalidate availability when the patient submits the booking.
3. Reject appointments outside the doctor's availability.
4. Reject overlapping appointments for the same doctor.
5. Apply sensible cancellation and status-transition rules.
6. Handle concurrent booking attempts safely using suitable transactions and database constraints/locking where needed.
7. Return a useful error and refresh availability if another user books the slot first.

## 7. Visual direction

Create a calm, trustworthy, practical hospital operations interface. It should look designed for real administrative, clinical, and patient tasks—not like a generic AI-generated SaaS dashboard.

### Design references

Study these references for ideas; do not copy an entire design blindly.

- Healthcare dashboard inspiration: https://dribbble.com/search/healthcare-dashboard
- Healthcare design case studies: https://www.behance.net/search/projects?search=healthcare%20dashboard
- Bootstrap components and layout: https://getbootstrap.com/docs/5.3/
- Flowbite component patterns: https://flowbite.com/blocks/
- Lucide icons: https://lucide.dev/icons/
- Bootstrap Icons: https://icons.getbootstrap.com/
- Inter font: https://fonts.google.com/specimen/Inter
- Source Sans 3 font: https://fonts.google.com/specimen/Source+Sans+3
- WCAG contrast checker: https://webaim.org/resources/contrastchecker/

Use one coherent component and icon system. If using Thymeleaf, Bootstrap 5 is a practical default. If using another templating approach, preserve the same design principles and explain the choice.

### Suggested design tokens

- Primary: `#153B50`
- Accent: `#187C80`
- Page background: `#F5F7F8`
- Surface: `#FFFFFF`
- Main text: `#26343D`
- Secondary text: `#647580`

Use Inter or Source Sans 3 consistently. Use a 4px/8px spacing scale, restrained shadows, subtle borders, moderate corner radii, and accessible contrast. Adjust tokens only when the result is more coherent and readable.

## 8. Strict anti-AI-design rules

These are mandatory design constraints.

1. **No generic AI visual recipe.** Avoid pervasive purple-blue gradients, glowing orbs, floating 3D objects, decorative blobs, and glassmorphism everywhere.
2. **No repetitive card grids.** Do not make every section three rounded cards. Use tables for administrative records, schedule/calendar or list views for appointments, timelines/lists for medical history, and forms for editing.
3. **No generic marketing copy.** This is an application, not a landing page. Use concise labels such as “Book appointment”, “Today's appointments”, and “No appointments scheduled for this date”.
4. **No excessive pill shapes.** Not every button, badge, or container needs fully rounded corners. Keep the interface structured and readable.
5. **No unnecessary animations.** Avoid scroll-reveal effects everywhere, custom cursors, floating elements, and animated counters. Use subtle interaction feedback only when useful.
6. **No fabricated authenticity.** Do not invent hospital accreditations, doctor credentials, patient testimonials, operational metrics, or real-world claims.
7. **No identical dashboards.** Admin focuses on operations, Doctor on schedules and authorized clinical work, and Patient on bookings and personal records. Their information hierarchy and actions must be genuinely different.
8. **No fake functionality.** Do not make controls appear functional when they are not connected to a real action. Never display a fake successful save.
9. **Use domain-specific content.** Use realistic fictional names, appointment statuses, dates, and schedules for demo data, and identify them as demo records.
10. **Make every layout earn its place.** Avoid excessive whitespace, oversized headings, and decorative sections that do not help the task.
11. **Use icons consistently.** Prefer one coherent SVG icon family; do not use emoji as interface icons.
12. **Design for accessibility.** Use semantic markup, associated form labels, keyboard navigation, visible focus states, responsive behavior, and appropriate contrast.

The goal is not to hide the use of AI. The goal is to produce specific, coherent, credible design decisions instead of default template output.

## 9. Security and privacy

- Enforce authorization on the server and in service/business logic.
- Do not rely only on hidden navigation links or disabled buttons.
- Verify record ownership for every patient-specific operation.
- Verify doctor-patient/appointment relationships before exposing clinical records.
- Use secure password hashing and session handling.
- Protect against CSRF where applicable.
- Validate and normalize user inputs.
- Avoid exposing stack traces or sensitive data to users.
- Do not log passwords, session tokens, or sensitive clinical notes.
- Never commit database passwords, secret keys, or credentials.
- Use fictional data only; this is a college/demo project, not a production clinical system.
- Do not claim legal or regulatory compliance without a real compliance review.

## 10. Testing and acceptance criteria

Create automated tests appropriate to the chosen stack.

At minimum, verify:
- Registration and login.
- Passwords are stored as hashes.
- Correct role-based dashboard routing.
- Unauthenticated access is blocked.
- Cross-role access is rejected.
- Patients cannot access another patient's records by changing IDs.
- Doctors cannot access unrelated clinical records.
- User and appointment CRUD operations persist.
- Booking rejects unavailable or overlapping slots.
- Medical records persist and have the correct owner/author.
- Validation errors are shown appropriately.
- Analytics are derived from database data.
- The app starts from documented commands.
- The build and tests pass, or remaining failures are clearly reported.

Do not claim tests passed unless they were actually run.

## 11. Build sequence

Implement the application in verified stages:

1. Confirm the backend stack and inspect the workspace.
2. Initialize the project from scratch.
3. Configure database connectivity and migrations/schema.
4. Implement entities, repositories, services, and validation.
5. Implement authentication, authorization, and role routing.
6. Establish the design tokens, shared layout, navigation, and reusable components.
7. Implement patient profile and appointment booking.
8. Implement doctor schedules, appointments, and medical records.
9. Implement admin user/appointment management, settings, and analytics.
10. Implement feedback and all relevant empty/error states.
11. Add tests, demo seed data, responsive styling, and accessibility checks.
12. Document setup and deployment.
13. Run the available build/tests, fix issues introduced by the implementation, and summarize verified results.

Do not stop after creating a skeleton or a visually attractive first page. Continue through the core workflows.

## 12. Environment and deployment

Create `.env.example` containing placeholder variable names only. Do not include actual credentials.

For Java/Spring Boot, document Maven commands and configure database properties using environment variables.

For Python, manage the project exclusively with `uv`; document setup using commands such as `uv sync` and execution/testing using `uv run`. Do not use pip.

Prepare GitHub-ready configuration and Render deployment files appropriate to the selected stack. Do not assume Render provides a persistent MySQL database automatically. Document the external managed database and environment variables needed.

## 13. Final deliverables

The finished workspace must contain:
- Complete source code
- Database schema/migrations
- Functional role-specific pages
- Shared styles and components
- Automated tests
- Demo-data setup
- `.gitignore`
- `.env.example`
- README with setup, run, test, and deployment instructions
- Deployment configuration where feasible

At completion, report:
1. What was created.
2. The selected stack and why.
3. Main routes and role capabilities.
4. Database setup instructions.
5. Commands to run and test the application.
6. Tests actually executed and their results.
7. Known limitations or unverified deployment steps.

**Start from scratch. Build the real application, not a mockup. Do not silently choose a backend that conflicts with the course requirements.**
