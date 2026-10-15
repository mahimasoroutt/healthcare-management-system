package com.hospital.hms.repository;
import com.hospital.hms.entity.PatientFeedback;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface PatientFeedbackRepository extends JpaRepository<PatientFeedback, Long> {
    List<PatientFeedback> findByDoctorId(Long doctorId);
    List<PatientFeedback> findByPatientId(Long patientId);
}
