-- Проверенные запросы сервиса записи к врачу.
-- В представлениях значения передаются параметром ?, а не склейкой строк.

-- 1. Выборка списка: все врачи и их специальности
SELECT
    doctors.id,
    doctors.name,
    specialties.name AS specialty
FROM doctors
JOIN specialties
    ON doctors.specialty_id = specialties.id
ORDER BY doctors.id;

-- 2. Выборка списка: справочник специальностей
SELECT
    id,
    name
FROM specialties
ORDER BY id;

-- 3. Выборка списка: пациенты в порядке появления в записях
SELECT
    id,
    name,
    age,
    CASE WHEN age < 18 THEN 1 ELSE 0 END AS is_minor
FROM patients
ORDER BY id;

-- 4. Фильтрация WHERE: поиск врача по части имени
-- В приложении вместо образца передаётся параметр ?
SELECT
    doctors.id,
    doctors.name,
    specialties.name AS specialty
FROM doctors
JOIN specialties
    ON doctors.specialty_id = specialties.id
WHERE doctors.name LIKE '%Смирнова%'
ORDER BY doctors.name;

-- 5. Фильтрация WHERE: врачи одной специальности
-- В приложении название передаётся параметром ?
SELECT
    doctors.id,
    doctors.name,
    specialties.name AS specialty
FROM doctors
JOIN specialties
    ON doctors.specialty_id = specialties.id
WHERE specialties.name = 'Кардиолог'
ORDER BY doctors.name;

-- 6. Фильтрация WHERE: только активные записи
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
ORDER BY appointments.appointment_date, appointments.appointment_time;

-- 7. Фильтрация WHERE: несовершеннолетние пациенты
SELECT
    id,
    name,
    age
FROM patients
WHERE age < 18
ORDER BY age;

-- 8. Соединение JOIN: полная карточка записи
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
ORDER BY appointments.id;

-- 9. Соединение JOIN: одна запись по идентификатору
-- В приложении 3 заменяется параметром ?
SELECT
    appointments.id,
    patients.name AS patient_name,
    doctors.name AS doctor_name,
    specialties.name AS specialty
FROM appointments
JOIN patients
    ON appointments.patient_id = patients.id
JOIN doctors
    ON appointments.doctor_id = doctors.id
JOIN specialties
    ON doctors.specialty_id = specialties.id
WHERE appointments.id = 3;

-- 10. Свободные врачи на выбранную дату.
-- Врач свободен, если на эту дату у него нет активной записи.
-- В приложении дата передаётся параметром ?
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
    WHERE appointments.appointment_date = '2026-09-15'
        AND appointments.is_cancelled = 0
)
ORDER BY doctors.name;

-- 11. Агрегатная функция: число активных записей
SELECT
    COUNT(*) AS appointments_count
FROM appointments
WHERE is_cancelled = 0;

-- 12. Агрегатные функции: возраст пациентов
SELECT
    COUNT(*) AS patients_count,
    AVG(age) AS average_age,
    MIN(age) AS min_age,
    MAX(age) AS max_age
FROM patients;

-- 13. Группировка GROUP BY: число врачей по специальностям
SELECT
    specialties.name AS name,
    COUNT(doctors.id) AS doctor_count
FROM specialties
LEFT JOIN doctors
    ON doctors.specialty_id = specialties.id
GROUP BY specialties.id, specialties.name
ORDER BY specialties.id;

-- 14. Группировка GROUP BY: активные записи каждого врача
SELECT
    doctors.name AS doctor_name,
    COUNT(appointments.id) AS appointments_count
FROM doctors
LEFT JOIN appointments
    ON doctors.id = appointments.doctor_id
    AND appointments.is_cancelled = 0
GROUP BY doctors.id, doctors.name
ORDER BY appointments_count DESC, doctors.name;

-- 15. Фильтрация групп HAVING: врачи более чем с одной активной записью
SELECT
    doctors.name AS doctor_name,
    COUNT(appointments.id) AS appointments_count
FROM doctors
JOIN appointments
    ON doctors.id = appointments.doctor_id
WHERE appointments.is_cancelled = 0
GROUP BY doctors.id, doctors.name
HAVING COUNT(appointments.id) > 1
ORDER BY appointments_count DESC;
