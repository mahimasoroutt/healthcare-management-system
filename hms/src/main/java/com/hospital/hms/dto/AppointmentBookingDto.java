package com.hospital.hms.dto;
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
