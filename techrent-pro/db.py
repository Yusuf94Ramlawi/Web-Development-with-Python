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
    }
}

next_equipment_id = 7

customer_data = {
    1: {
        "id": 1,
        "name": "Alice Johnson",
        "email": "alice.johnson@example.com",
        "phone": "123-456-7890",
        "created_at": "2023-01-01T00:00:00Z"
    },
    2: {
        "id": 2,
        "name": "Bob Smith",
        "email": "bob.smith@example.com",
        "phone": "987-654-3210",
        "created_at": "2023-02-01T00:00:00Z"
    },
    3: {
        "id": 3,
        "name": "Charlie Brown",
        "email": "charlie.brown@example.com",
        "phone": "555-555-5555",
        "created_at": "2023-03-01T00:00:00Z"
    }
}

next_customer_id = 4

rental_data = {
    1: {
        "id": 1,
        "equipment_id": 1,
        "customer_id": 1,
        "start_date": "2023-04-01",
        "end_date": "2023-04-05",
        "status": "active",
        "total_cost": 250.0
    },
    2: {
        "id": 2,
        "equipment_id": 2,
        "customer_id": 2,
        "start_date": "2023-04-10",
        "end_date": "2023-04-12",
        "status": "returned",
        "total_cost": 80.0
    },
    3: {
        "id": 3,
        "equipment_id": 3,
        "customer_id": 3,
        "start_date": "2023-04-15",
        "end_date": "2023-04-20",
        "status": "overdue",
        "total_cost": 100.0
    },
    4: {
        "id": 4,
        "equipment_id": 1,
        "customer_id": 2,
        "start_date": "2023-04-22",
        "end_date": "2023-04-25",
        "status": "active",
        "total_cost": 150.0
    },
    5: {
        "id": 5,
        "equipment_id": 4,
        "customer_id": 1,
        "start_date": "2023-04-26",
        "end_date": "2023-04-30",
        "status": "active",
        "total_cost": 180.0
    },
    6: {
        "id": 6,
        "equipment_id": 5,
        "customer_id": 3,
        "start_date": "2023-05-01",
        "end_date": "2023-05-05",
        "status": "active",
        "total_cost": 120.0
    },
    7: {
        "id": 7,
        "equipment_id": 6,
        "customer_id": 1,
        "start_date": "2023-05-10",
        "end_date": "2023-05-15",
        "status": "active",
        "total_cost": 75.0
    },
    8: {
        "id": 8,
        "equipment_id": 2,
        "customer_id": 3,
        "start_date": "2023-05-20",
        "end_date": "2023-05-25",
        "status": "active",
        "total_cost": 200.0},
    9: {
        "id": 9,
        "equipment_id": 3,
        "customer_id": 2,
        "start_date": "2023-05-30",
        "end_date": "2023-06-05",
        "status": "active",
        "total_cost": 150.0},
    10: {
        "id": 10,
        "equipment_id": 4,
        "customer_id": 1,
        "start_date": "2023-06-10",
        "end_date": "2023-06-15",
        "status": "active",
        "total_cost": 225.0
    }
}

next_rental_id = 11