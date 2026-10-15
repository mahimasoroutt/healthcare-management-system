import os

base_dir = "hms/src/main/java/com/hospital/hms"
templates_dir = "hms/src/main/resources/templates"

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)

# 1. Admin Controller
admin_controller = """package com.hospital.hms.controller;

import com.hospital.hms.entity.Role;
import com.hospital.hms.entity.User;
import com.hospital.hms.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.List;

@Controller
@RequestMapping("/admin")
public class AdminController {

    @Autowired
    private UserRepository userRepository;
    
    @Autowired
    private PasswordEncoder passwordEncoder;

    @GetMapping("/dashboard")
    public String adminDashboard(Model model) {
        List<User> doctors = userRepository.findByRole(Role.DOCTOR);
        List<User> allUsers = userRepository.findAll();
        
        model.addAttribute("totalPatients", allUsers.stream().filter(u -> u.getRole() == Role.PATIENT).count());
        model.addAttribute("totalDoctors", doctors.size());
        model.addAttribute("users", allUsers);
        
        return "admin/dashboard";
    }
    
    @PostMapping("/register-staff")
    public String registerStaff(@RequestParam("name") String name,
                              @RequestParam("email") String email,
                              @RequestParam("password") String password,
                              @RequestParam("role") String roleStr) {
                              
        if (userRepository.findByEmail(email).isPresent()) {
            return "redirect:/admin/dashboard?error=email_exists";
        }
        
        User user = new User();
        user.setName(name);
        user.setEmail(email);
        user.setPassword(passwordEncoder.encode(password));
        user.setEnabled(true);
        user.setRole(Role.valueOf(roleStr));
        
        userRepository.save(user);
        
        return "redirect:/admin/dashboard?success=staff_registered";
    }
}
"""
write_file(os.path.join(base_dir, "controller", "AdminController.java"), admin_controller)

# Remove the /admin/dashboard mapping from DashboardController to avoid conflicts
dash_controller = """package com.hospital.hms.controller;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class DashboardController {

    @GetMapping("/")
    public String home() {
        return "redirect:/login";
    }

    @GetMapping("/doctor/dashboard")
    public String doctorDashboard() {
        return "doctor/dashboard";
    }
}
"""
write_file(os.path.join(base_dir, "controller", "DashboardController.java"), dash_controller)

# 2. Update Admin Dashboard Template
admin_dashboard = """<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head th:replace="~{fragments/layout :: head('Admin Dashboard')}"></head>
<body class="d-flex flex-column min-vh-100">
<div th:replace="~{fragments/layout :: navbar}"></div>

<div class="container-fluid px-4 mb-5">
    <div class="page-title d-flex justify-content-between align-items-center">
        <h2 class="mb-0">Administrative Overview</h2>
        <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#registerStaffModal">
            <i class="bi bi-plus-lg"></i> Register Staff
        </button>
    </div>
    
    <div th:if="${param.success == 'staff_registered'}" class="alert alert-success alert-dismissible fade show" role="alert">
        <i class="bi bi-check-circle-fill me-2"></i> Staff member successfully registered!
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    <div th:if="${param.error == 'email_exists'}" class="alert alert-danger alert-dismissible fade show" role="alert">
        <i class="bi bi-exclamation-triangle-fill me-2"></i> A user with that email already exists.
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>

    <div class="row g-4 mb-4">
        <!-- Key Metrics -->
        <div class="col-md-3">
            <div class="card h-100 border-0 shadow-sm">
                <div class="card-body">
                    <h6 class="text-muted text-uppercase mb-2">Total Patients</h6>
                    <h3 class="mb-0" th:text="${totalPatients}">0</h3>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card h-100 border-0 shadow-sm">
                <div class="card-body">
                    <h6 class="text-muted text-uppercase mb-2">Active Doctors</h6>
                    <h3 class="mb-0" th:text="${totalDoctors}">0</h3>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card h-100 border-0 shadow-sm">
                <div class="card-body">
                    <h6 class="text-muted text-uppercase mb-2">Today's Appointments</h6>
                    <h3 class="mb-0">0</h3>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card h-100 border-0 shadow-sm">
                <div class="card-body">
                    <h6 class="text-muted text-uppercase mb-2">System Status</h6>
                    <h3 class="mb-0 text-success">Healthy</h3>
                </div>
            </div>
        </div>
    </div>

    <div class="row">
        <!-- All Users Table -->
        <div class="col-lg-8">
            <div class="card h-100 shadow-sm border-0">
                <div class="card-header bg-white d-flex justify-content-between align-items-center py-3">
                    <h5 class="mb-0">System Users</h5>
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
                                </tr>
                            </thead>
                            <tbody>
                                <tr th:each="u : ${users}">
                                    <td class="ps-4 fw-medium" th:text="${u.name}"></td>
                                    <td class="text-muted" th:text="${u.email}"></td>
                                    <td>
                                        <span class="badge" 
                                              th:classappend="${u.role.name() == 'ADMIN' ? 'bg-danger' : (u.role.name() == 'DOCTOR' ? 'bg-primary' : 'bg-secondary')}"
                                              th:text="${u.role}"></span>
                                    </td>
                                    <td><span class="badge bg-success">Active</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- System Settings Quick Access -->
        <div class="col-lg-4">
            <div class="card h-100 shadow-sm border-0">
                <div class="card-header bg-white py-3">
                    <h5 class="mb-0">System Configuration</h5>
                </div>
                <div class="card-body">
                    <div class="list-group list-group-flush">
                        <a href="#" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center px-0">
                            <div>
                                <h6 class="mb-1">Clinic Operating Hours</h6>
                                <small class="text-muted">08:00 AM - 08:00 PM</small>
                            </div>
                            <i class="bi bi-chevron-right text-muted"></i>
                        </a>
                        <a href="#" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center px-0">
                            <div>
                                <h6 class="mb-1">Appointment Duration</h6>
                                <small class="text-muted">Default: 30 minutes</small>
                            </div>
                            <i class="bi bi-chevron-right text-muted"></i>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Register Staff Modal -->
<div class="modal fade" id="registerStaffModal" tabindex="-1" aria-labelledby="registerStaffModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="registerStaffModalLabel">Register New Staff Member</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <form th:action="@{/admin/register-staff}" method="post">
          <div class="modal-body">
              <div class="mb-3">
                  <label class="form-label text-muted small fw-semibold">Role</label>
                  <select class="form-select" name="role" required>
                      <option value="DOCTOR">Doctor</option>
                      <option value="ADMIN">Administrator</option>
                  </select>
              </div>
              <div class="mb-3">
                  <label class="form-label text-muted small fw-semibold">Full Name</label>
                  <input type="text" class="form-control" name="name" required>
              </div>
              <div class="mb-3">
                  <label class="form-label text-muted small fw-semibold">Email Address</label>
                  <input type="email" class="form-control" name="email" required>
              </div>
              <div class="mb-3">
                  <label class="form-label text-muted small fw-semibold">Temporary Password</label>
                  <input type="password" class="form-control" name="password" required>
              </div>
          </div>
          <div class="modal-footer border-0">
            <button type="button" class="btn btn-light" data-bs-dismiss="modal">Cancel</button>
            <button type="submit" class="btn btn-primary">Register Staff</button>
          </div>
      </form>
    </div>
  </div>
</div>

<div th:replace="~{fragments/layout :: footer}"></div>
</body>
</html>
"""
write_file(os.path.join(templates_dir, "admin", "dashboard.html"), admin_dashboard)

print("Admin functionality added successfully.")
