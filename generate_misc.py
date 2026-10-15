import os

base_dir = "hms"

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)

# DataInitializer
data_init_path = os.path.join(base_dir, "src/main/java/com/hospital/hms/config")
os.makedirs(data_init_path, exist_ok=True)
data_init_content = """package com.hospital.hms.config;

import com.hospital.hms.entity.Role;
import com.hospital.hms.entity.User;
import com.hospital.hms.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

@Component
public class DataInitializer implements CommandLineRunner {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Override
    public void run(String... args) throws Exception {
        if (userRepository.findByEmail("admin@hospital.com").isEmpty()) {
            User admin = new User();
            admin.setName("System Admin");
            admin.setEmail("admin@hospital.com");
            admin.setPassword(passwordEncoder.encode("admin123"));
            admin.setRole(Role.ADMIN);
            admin.setEnabled(true);
            userRepository.save(admin);
            System.out.println("Admin user created.");
        }
        
        if (userRepository.findByEmail("doctor@hospital.com").isEmpty()) {
            User doctor = new User();
            doctor.setName("Dr. John Smith");
            doctor.setEmail("doctor@hospital.com");
            doctor.setPassword(passwordEncoder.encode("doctor123"));
            doctor.setRole(Role.DOCTOR);
            doctor.setEnabled(true);
            userRepository.save(doctor);
            System.out.println("Doctor user created.");
        }
    }
}
"""
write_file(os.path.join(data_init_path, "DataInitializer.java"), data_init_content)

# .env.example
env_content = """# Database configuration
DB_USERNAME=root
DB_PASSWORD=root
"""
write_file(os.path.join(base_dir, ".env.example"), env_content)

# .gitignore
gitignore_content = """target/
!.mvn/wrapper/maven-wrapper.jar
!**/src/main/**/target/
!**/src/test/**/target/

### STS ###
.apt_generated
.classpath
.factorypath
.project
.settings
.springBeans
.sts4-cache

### IntelliJ IDEA ###
.idea
*.iws
*.iml
*.ipr

### NetBeans ###
/nbproject/private/
/nbbuild/
/dist/
/nbdist/
/.nb-gradle/
build/
!**/src/main/**/build/
!**/src/test/**/build/

### VS Code ###
.vscode/
"""
write_file(os.path.join(base_dir, ".gitignore"), gitignore_content)

# README.md
readme_content = """# Hospital Management System (HMS)

This is a comprehensive Hospital Management System built with Java, Spring Boot, Spring Data JPA/Hibernate, MySQL, and Thymeleaf.

## Features
- **Roles:** Admin, Doctor, Patient
- **Authentication:** Spring Security with BCrypt
- **Design:** Clean, accessible interfaces using Bootstrap 5 with custom tokens

## Setup Instructions

1. **Database Setup**
   Ensure MySQL is running on your machine.
   The application will create a database named `hospital_managment` if it doesn't exist, and `ddl-auto=update` will generate the schema.
   
2. **Environment Variables**
   Set `DB_USERNAME` and `DB_PASSWORD` (default: root/root).
   See `.env.example`.

3. **Running the application**
   Navigate to the project root (`hms` folder).
   Since Maven is not installed globally in your workspace, you must install Maven to build this, or run it through an IDE like IntelliJ / Eclipse.
   ```bash
   mvn spring-boot:run
   ```

4. **Demo Data**
   The application creates two default users on startup:
   - Admin: `admin@hospital.com` / `admin123`
   - Doctor: `doctor@hospital.com` / `doctor123`

## Known Limitations / Remaining Work
- Core UI structures and controllers for Admin/Doctor/Patient dashboards are scaffolded but the individual appointment booking algorithms and form views require full domain logic implementations.
- Appointment conflict detection logic needs to be added into the service layer.
"""
write_file(os.path.join(base_dir, "README.md"), readme_content)

print("Misc files generated.")
