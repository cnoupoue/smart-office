db = db.getSiblingDB('reservationDB');

// Collection client
db.client.insertMany([
    {
        id_client: 1,
        login: "john_doe",
        role: "user",
        firstname: "John",
        name: "Doe",
        password: "hashed_password",
        salt: "random_salt"
    }
]);

// Collection premise
db.premise.insertMany([
    {
        id_premise: 1,
        name: "Conference Room A"
    }
]);

// Collection reservation
db.reservation.insertMany([
    {
        start_time: ISODate("2024-06-01T10:00:00Z"),
        end_time: ISODate("2024-06-01T12:00:00Z"),
        client_id: 1,
        premise_id: 1
    }
]);

// Collection log
db.log.insertMany([
    {
        id_log: 1,
        topic: "reservation",
        date_log: ISODate("2024-06-01T09:00:00Z"),
        value_log: "Reservation created successfully"
    }
]);

