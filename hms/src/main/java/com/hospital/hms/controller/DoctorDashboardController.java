package com.hospital.hms.controller;

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
