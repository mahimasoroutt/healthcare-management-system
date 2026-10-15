package com.hospital.hms.controller;

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
