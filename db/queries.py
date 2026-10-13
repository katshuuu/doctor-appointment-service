"""SQL-запросы, которые используют представления сайта.

Те же тексты с комментариями лежат в sql/queries.sql.
Значения подставляются только через параметры ?.
"""

DOCTORS = """
SELECT
    doctors.id,
    doctors.name,
    specialties.name AS specialty
FROM doctors
JOIN specialties
    ON doctors.specialty_id = specialties.id
ORDER BY doctors.id
"""

DOCTORS_BY_NAME = """
SELECT
    doctors.id,
    doctors.name,
    specialties.name AS specialty
FROM doctors
JOIN specialties
    ON doctors.specialty_id = specialties.id
WHERE doctors.name LIKE '%' || ? || '%'
ORDER BY doctors.name
"""

DOCTOR_BY_ID = """
SELECT
    doctors.id,
    doctors.name,
    specialties.name AS specialty
FROM doctors
JOIN specialties
    ON doctors.specialty_id = specialties.id
WHERE doctors.id = ?
"""

FREE_DOCTORS = """
SELECT
    doctors.id,
    doctors.name,
    specialties.name AS specialty
FROM doctors
JOIN specialties
    ON doctors.specialty_id = specialties.id
WHERE doctors.id NOT IN (
    SELECT appointments.doctor_id
    FROM appointments
    WHERE appointments.appointment_date = ?
        AND appointments.is_cancelled = 0
)
ORDER BY doctors.name
"""

SPECIALTIES = """
SELECT
    id,
    name
FROM specialties
ORDER BY id
"""

DOCTORS_BY_SPECIALTY = """
SELECT
    specialties.name AS name,
    COUNT(doctors.id) AS doctor_count
FROM specialties
LEFT JOIN doctors
    ON doctors.specialty_id = specialties.id
GROUP BY specialties.id, specialties.name
ORDER BY specialties.id
"""

DOCTORS_OF_SPECIALTY = """
SELECT
    doctors.id,
    doctors.name,
    specialties.name AS specialty
FROM doctors
JOIN specialties
    ON doctors.specialty_id = specialties.id
WHERE specialties.name = ?
ORDER BY doctors.name
"""

SPECIALTY_BY_NAME = """
SELECT
    id,
    name
FROM specialties
WHERE name = ?
"""

PATIENTS = """
SELECT
    id,
    name,
    age,
    CASE WHEN age < 18 THEN 1 ELSE 0 END AS is_minor
FROM patients
ORDER BY id
"""

PATIENT_BY_ID = """
SELECT
    id,
    name,
    age,
    CASE WHEN age < 18 THEN 1 ELSE 0 END AS is_minor
FROM patients
WHERE id = ?
"""

MINOR_PATIENTS = """
SELECT
    id,
    name,
    age
FROM patients
WHERE age < 18
ORDER BY age
"""

PATIENT_AGE_STATS = """
SELECT
    COUNT(*) AS patients_count,
    AVG(age) AS average_age,
    MIN(age) AS min_age,
    MAX(age) AS max_age
FROM patients
"""

APPOINTMENTS = """
SELECT
    appointments.id,
    appointments.appointment_date,
    appointments.appointment_time,
    appointments.is_cancelled,
    patients.name AS patient_name,
    patients.age AS patient_age,
    doctors.id AS doctor_id,
    doctors.name AS doctor_name,
    specialties.name AS specialty
FROM appointments
JOIN patients
    ON appointments.patient_id = patients.id
JOIN doctors
    ON appointments.doctor_id = doctors.id
JOIN specialties
    ON doctors.specialty_id = specialties.id
ORDER BY appointments.id
"""

ACTIVE_APPOINTMENTS = """
SELECT
    appointments.id,
    appointments.appointment_date,
    appointments.appointment_time,
    patients.name AS patient_name,
    doctors.name AS doctor_name
FROM appointments
JOIN patients
    ON appointments.patient_id = patients.id
JOIN doctors
    ON appointments.doctor_id = doctors.id
WHERE appointments.is_cancelled = 0
ORDER BY appointments.appointment_date, appointments.appointment_time
"""

APPOINTMENT_BY_ID = """
SELECT
    appointments.id,
    appointments.appointment_date,
    appointments.appointment_time,
    appointments.is_cancelled,
    patients.name AS patient_name,
    patients.age AS patient_age,
    CASE WHEN patients.age < 18 THEN 1 ELSE 0 END AS is_minor,
    doctors.id AS doctor_id,
    doctors.name AS doctor_name,
    specialties.name AS specialty
FROM appointments
JOIN patients
    ON appointments.patient_id = patients.id
JOIN doctors
    ON appointments.doctor_id = doctors.id
JOIN specialties
    ON doctors.specialty_id = specialties.id
WHERE appointments.id = ?
"""

APPOINTMENTS_BY_DOCTOR = """
SELECT
    appointments.id,
    appointments.appointment_date,
    appointments.appointment_time,
    appointments.is_cancelled,
    patients.name AS patient_name
FROM appointments
JOIN patients
    ON appointments.patient_id = patients.id
WHERE appointments.doctor_id = ?
ORDER BY appointments.id
"""

APPOINTMENTS_BY_PATIENT = """
SELECT
    appointments.id,
    appointments.appointment_date,
    appointments.appointment_time,
    appointments.is_cancelled,
    doctors.name AS doctor_name
FROM appointments
JOIN doctors
    ON appointments.doctor_id = doctors.id
WHERE appointments.patient_id = ?
ORDER BY appointments.id
"""

ACTIVE_APPOINTMENTS_COUNT = """
SELECT
    COUNT(*) AS appointments_count
FROM appointments
WHERE is_cancelled = 0
"""

STATS_BY_DOCTOR = """
SELECT
    doctors.name AS doctor_name,
    COUNT(appointments.id) AS appointments_count
FROM doctors
LEFT JOIN appointments
    ON doctors.id = appointments.doctor_id
    AND appointments.is_cancelled = 0
GROUP BY doctors.id, doctors.name
ORDER BY appointments_count DESC, doctors.name
"""

BUSY_DOCTORS = """
SELECT
    doctors.name AS doctor_name,
    COUNT(appointments.id) AS appointments_count
FROM doctors
JOIN appointments
    ON doctors.id = appointments.doctor_id
WHERE appointments.is_cancelled = 0
GROUP BY doctors.id, doctors.name
HAVING COUNT(appointments.id) > 1
ORDER BY appointments_count DESC
"""
