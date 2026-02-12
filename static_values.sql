INSERT INTO organiser (
    organiser_id,
    name,
    phone,
    email,
    password,
    updated_at,
    created_at,
    is_active
) VALUES
(
    gen_random_uuid(),
    'Google Meet',
    '9638527410',
    'contact@gdg.com',
    'contact963852',
    NOW(),
    NOW(),
    TRUE
),
(
    gen_random_uuid(),
    'FOSS Conferences',
    '9876543210',
    'info@globalconf.com',
    'info987654',
    NOW(),
    NOW(),
    FALSE
),
(
    gen_random_uuid(),
    'Innovate tecg Meetups',
    '9876543210',
    'hello@innovate.com',
    'hello98765',
    NOW(),
    NOW(),
    TRUE
);