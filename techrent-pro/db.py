equipment_data = {
    1: {
        "id": 1,
        "name": "Canon EOS R5",
        "category": "Camera",
        "daily_rate": 50.0,
        "quantity": 5,
        "description": "High-resolution mirrorless camera with advanced autofocus.",
        "available": True
    },
    2: {
        "id": 2,
        "name": "DJI Mavic Air 2",
        "category": "Drone",
        "daily_rate": 40.0,
        "quantity": 3,
        "description": "Compact drone with excellent camera capabilities.",
        "available": True
    },
    3: {
        "id": 3,
        "name": "GoPro HERO9 Black",
        "category": "Action Camera",
        "daily_rate": 20.0,
        "quantity": 10,
        "description": "Durable action camera with high-quality video recording.",
        "available": True
    },
    4: {
        "id": 4,
        "name": "Sony A7 III",
        "category": "Camera",
        "daily_rate": 45.0,
        "quantity": 4,
        "description": "Full-frame mirrorless camera with excellent low-light performance.",
        "available": True
    },
    5: {
        "id": 5,
        "name": "DJI Ronin-S",
        "category": "Gimbal",
        "daily_rate": 30.0,
        "quantity": 2,
        "description": "3-axis handheld gimbal stabilizer for smooth video footage.",
        "available": True
    },
    6: {
        "id": 6,
        "name": "Rode VideoMic Pro+",
        "category": "Microphone",
        "daily_rate": 15.0,
        "quantity": 8,
        "description": "Directional shotgun microphone for high-quality audio recording.",
        "available": True
    },
    7: {
        "id": 7,
        "name": "Manfrotto Befree Advanced Tripod",
        "category": "Tripod",
        "daily_rate": 10.0,
        "quantity": 6,
        "description": "Lightweight and compact tripod for travel photography.",
        "available": True
    },
    8: {
        "id": 8,
        "name": "Blackmagic Pocket Cinema Camera 6K",
        "category": "Camera",
        "daily_rate": 60.0,
        "quantity": 2,
        "description": "High-end cinema camera with Super 35 sensor and 6K recording.",
        "available": True
    },
    9: {
        "id": 9,
        "name": "DJI Inspire 2",
        "category": "Drone",
        "daily_rate": 70.0,
        "quantity": 1,
        "description": "Professional drone with advanced flight capabilities and camera options.",
        "available": True
    },
    10: {
        "id": 10,
        "name": "Zoom H6 Handy Recorder",
        "category": "Audio Recorder",
        "daily_rate": 25.0,
        "quantity": 5,
        "description": "Portable audio recorder with multiple input options for high-quality sound recording.",
        "available": True
    }
}

next_equipment_id = 11

customer_data = {
    1: {
        "id": 1,
        "name": "Alice Johnson",
        "email": "alice.johnson@example.com",
        "phone": "123-456-7890",
        "created_at": "2025-01-01T00:00:00Z"
    },
    2: {
        "id": 2,
        "name": "Bob Smith",
        "email": "bob.smith@example.com",
        "phone": "987-654-3210",
        "created_at": "2025-02-01T00:00:00Z"
    },
    3: {
        "id": 3,
        "name": "Charlie Brown",
        "email": "charlie.brown@example.com",
        "phone": "555-555-5555",
        "created_at": "2025-03-01T00:00:00Z"
    },
    4: {
        "id": 4,
        "name": "David Williams",
        "email": "david.williams@example.com",
        "phone": "444-444-4444",
        "created_at": "2025-04-01T00:00:00Z"
    },
    5: {
        "id": 5,
        "name": "Eve Thompson",
        "email": "eve.thompson@example.com",
        "phone": "333-333-3333",
        "created_at": "2025-05-01T00:00:00Z"
    },
    6: {
        "id": 6,
        "name": "Frank Miller",
        "email": "frank.miller@example.com",
        "phone": "222-222-2222",
        "created_at": "2025-06-01T00:00:00Z"
    },
    7: {
        "id": 7,
        "name": "Grace Lee",
        "email": "grace.lee@example.com",
        "phone": "111-111-1111",
        "created_at": "2025-07-01T00:00:00Z"
    },
    8: {
        "id": 8,
        "name": "Hannah White",
        "email": "hannah.white@example.com",
        "phone": "000-000-0000",
        "created_at": "2025-08-01T00:00:00Z"
    },
    9: {
        "id": 9,
        "name": "Ian Black",
        "email": "ian.black@example.com",
        "phone": "999-999-9999",
        "created_at": "2025-09-01T00:00:00Z"
    },
    10: {
        "id": 10,
        "name": "Jack Green",
        "email": "jack.green@example.com",
        "phone": "888-888-8888",
        "created_at": "2025-10-01T00:00:00Z"
    }
}

next_customer_id = 11

rental_data = {
    1: {
        "id": 1,
        "equipment_id": 1,
        "customer_id": 1,
        "start_date": "2025-04-01",
        "end_date": "2025-04-05",
        "status": "active",
        "total_cost": 250.0
    },
    2: {
        "id": 2,
        "equipment_id": 2,
        "customer_id": 2,
        "start_date": "2025-04-10",
        "end_date": "2025-04-12",
        "status": "returned",
        "total_cost": 80.0
    },
    3: {
        "id": 3,
        "equipment_id": 3,
        "customer_id": 3,
        "start_date": "2025-04-15",
        "end_date": "2025-04-20",
        "status": "overdue",
        "total_cost": 100.0
    },
    4: {
        "id": 4,
        "equipment_id": 1,
        "customer_id": 2,
        "start_date": "2025-04-22",
        "end_date": "2025-04-25",
        "status": "active",
        "total_cost": 150.0
    },
    5: {
        "id": 5,
        "equipment_id": 4,
        "customer_id": 1,
        "start_date": "2025-04-26",
        "end_date": "2025-04-30",
        "status": "active",
        "total_cost": 180.0
    },
    6: {
        "id": 6,
        "equipment_id": 5,
        "customer_id": 3,
        "start_date": "2025-05-01",
        "end_date": "2025-05-05",
        "status": "active",
        "total_cost": 120.0
    },
    7: {
        "id": 7,
        "equipment_id": 6,
        "customer_id": 1,
        "start_date": "2025-05-10",
        "end_date": "2025-05-15",
        "status": "active",
        "total_cost": 75.0
    },
    8: {
        "id": 8,
        "equipment_id": 2,
        "customer_id": 3,
        "start_date": "2025-05-20",
        "end_date": "2025-05-25",
        "status": "active",
        "total_cost": 200.0},
    9: {
        "id": 9,
        "equipment_id": 3,
        "customer_id": 2,
        "start_date": "2025-05-30",
        "end_date": "2025-06-05",
        "status": "active",
        "total_cost": 150.0},
    10: {
        "id": 10,
        "equipment_id": 4,
        "customer_id": 1,
        "start_date": "2025-06-10",
        "end_date": "2025-06-15",
        "status": "active",
        "total_cost": 225.0
    },
    11: {
        "id": 11,
        "equipment_id": 5,
        "customer_id": 2,
        "start_date": "2025-06-20",
        "end_date": "2025-06-25",
        "status": "active",
        "total_cost": 300.0
    },
    12: {
        "id": 12,
        "equipment_id": 6,
        "customer_id": 3,
        "start_date": "2025-07-01",
        "end_date": "2025-07-05",
        "status": "active",
        "total_cost": 125.0
    },
    13: {
        "id": 13,
        "equipment_id": 1,
        "customer_id": 1,
        "start_date": "2025-07-10",
        "end_date": "2025-07-15",
        "status": "active",
        "total_cost": 200.0
    },
    14: {
        "id": 14,
        "equipment_id": 2,
        "customer_id": 2,
        "start_date": "2025-07-20",
        "end_date": "2025-07-25",
        "status": "active",
        "total_cost": 250.0
    },
    15: {
        "id": 15,
        "equipment_id": 3,
        "customer_id": 3,
        "start_date": "2025-08-01",
        "end_date": "2025-08-05",
        "status": "active",
        "total_cost": 175.0
    },
    16: {
        "id": 16,
        "equipment_id": 4,
        "customer_id": 1,
        "start_date": "2025-08-10",
        "end_date": "2025-08-15",
        "status": "active",
        "total_cost": 225.0
    },
    17: {
        "id": 17,
        "equipment_id": 5,
        "customer_id": 2,
        "start_date": "2025-08-20",
        "end_date": "2025-08-25",
        "status": "active",
        "total_cost": 300.0
    },
    18: {
        "id": 18,
        "equipment_id": 6,
        "customer_id": 3,
        "start_date": "2025-09-01",
        "end_date": "2025-09-05",
        "status": "active",
        "total_cost": 125.0
    },
    19: {
        "id": 19,
        "equipment_id": 1,
        "customer_id": 1,
        "start_date": "2025-09-10",
        "end_date": "2025-09-15",
        "status": "active",
        "total_cost": 200.0
    },
    20: {
        "id": 20,
        "equipment_id": 2,
        "customer_id": 2,
        "start_date": "2025-09-20",
        "end_date": "2025-09-25",
        "status": "active",
        "total_cost": 250.0
    }
}

next_rental_id = 21
