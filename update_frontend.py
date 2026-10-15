import os

base_dir = "hms/src/main/resources"
templates_dir = os.path.join(base_dir, "templates")
static_css = os.path.join(base_dir, "static", "css")
os.makedirs(static_css, exist_ok=True)

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)

css_content = """
:root {
    --primary-color: #153B50;
    --accent-color: #187C80;
    --bg-color: #F5F7F8;
    --surface-color: #FFFFFF;
    --main-text: #26343D;
    --sec-text: #647580;
    --border-color: #E2E8F0;
}

body {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-color);
    color: var(--main-text);
    -webkit-font-smoothing: antialiased;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    color: var(--primary-color);
    font-weight: 600;
}

/* Navbar */
.navbar-custom {
    background-color: var(--primary-color);
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.navbar-custom .navbar-brand {
    color: #ffffff;
    font-weight: 600;
    letter-spacing: 0.5px;
}
.navbar-custom .nav-link {
    color: rgba(255, 255, 255, 0.85);
    font-weight: 500;
}
.navbar-custom .nav-link:hover, .navbar-custom .nav-link.active {
    color: #ffffff;
}

/* Cards & Surfaces */
.card {
    background-color: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}
.card-header {
    background-color: var(--surface-color);
    border-bottom: 1px solid var(--border-color);
    font-weight: 600;
    color: var(--primary-color);
}

/* Buttons */
.btn-primary {
    background-color: var(--accent-color);
    border-color: var(--accent-color);
    border-radius: 4px;
    font-weight: 500;
}
.btn-primary:hover {
    background-color: #136265;
    border-color: #136265;
}
.btn-outline-primary {
    color: var(--accent-color);
    border-color: var(--accent-color);
}
.btn-outline-primary:hover {
    background-color: var(--accent-color);
    color: #ffffff;
}

/* Tables */
.table {
    color: var(--main-text);
}
.table thead th {
    border-bottom: 2px solid var(--border-color);
    color: var(--sec-text);
    font-weight: 600;
    font-size: 0.85rem;
    text-transform: uppercase;
}
.table td {
    vertical-align: middle;
    border-bottom: 1px solid var(--border-color);
}

/* Layout */
.page-title {
    margin-bottom: 1.5rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--border-color);
}

.empty-state {
    padding: 3rem 1rem;
    text-align: center;
    color: var(--sec-text);
    background-color: #f8fafc;
    border: 1px dashed var(--border-color);
    border-radius: 6px;
}
.empty-state i {
    font-size: 2.5rem;
    color: #cbd5e1;
    margin-bottom: 1rem;
}
"""
write_file(os.path.join(static_css, "style.css"), css_content)

layout_content = """<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org" xmlns:sec="http://www.thymeleaf.org/extras/spring-security">
<head th:fragment="head(title)">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title th:text="${title} + ' - HMS'">HMS</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    <link rel="stylesheet" th:href="@{/css/style.css}">
</head>
<body>

<nav th:fragment="navbar" class="navbar navbar-expand-lg navbar-custom sticky-top mb-4">
  <div class="container-fluid px-4">
    <a class="navbar-brand" href="#"><i class="bi bi-hospital"></i> HMS</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav me-auto">
        <li class="nav-item" sec:authorize="hasRole('ADMIN')">
          <a class="nav-link" th:href="@{/admin/dashboard}"><i class="bi bi-speedometer2"></i> Dashboard</a>
        </li>
        <li class="nav-item" sec:authorize="hasRole('DOCTOR')">
          <a class="nav-link" th:href="@{/doctor/dashboard}"><i class="bi bi-calendar3"></i> Schedule</a>
        </li>
        <li class="nav-item" sec:authorize="hasRole('PATIENT')">
          <a class="nav-link" th:href="@{/patient/dashboard}"><i class="bi bi-house"></i> Overview</a>
        </li>
      </ul>
      <ul class="navbar-nav align-items-center">
        <li class="nav-item me-3" sec:authorize="isAuthenticated()">
            <span class="nav-link text-white-50"><i class="bi bi-person-circle"></i> <span sec:authentication="name"></span></span>
        </li>
        <li class="nav-item" sec:authorize="isAuthenticated()">
            <form th:action="@{/logout}" method="post" class="m-0">
                <button type="submit" class="btn btn-sm btn-outline-light">Sign Out</button>
            </form>
        </li>
      </ul>
    </div>
  </div>
</nav>

<footer th:fragment="footer" class="mt-auto py-3 bg-white border-top">
    <div class="container text-center">
        <small class="text-muted">&copy; 2026 Hospital Management System. Restricted Access.</small>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</footer>

</body>
</html>
"""
write_file(os.path.join(templates_dir, "fragments", "layout.html"), layout_content)

admin_dashboard = """<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head th:replace="~{fragments/layout :: head('Admin Dashboard')}"></head>
<body class="d-flex flex-column min-vh-100">
<div th:replace="~{fragments/layout :: navbar}"></div>

<div class="container-fluid px-4 mb-5">
    <div class="page-title d-flex justify-content-between align-items-center">
        <h2 class="mb-0">Administrative Overview</h2>
        <button class="btn btn-primary"><i class="bi bi-plus-lg"></i> Register Staff</button>
    </div>

    <div class="row g-4 mb-4">
        <!-- Key Metrics -->
        <div class="col-md-3">
            <div class="card h-100 border-0 shadow-sm">
                <div class="card-body">
                    <h6 class="text-muted text-uppercase mb-2">Total Patients</h6>
                    <h3 class="mb-0">1,248</h3>
                    <small class="text-success"><i class="bi bi-arrow-up"></i> 12 this week</small>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card h-100 border-0 shadow-sm">
                <div class="card-body">
                    <h6 class="text-muted text-uppercase mb-2">Active Doctors</h6>
                    <h3 class="mb-0">45</h3>
                    <small class="text-muted">Across 8 departments</small>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card h-100 border-0 shadow-sm">
                <div class="card-body">
                    <h6 class="text-muted text-uppercase mb-2">Today's Appointments</h6>
                    <h3 class="mb-0">112</h3>
                    <small class="text-warning"><i class="bi bi-clock"></i> 34 pending</small>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card h-100 border-0 shadow-sm">
                <div class="card-body">
                    <h6 class="text-muted text-uppercase mb-2">System Status</h6>
                    <h3 class="mb-0 text-success">Healthy</h3>
                    <small class="text-muted">Last backup: 2h ago</small>
                </div>
            </div>
        </div>
    </div>

    <div class="row">
        <!-- Recent Users Table -->
        <div class="col-lg-8">
            <div class="card h-100 shadow-sm">
                <div class="card-header bg-white d-flex justify-content-between align-items-center py-3">
                    <h5 class="mb-0">Recent User Registrations</h5>
                    <a href="#" class="btn btn-sm btn-outline-secondary">View All Users</a>
                </div>
                <div class="card-body p-0">
                    <div class="table-responsive">
                        <table class="table table-hover mb-0">
                            <thead class="table-light">
                                <tr>
                                    <th class="ps-4">Name</th>
                                    <th>Email</th>
                                    <th>Role</th>
                                    <th>Status</th>
                                    <th class="text-end pe-4">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td class="ps-4">John Doe</td>
                                    <td>john@example.com</td>
                                    <td><span class="badge bg-secondary">PATIENT</span></td>
                                    <td><span class="badge bg-success">Active</span></td>
                                    <td class="text-end pe-4">
                                        <button class="btn btn-sm btn-light border"><i class="bi bi-pencil"></i></button>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="ps-4">Dr. Sarah Smith</td>
                                    <td>sarah.s@hospital.com</td>
                                    <td><span class="badge bg-primary">DOCTOR</span></td>
                                    <td><span class="badge bg-success">Active</span></td>
                                    <td class="text-end pe-4">
                                        <button class="btn btn-sm btn-light border"><i class="bi bi-pencil"></i></button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- System Settings Quick Access -->
        <div class="col-lg-4">
            <div class="card h-100 shadow-sm">
                <div class="card-header bg-white py-3">
                    <h5 class="mb-0">System Configuration</h5>
                </div>
                <div class="card-body">
                    <div class="list-group list-group-flush">
                        <a href="#" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="mb-1">Clinic Operating Hours</h6>
                                <small class="text-muted">08:00 AM - 08:00 PM</small>
                            </div>
                            <i class="bi bi-chevron-right text-muted"></i>
                        </a>
                        <a href="#" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="mb-1">Appointment Duration</h6>
                                <small class="text-muted">Default: 30 minutes</small>
                            </div>
                            <i class="bi bi-chevron-right text-muted"></i>
                        </a>
                        <a href="#" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="mb-1">Booking Window</h6>
                                <small class="text-muted">Max 60 days advance</small>
                            </div>
                            <i class="bi bi-chevron-right text-muted"></i>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<div th:replace="~{fragments/layout :: footer}"></div>
</body>
</html>
"""
write_file(os.path.join(templates_dir, "admin", "dashboard.html"), admin_dashboard)

doctor_dashboard = """<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head th:replace="~{fragments/layout :: head('Doctor Dashboard')}"></head>
<body class="d-flex flex-column min-vh-100">
<div th:replace="~{fragments/layout :: navbar}"></div>

<div class="container mb-5">
    <div class="page-title">
        <h2 class="mb-0">Doctor Schedule</h2>
        <p class="text-muted mb-0">Manage your availability and clinical appointments.</p>
    </div>

    <div class="row">
        <!-- Today's Schedule -->
        <div class="col-lg-8">
            <div class="card shadow-sm mb-4">
                <div class="card-header bg-white py-3 d-flex justify-content-between align-items-center">
                    <h5 class="mb-0">Today's Appointments</h5>
                    <span class="text-muted small" th:text="${#calendars.format(#calendars.createNow(), 'EEEE, MMMM dd, yyyy')}">Date</span>
                </div>
                <div class="card-body p-0">
                    <!-- Placeholder Empty State -->
                    <div class="empty-state">
                        <i class="bi bi-calendar-x"></i>
                        <h5>No appointments scheduled for today.</h5>
                        <p>Enjoy your break or check upcoming days.</p>
                    </div>
                </div>
            </div>
            
            <div class="card shadow-sm">
                <div class="card-header bg-white py-3">
                    <h5 class="mb-0">Recent Patient Records</h5>
                </div>
                <div class="card-body p-0">
                     <div class="empty-state">
                        <i class="bi bi-file-earmark-medical"></i>
                        <h5>No recent clinical records.</h5>
                        <p>Records you create will appear here.</p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Manage Availability -->
        <div class="col-lg-4">
            <div class="card shadow-sm">
                <div class="card-header bg-white py-3">
                    <h5 class="mb-0">Weekly Availability</h5>
                </div>
                <div class="card-body">
                    <p class="text-muted small mb-3">Set your standard working hours for appointment booking.</p>
                    <form>
                        <div class="mb-3 d-flex align-items-center justify-content-between">
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" id="mon" checked>
                                <label class="form-check-label" for="mon">Monday</label>
                            </div>
                            <div class="text-muted small">09:00 - 17:00</div>
                        </div>
                        <div class="mb-3 d-flex align-items-center justify-content-between">
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" id="tue" checked>
                                <label class="form-check-label" for="tue">Tuesday</label>
                            </div>
                            <div class="text-muted small">09:00 - 17:00</div>
                        </div>
                        <div class="mb-3 d-flex align-items-center justify-content-between">
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" id="wed" checked>
                                <label class="form-check-label" for="wed">Wednesday</label>
                            </div>
                            <div class="text-muted small">09:00 - 17:00</div>
                        </div>
                        <hr>
                        <button type="button" class="btn btn-outline-primary w-100">Update Schedule</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>

<div th:replace="~{fragments/layout :: footer}"></div>
</body>
</html>
"""
write_file(os.path.join(templates_dir, "doctor", "dashboard.html"), doctor_dashboard)

patient_dashboard = """<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head th:replace="~{fragments/layout :: head('Patient Dashboard')}"></head>
<body class="d-flex flex-column min-vh-100">
<div th:replace="~{fragments/layout :: navbar}"></div>

<div class="container mb-5">
    <div class="page-title d-flex justify-content-between align-items-center">
        <div>
            <h2 class="mb-0">My Dashboard</h2>
            <p class="text-muted mb-0">Manage your healthcare appointments and records.</p>
        </div>
        <a href="#" class="btn btn-primary"><i class="bi bi-calendar-plus"></i> Book Appointment</a>
    </div>

    <div class="row g-4">
        <div class="col-lg-8">
            <div class="card shadow-sm mb-4">
                <div class="card-header bg-white py-3">
                    <h5 class="mb-0">Upcoming Appointments</h5>
                </div>
                <div class="card-body p-0">
                    <div class="empty-state">
                        <i class="bi bi-calendar2-check"></i>
                        <h5>No upcoming appointments</h5>
                        <p>You have no scheduled visits at the moment.</p>
                        <button class="btn btn-outline-primary mt-2">Book a Session</button>
                    </div>
                </div>
            </div>
            
            <div class="card shadow-sm">
                <div class="card-header bg-white py-3">
                    <h5 class="mb-0">Medical History</h5>
                </div>
                <div class="card-body p-0">
                    <div class="empty-state">
                        <i class="bi bi-clipboard2-pulse"></i>
                        <h5>No medical records found</h5>
                        <p>Your clinical history will appear here after a consultation.</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-lg-4">
            <div class="card shadow-sm">
                <div class="card-header bg-white py-3">
                    <h5 class="mb-0">Profile Summary</h5>
                </div>
                <div class="card-body text-center pt-4">
                    <div class="display-1 text-muted mb-3"><i class="bi bi-person-circle"></i></div>
                    <h5 class="mb-1" sec:authentication="name">Patient Name</h5>
                    <p class="text-muted small">Registered Patient</p>
                    <hr>
                    <ul class="list-unstyled text-start mb-0">
                        <li class="mb-2"><i class="bi bi-envelope text-muted me-2"></i> <span sec:authentication="name"></span></li>
                        <li class="mb-2"><i class="bi bi-telephone text-muted me-2"></i> Update required</li>
                        <li><i class="bi bi-geo-alt text-muted me-2"></i> Update required</li>
                    </ul>
                    <button class="btn btn-sm btn-light border w-100 mt-3">Edit Profile</button>
                </div>
            </div>
        </div>
    </div>
</div>

<div th:replace="~{fragments/layout :: footer}"></div>
</body>
</html>
"""
write_file(os.path.join(templates_dir, "patient", "dashboard.html"), patient_dashboard)

auth_login = """<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head th:replace="~{fragments/layout :: head('Login')}"></head>
<body class="d-flex align-items-center py-4 bg-body-tertiary h-100" style="min-height: 100vh;">
    
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-5 col-lg-4">
            <div class="text-center mb-4">
                <i class="bi bi-hospital fs-1" style="color: var(--primary-color);"></i>
                <h2 class="h3 mb-3 fw-bold mt-2" style="color: var(--primary-color);">Hospital Portal</h2>
            </div>
            <div class="card border-0 shadow-sm p-4">
                <p class="text-muted text-center mb-4">Sign in to your account</p>

                <div th:if="${param.error}" class="alert alert-danger p-2 small text-center">
                    Invalid email or password.
                </div>
                <div th:if="${param.logout}" class="alert alert-success p-2 small text-center">
                    You have been securely logged out.
                </div>

                <form th:action="@{/login}" method="post">
                    <div class="mb-3">
                        <label for="username" class="form-label small fw-semibold text-muted">Email address</label>
                        <input type="email" class="form-control" id="username" name="username" placeholder="name@example.com" required autofocus>
                    </div>
                    <div class="mb-4">
                        <label for="password" class="form-label small fw-semibold text-muted">Password</label>
                        <input type="password" class="form-control" id="password" name="password" placeholder="Enter password" required>
                    </div>
                    
                    <button class="btn btn-primary w-100 py-2 mb-3" type="submit">Sign In</button>
                </form>
            </div>
            <div class="text-center mt-4">
                <span class="text-muted small">New patient?</span> <a th:href="@{/register}" class="text-decoration-none fw-semibold">Register here</a>
            </div>
        </div>
    </div>
</div>

</body>
</html>
"""
write_file(os.path.join(templates_dir, "auth", "login.html"), auth_login)

auth_register = """<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head th:replace="~{fragments/layout :: head('Register')}"></head>
<body class="d-flex align-items-center py-4 bg-body-tertiary h-100" style="min-height: 100vh;">
    
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
            <div class="text-center mb-4">
                <i class="bi bi-clipboard2-heart fs-1" style="color: var(--primary-color);"></i>
                <h2 class="h3 mb-3 fw-bold mt-2" style="color: var(--primary-color);">Patient Registration</h2>
            </div>
            
            <div class="card border-0 shadow-sm p-4">
                <div th:if="${param.success}" class="alert alert-success text-center">
                    Registration successful! <a th:href="@{/login}" class="alert-link">Login here</a>.
                </div>

                <form th:action="@{/register}" th:object="${user}" method="post">
                    <div class="mb-3">
                        <label for="name" class="form-label small fw-semibold text-muted">Full Legal Name</label>
                        <input type="text" class="form-control" id="name" th:field="*{name}">
                        <div class="text-danger small mt-1" th:if="${#fields.hasErrors('name')}" th:errors="*{name}"></div>
                    </div>
                    <div class="mb-3">
                        <label for="email" class="form-label small fw-semibold text-muted">Email Address</label>
                        <input type="email" class="form-control" id="email" th:field="*{email}">
                        <div class="text-danger small mt-1" th:if="${#fields.hasErrors('email')}" th:errors="*{email}"></div>
                    </div>
                    <div class="mb-4">
                        <label for="password" class="form-label small fw-semibold text-muted">Password</label>
                        <input type="password" class="form-control" id="password" th:field="*{password}">
                        <div class="text-danger small mt-1" th:if="${#fields.hasErrors('password')}" th:errors="*{password}"></div>
                        <div class="form-text small">Ensure your password is at least 8 characters.</div>
                    </div>
                    
                    <button class="btn btn-primary w-100 py-2 mb-3" type="submit">Create Account</button>
                </form>
            </div>
            <div class="text-center mt-4">
                <span class="text-muted small">Already have an account?</span> <a th:href="@{/login}" class="text-decoration-none fw-semibold">Sign in</a>
            </div>
        </div>
    </div>
</div>

</body>
</html>
"""
write_file(os.path.join(templates_dir, "auth", "register.html"), auth_register)

print("Frontend templates significantly improved.")
