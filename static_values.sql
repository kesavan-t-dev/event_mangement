INSERT INTO organiser (
    organiser_id,
    name,
    phone,
    email,
    updated_at,
    created_at,
    is_active
) VALUES
(
    gen_random_uuid(),
    'Google Meet',
    '9638527410',
    'contact@gdg.com',
    NOW(),
    NOW(),
    TRUE
),
(
    gen_random_uuid(),
    'FOSS Conferences',
    '9876543210',
    'info@globalconf.com',
    NOW(),
    NOW(),
    FALSE
),
(
    gen_random_uuid(),
    'Innovate tecg Meetups',
    '+91-9876543210',
    'hello@innovate.com',
    NOW(),
    NOW(),
    TRUE
);