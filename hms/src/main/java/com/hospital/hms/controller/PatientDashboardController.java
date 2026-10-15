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
