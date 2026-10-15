import os

base_dir = "hms/src/main/resources/templates"

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)

templates = {
    "fragments/layout.html": """<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org" xmlns:sec="http://www.thymeleaf.org/extras/spring-security">
<head th:fragment="head(title)">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title th:text="${title} + ' - HMS'">HMS</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    <style>
        :root {
            --primary-color: #153B50;
            --accent-color: #187C80;
            --bg-color: #F5F7F8;
            --surface-color: #FFFFFF;
            --main-text: #26343D;
            --sec-text: #647580;
        }
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--main-text);
        }
        .navbar-custom {
            background-color: var(--primary-color);
        }
        .navbar-custom .navbar-brand, .navbar-custom .nav-link {
            color: #ffffff;
        }
        .btn-primary {
            background-color: var(--accent-color);
            border-color: var(--accent-color);
        }
        .btn-primary:hover {
            background-color: #136265;
            border-color: #136265;
        }
        .card {
            border: none;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            border-radius: 8px;
        }
    </style>
</head>
<body>

<nav th:fragment="navbar" class="navbar navbar-expand-lg navbar-custom mb-4">
  <div class="container">
    <a class="navbar-brand" href="#">HMS Admin/Portal</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav me-auto">
        <li class="nav-item" sec:authorize="hasRole('ADMIN')">
          <a class="nav-link" th:href="@{/admin/dashboard}">Dashboard</a>
        </li>
        <li class="nav-item" sec:authorize="hasRole('DOCTOR')">
          <a class="nav-link" th:href="@{/doctor/dashboard}">Dashboard</a>
        </li>
        <li class="nav-item" sec:authorize="hasRole('PATIENT')">
          <a class="nav-link" th:href="@{/patient/dashboard}">Dashboard</a>
        </li>
      </ul>
      <ul class="navbar-nav">
        <li class="nav-item" sec:authorize="isAuthenticated()">
            <span class="nav-link"><i class="bi bi-person-circle"></i> <span sec:authentication="name"></span></span>
        </li>
        <li class="nav-item" sec:authorize="isAuthenticated()">
            <form th:action="@{/logout}" method="post" class="d-inline">
                <button type="submit" class="btn btn-link nav-link text-white">Logout</button>
            </form>
        </li>
      </ul>
    </div>
  </div>
</nav>

<footer th:fragment="footer" class="mt-5 py-4 text-center text-muted">
    <div class="container">
        <small>&copy; 2026 Hospital Management System.</small>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</footer>

</body>
</html>
""",

    "auth/login.html": """<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head th:replace="~{fragments/layout :: head('Login')}"></head>
<body class="d-flex align-items-center py-4 bg-body-tertiary h-100" style="min-height: 100vh;">
    
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-5">
            <div class="card p-4">
                <div class="text-center mb-4">
                    <h2 class="h3 mb-3 fw-normal" style="color: var(--primary-color);">Hospital Management System</h2>
                    <p class="text-muted">Please sign in to your account</p>
                </div>

                <div th:if="${param.error}" class="alert alert-danger">
                    Invalid email or password.
                </div>
                <div th:if="${param.logout}" class="alert alert-success">
                    You have been logged out.
                </div>

                <form th:action="@{/login}" method="post">
                    <div class="form-floating mb-3">
                        <input type="email" class="form-control" id="username" name="username" placeholder="name@example.com" required>
                        <label for="username">Email address</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input type="password" class="form-control" id="password" name="password" placeholder="Password" required>
                        <label for="password">Password</label>
                    </div>
                    
                    <button class="btn btn-primary w-100 py-2 mb-3" type="submit">Sign in</button>
                    <div class="text-center">
                        <a th:href="@{/register}" class="text-decoration-none">Create new patient account</a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>

</body>
</html>
""",

    "auth/register.html": """<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head th:replace="~{fragments/layout :: head('Register')}"></head>
<body class="d-flex align-items-center py-4 bg-body-tertiary h-100" style="min-height: 100vh;">
    
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-5">
            <div class="card p-4">
                <div class="text-center mb-4">
                    <h2 class="h3 mb-3 fw-normal" style="color: var(--primary-color);">Patient Registration</h2>
                </div>

                <div th:if="${param.success}" class="alert alert-success">
                    Registration successful! <a th:href="@{/login}">Login here</a>.
                </div>

                <form th:action="@{/register}" th:object="${user}" method="post">
                    <div class="mb-3">
                        <label for="name" class="form-label">Full Name</label>
                        <input type="text" class="form-control" id="name" th:field="*{name}">
                        <div class="text-danger" th:if="${#fields.hasErrors('name')}" th:errors="*{name}"></div>
                    </div>
                    <div class="mb-3">
                        <label for="email" class="form-label">Email address</label>
                        <input type="email" class="form-control" id="email" th:field="*{email}">
                        <div class="text-danger" th:if="${#fields.hasErrors('email')}" th:errors="*{email}"></div>
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input type="password" class="form-control" id="password" th:field="*{password}">
                        <div class="text-danger" th:if="${#fields.hasErrors('password')}" th:errors="*{password}"></div>
                    </div>
                    
                    <button class="btn btn-primary w-100 py-2 mb-3" type="submit">Register</button>
                    <div class="text-center">
                        <a th:href="@{/login}" class="text-decoration-none">Already have an account? Sign in</a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>

</body>
</html>
""",

    "admin/dashboard.html": """<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head th:replace="~{fragments/layout :: head('Admin Dashboard')}"></head>
<body>
<div th:replace="~{fragments/layout :: navbar}"></div>

<div class="container">
    <h2 class="mb-4">Admin Dashboard</h2>
    <div class="row">
        <div class="col-md-4 mb-4">
            <div class="card p-4 text-center">
                <i class="bi bi-people fs-1 text-primary mb-2"></i>
                <h3 class="h5">Manage Users</h3>
                <p class="text-muted small">View, add, or edit system users</p>
                <a href="#" class="btn btn-outline-primary mt-2">Go to Users</a>
            </div>
        </div>
        <div class="col-md-4 mb-4">
            <div class="card p-4 text-center">
                <i class="bi bi-calendar-check fs-1 text-primary mb-2"></i>
                <h3 class="h5">Appointments</h3>
                <p class="text-muted small">Overview of hospital appointments</p>
                <a href="#" class="btn btn-outline-primary mt-2">Go to Appointments</a>
            </div>
        </div>
        <div class="col-md-4 mb-4">
            <div class="card p-4 text-center">
                <i class="bi bi-gear fs-1 text-primary mb-2"></i>
                <h3 class="h5">System Settings</h3>
                <p class="text-muted small">Configure global settings</p>
                <a href="#" class="btn btn-outline-primary mt-2">Go to Settings</a>
            </div>
        </div>
    </div>
</div>

<div th:replace="~{fragments/layout :: footer}"></div>
</body>
</html>
""",
    "doctor/dashboard.html": """<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head th:replace="~{fragments/layout :: head('Doctor Dashboard')}"></head>
<body>
<div th:replace="~{fragments/layout :: navbar}"></div>

<div class="container">
    <h2 class="mb-4">Doctor Dashboard</h2>
    <p>Welcome, Doctor. Here you will manage your schedule and appointments.</p>
</div>

<div th:replace="~{fragments/layout :: footer}"></div>
</body>
</html>
""",
    "patient/dashboard.html": """<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head th:replace="~{fragments/layout :: head('Patient Dashboard')}"></head>
<body>
<div th:replace="~{fragments/layout :: navbar}"></div>

<div class="container">
    <h2 class="mb-4">Patient Dashboard</h2>
    <p>Welcome. Here you can book appointments and view your medical history.</p>
</div>

<div th:replace="~{fragments/layout :: footer}"></div>
</body>
</html>
"""
}

for name, content in templates.items():
    write_file(os.path.join(base_dir, name), content)

print("Templates generated.")
