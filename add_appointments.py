import os

base_dir = "hms/src/main/java/com/hospital/hms"
templates_dir = "hms/src/main/resources/templates"

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)

# 1. DTO for booking
booking_dto = """package com.hospital.hms.dto;
import org.springframework.format.annotation.DateTimeFormat;
import java.time.LocalDateTime;

public class AppointmentBookingDto {
    private Long doctorId;
    
    @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME)
    private LocalDateTime startTime;
    
    private String reason;

    // Getters and setters
    public Long getDoctorId() { return doctorId; }
    public void setDoctorId(Long doctorId) { this.doctorId = doctorId; }
    public LocalDateTime getStartTime() { return startTime; }
    public void setStartTime(LocalDateTime startTime) { this.startTime = startTime; }
    public String getReason() { return reason; }
    public void setReason(String reason) { this.reason = reason; }
}
"""
write_file(os.path.join(base_dir, "dto", "AppointmentBookingDto.java"), booking_dto)

# 2. Appointment Controller
appointment_controller = """package com.hospital.hms.controller;

import com.hospital.hms.dto.AppointmentBookingDto;
import com.hospital.hms.entity.Appointment;
import com.hospital.hms.entity.AppointmentStatus;
import com.hospital.hms.entity.Role;
import com.hospital.hms.entity.User;
import com.hospital.hms.repository.AppointmentRepository;
import com.hospital.hms.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;

@Controller
@RequestMapping("/patient/appointments")
public class AppointmentController {

    @Autowired
    private AppointmentRepository appointmentRepository;

    @Autowired
    private UserRepository userRepository;

    @GetMapping("/new")
    public String showBookingForm(Model model) {
        List<User> doctors = userRepository.findByRole(Role.DOCTOR);
        model.addAttribute("doctors", doctors);
        model.addAttribute("bookingDto", new AppointmentBookingDto());
        return "patient/book-appointment";
    }

    @PostMapping("/book")
    public String bookAppointment(@ModelAttribute("bookingDto") AppointmentBookingDto dto, Authentication auth, Model model) {
        User patient = userRepository.findByEmail(auth.getName()).orElse(null);
        User doctor = userRepository.findById(dto.getDoctorId()).orElse(null);
        
        if (patient == null || doctor == null) {
            return "redirect:/patient/appointments/new?error=invalid_user";
        }
        
        // Basic conflict checking (very simple for demo)
        LocalDateTime endTime = dto.getStartTime().plusMinutes(30);
        long conflicts = appointmentRepository.countByDoctorIdAndStartTimeBetween(doctor.getId(), dto.getStartTime().minusMinutes(29), endTime);
        if (conflicts > 0) {
            return "redirect:/patient/appointments/new?error=conflict";
        }

        Appointment appt = new Appointment();
        appt.setPatient(patient);
        appt.setDoctor(doctor);
        appt.setStartTime(dto.getStartTime());
        appt.setEndTime(endTime);
        appt.setStatus(AppointmentStatus.SCHEDULED);
        appt.setReason(dto.getReason());
        
        appointmentRepository.save(appt);
        
        return "redirect:/patient/dashboard?success=booked";
    }
}
"""
write_file(os.path.join(base_dir, "controller", "AppointmentController.java"), appointment_controller)

# 3. Patient Dashboard Controller to show appointments
patient_dashboard_controller = """package com.hospital.hms.controller;

import com.hospital.hms.entity.Appointment;
import com.hospital.hms.entity.User;
import com.hospital.hms.repository.AppointmentRepository;
import com.hospital.hms.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.List;

@Controller
public class PatientDashboardController {

    @Autowired
    private AppointmentRepository appointmentRepository;
    
    @Autowired
    private UserRepository userRepository;

    @GetMapping("/patient/dashboard")
    public String patientDashboard(Authentication auth, Model model) {
        User patient = userRepository.findByEmail(auth.getName()).orElse(null);
        if (patient != null) {
            List<Appointment> appointments = appointmentRepository.findByPatientId(patient.getId());
            model.addAttribute("appointments", appointments);
            model.addAttribute("patient", patient);
        }
        return "patient/dashboard";
    }
}
"""
# Replace the empty dashboard mapping for patient in DashboardController.java to avoid conflicts
# We will just rewrite DashboardController
dash_controller = """package com.hospital.hms.controller;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class DashboardController {

    @GetMapping("/")
    public String home() {
        return "redirect:/login";
    }

    @GetMapping("/admin/dashboard")
    public String adminDashboard() {
        return "admin/dashboard";
    }

    @GetMapping("/doctor/dashboard")
    public String doctorDashboard() {
        return "doctor/dashboard";
    }
}
"""
write_file(os.path.join(base_dir, "controller", "DashboardController.java"), dash_controller)
write_file(os.path.join(base_dir, "controller", "PatientDashboardController.java"), patient_dashboard_controller)

# 4. Booking Template
booking_template = """<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head th:replace="~{fragments/layout :: head('Book Appointment')}"></head>
<body class="d-flex flex-column min-vh-100">
<div th:replace="~{fragments/layout :: navbar}"></div>

<div class="container mb-5">
    <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
            <div class="card shadow-sm border-0">
                <div class="card-header bg-white py-3">
                    <h5 class="mb-0"><i class="bi bi-calendar-plus text-primary me-2"></i> Book a Consultation</h5>
                </div>
                <div class="card-body p-4">
                    <div th:if="${param.error == 'conflict'}" class="alert alert-danger">
                        The selected time slot conflicts with an existing appointment. Please choose another time.
                    </div>
                    
                    <form th:action="@{/patient/appointments/book}" th:object="${bookingDto}" method="post">
                        <div class="mb-4">
                            <label class="form-label fw-semibold text-muted small">Select Doctor</label>
                            <select class="form-select" th:field="*{doctorId}" required>
                                <option value="" disabled selected>Choose a physician...</option>
                                <option th:each="doc : ${doctors}" th:value="${doc.id}" th:text="${doc.name}"></option>
                            </select>
                        </div>
                        
                        <div class="mb-4">
                            <label class="form-label fw-semibold text-muted small">Preferred Date & Time</label>
                            <input type="datetime-local" class="form-control" th:field="*{startTime}" required>
                            <div class="form-text small">Appointments are scheduled for 30-minute intervals.</div>
                        </div>
                        
                        <div class="mb-4">
                            <label class="form-label fw-semibold text-muted small">Reason for Visit</label>
                            <textarea class="form-control" th:field="*{reason}" rows="3" placeholder="Briefly describe your symptoms or reason for visit..."></textarea>
                        </div>
                        
                        <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                            <a th:href="@{/patient/dashboard}" class="btn btn-light border">Cancel</a>
                            <button type="submit" class="btn btn-primary px-4">Confirm Booking</button>
                        </div>
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
write_file(os.path.join(templates_dir, "patient", "book-appointment.html"), booking_template)

# 5. Update patient dashboard to dynamically show appointments
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
        <a th:href="@{/patient/appointments/new}" class="btn btn-primary"><i class="bi bi-calendar-plus"></i> Book Appointment</a>
    </div>

    <div th:if="${param.success == 'booked'}" class="alert alert-success alert-dismissible fade show" role="alert">
        <i class="bi bi-check-circle-fill me-2"></i> Your appointment has been successfully scheduled!
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>

    <div class="row g-4">
        <div class="col-lg-8">
            <div class="card shadow-sm mb-4 border-0">
                <div class="card-header bg-white py-3">
                    <h5 class="mb-0">My Appointments</h5>
                </div>
                <div class="card-body p-0">
                    <div th:if="${#lists.isEmpty(appointments)}" class="empty-state">
                        <i class="bi bi-calendar2-check"></i>
                        <h5>No appointments found</h5>
                        <p>You have no scheduled visits at the moment.</p>
                        <a th:href="@{/patient/appointments/new}" class="btn btn-outline-primary mt-2">Book a Session</a>
                    </div>
                    
                    <div th:unless="${#lists.isEmpty(appointments)}" class="table-responsive">
                        <table class="table table-hover mb-0">
                            <thead class="table-light">
                                <tr>
                                    <th class="ps-4">Date & Time</th>
                                    <th>Doctor</th>
                                    <th>Status</th>
                                    <th>Reason</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr th:each="appt : ${appointments}">
                                    <td class="ps-4 fw-medium" th:text="${#temporals.format(appt.startTime, 'MMM dd, yyyy HH:mm')}"></td>
                                    <td th:text="${appt.doctor.name}"></td>
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
            <div class="card shadow-sm border-0">
                <div class="card-header bg-white py-3">
                    <h5 class="mb-0">Profile Summary</h5>
                </div>
                <div class="card-body text-center pt-4">
                    <div class="display-1 text-muted mb-3"><i class="bi bi-person-circle"></i></div>
                    <h5 class="mb-1" th:text="${patient != null ? patient.name : 'Unknown'}">Patient Name</h5>
                    <p class="text-muted small">Registered Patient</p>
                    <hr>
                    <ul class="list-unstyled text-start mb-0">
                        <li class="mb-2"><i class="bi bi-envelope text-muted me-2"></i> <span th:text="${patient != null ? patient.email : 'N/A'}"></span></li>
                    </ul>
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

print("Appointment booking logic added successfully.")
