# Hospital Management System (HMS) - Application Module

This directory contains the Spring Boot application module for the Hospital Management System.

For complete step-by-step setup, configuration, and run instructions, please refer to the main [Root README.md](../README.md).

## Quick Run

### 1. Configure Local Database Credentials
Create `application-local.properties` in this directory:
```properties
spring.datasource.username=root
spring.datasource.password=your_mysql_password
```

### 2. Run with Maven Wrapper
- **Windows**:
  ```powershell
  .\mvnw.cmd spring-boot:run
  ```
- **macOS / Linux**:
  ```bash
  ./mvnw spring-boot:run
  ```

### 3. Open in Browser
Navigate to [http://localhost:8080](http://localhost:8080).
