package com.hospital.hms.controller;

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
