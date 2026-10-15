package com.hospital.hms.service;
import com.hospital.hms.dto.UserRegistrationDto;
import com.hospital.hms.entity.User;
import java.util.List;

public interface UserService {
    User registerPatient(UserRegistrationDto registrationDto);
    User findByEmail(String email);
    List<User> getAllUsers();
}
