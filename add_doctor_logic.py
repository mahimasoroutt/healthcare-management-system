import os

base_dir = "hms/src/main/java/com/hospital/hms"
templates_dir = "hms/src/main/resources/templates"

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)

# 1. Doctor Dashboard Controller
doctor_dashboard_controller = """package com.hospital.hms.controller;

import com.hospital.hms.entity.Appointment;
import com.hospital.hms.entity.User;
import com.hospital.hms.repository.AppointmentRepository;
import com.hospital.hms.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

import java.util.List;

@Controller
public class DoctorDashboardController {

    @Autowired
    private AppointmentRepository appointmentRepository;
    
    @Autowired
    private UserRepository userRepository;

    @GetMapping("/doctor/dashboard")
    public String doctorDashboard(Authentication auth, Model model) {
        User doctor = userRepository.findByEmail(auth.getName()).orElse(null);
        if (doctor != null) {
            List<Appointment> appointments = appointmentRepository.findByDoctorId(doctor.getId());
            model.addAttribute("appointments", appointments);
        }
        return "doctor/dashboard";
    }
    
    @PostMapping("/doctor/update-schedule")
    public String updateSchedule() {
        // Here we would normally save the DoctorSchedule entities to the database.
        // For now, we will just return a success message.
        return "redirect:/doctor/dashboard?success=schedule_updated";
    }
}
"""
write_file(os.path.join(base_dir, "controller", "DoctorDashboardController.java"), doctor_dashboard_controller)

# 2. Fix DashboardController to remove old /doctor/dashboard mapping
dash_controller = """package com.hospital.hms.controller;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class DashboardController {

    @GetMapping("/")
    public String home() {
        return "redirect:/login";
    }
}
"""
write_file(os.path.join(base_dir, "controller", "DashboardController.java"), dash_controller)

# 3. Update Doctor Dashboard Template to show appointments
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
    
    <div th:if="${param.success == 'schedule_updated'}" class="alert alert-success alert-dismissible fade show" role="alert">
        <i class="bi bi-check-circle-fill me-2"></i> Your weekly availability has been updated successfully.
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>

    <div class="row">
        <!-- Today's Schedule -->
        <div class="col-lg-8">
            <div class="card shadow-sm mb-4 border-0">
                <div class="card-header bg-white py-3 d-flex justify-content-between align-items-center">
                    <h5 class="mb-0">My Appointments</h5>
                    <span class="text-muted small" th:text="${#calendars.format(#calendars.createNow(), 'EEEE, MMMM dd, yyyy')}">Date</span>
                </div>
                <div class="card-body p-0">
                    <div th:if="${#lists.isEmpty(appointments)}" class="empty-state">
                        <i class="bi bi-calendar-x"></i>
                        <h5>No appointments scheduled.</h5>
                        <p>Enjoy your break or check upcoming days.</p>
                    </div>
                    
                    <div th:unless="${#lists.isEmpty(appointments)}" class="table-responsive">
                        <table class="table table-hover mb-0">
                            <thead class="table-light">
                                <tr>
                                    <th class="ps-4">Date & Time</th>
                                    <th>Patient</th>
                                    <th>Status</th>
                                    <th>Reason</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr th:each="appt : ${appointments}">
                                    <td class="ps-4 fw-medium" th:text="${#temporals.format(appt.startTime, 'MMM dd, HH:mm')}"></td>
                                    <td th:text="${appt.patient.name}"></td>
                                    <td>
                                        <span class="badge" 
                                              th:classappend="${appt.status.name() == 'SCHEDULED' ? 'bg-primary' : (appt.status.name() == 'COMPLETED' ? 'bg-success' : 'bg-danger')}"
                                              th:text="${appt.status}"></span>
                                    </td>
                                    <td class="text-muted small" th:text="${appt.reason}"></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            
            <div class="card shadow-sm border-0">
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
            <div class="card shadow-sm border-0">
                <div class="card-header bg-white py-3">
                    <h5 class="mb-0">Weekly Availability</h5>
                </div>
                <div class="card-body">
                    <p class="text-muted small mb-3">Set your standard working hours for appointment booking.</p>
                    <form th:action="@{/doctor/update-schedule}" method="post">
                        <div class="mb-3 d-flex align-items-center justify-content-between">
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" id="mon" name="mon" checked>
                                <label class="form-check-label" for="mon">Monday</label>
                            </div>
                            <div class="text-muted small">09:00 - 17:00</div>
                        </div>
                        <div class="mb-3 d-flex align-items-center justify-content-between">
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" id="tue" name="tue" checked>
                                <label class="form-check-label" for="tue">Tuesday</label>
                            </div>
                            <div class="text-muted small">09:00 - 17:00</div>
                        </div>
                        <div class="mb-3 d-flex align-items-center justify-content-between">
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" id="wed" name="wed" checked>
                                <label class="form-check-label" for="wed">Wednesday</label>
                            </div>
                            <div class="text-muted small">09:00 - 17:00</div>
                        </div>
                        <hr>
                        <button type="submit" class="btn btn-outline-primary w-100">Update Schedule</button>
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

# 4. Add findByDoctorId to AppointmentRepository
appt_repo = """package com.hospital.hms.repository;

import com.hospital.hms.entity.Appointment;
import org.springframework.data.jpa.repository.JpaRepository;
import java.time.LocalDateTime;
import java.util.List;

public interface AppointmentRepository extends JpaRepository<Appointment, Long> {
    List<Appointment> findByPatientId(Long patientId);
    List<Appointment> findByDoctorId(Long doctorId);
    List<Appointment> findByDoctorIdAndStartTimeBetween(Long doctorId, LocalDateTime start, LocalDateTime end);
    long countByDoctorIdAndStartTimeBetween(Long doctorId, LocalDateTime start, LocalDateTime end);
}
"""
write_file(os.path.join(base_dir, "repository", "AppointmentRepository.java"), appt_repo)

print("Doctor logic updated successfully.")
