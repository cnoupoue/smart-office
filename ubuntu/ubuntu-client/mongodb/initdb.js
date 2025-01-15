db = db.getSiblingDB('reservationDB');

// Drop existing collections if they exist
db.client.drop();
db.premise.drop();
db.reservation.drop();
db.device.drop();
db.log.drop();

// Create the 'client' collection
db.createCollection("client");
db.client.insertMany([
    {
        _id: ObjectId(),
        email: "cameron.noupoue@student.hepl.be",
        firstname: "Cameron",
        name: "Noupoue",
        telephone: 123456789,
        password: "$2b$12$lNEgT3SSWrQeR/6RIoCfVe.DSg.zs82PvlO8rpesoP4gtQwOik8fW",
        salt: "$2b$12$lNEgT3SSWrQeR/6RIoCfVe",
        role: "user",
        rfid: "027004241250",
    },
    {
        _id: ObjectId(),
        email: "nasser.kotiyev@student.hepl.be",
        firstname: "Nasser",
        name: "Kotiyev",
        telephone: 987654321,
        password: "$2b$12$lNEgT3SSWrQeR/6RIoCfVe.DSg.zs82PvlO8rpesoP4gtQwOik8fW",
        salt: "$2b$12$lNEgT3SSWrQeR/6RIoCfVe",
        role: "admin",
        rfid: "000000006680",
    }
]);

// Create the 'premise' collection
db.createCollection("premise");
db.premise.insertMany([
    {
        _id: ObjectId(),
        name: "290A"
    },
    {
        _id: ObjectId(),
        name: "290C"
    }
]);

// Create the 'device' collection
db.createCollection("device");
db.device.insertMany([
    {
        _id: "1000000044888d31",
        id_premise: db.premise.findOne({ name: "290A" })._id
    },
]);

// Create the 'reservation' collection
db.createCollection("reservation");
db.reservation.insertMany([
    {
        _id: ObjectId(),
        start_time: ISODate("2024-12-25T09:00:00Z"),
        end_time: ISODate("2024-12-25T10:00:00Z"),
        id_premise: db.premise.findOne({ name: "290A" })._id,
        id_client: db.client.findOne({ rfid: "027004241250" })._id
    },
    {
        _id: ObjectId(),
        start_time: ISODate("2024-12-25T11:00:00Z"),
        end_time: ISODate("2024-12-25T12:00:00Z"),
        id_premise: db.premise.findOne({ name: "290A" })._id,
        id_client: db.client.findOne({ rfid: "027004241250" })._id
    }
]);

// Create the 'log' collection
db.createCollection("log");
db.log.insertMany([
    {
        _id: ObjectId(),
        topic: "rfid",
        date_log: ISODate("2024-12-25T09:15:00Z"),
        value_log: "027004241250",
        id_premise: db.premise.findOne({ name: "290A" })._id,
        id_device: "1000000044888d31"
    },
    {
        _id: ObjectId(),
        topic: "rfid",
        date_log: ISODate("2024-12-26T09:20:00Z"),
        value_log: "027004241250",
        id_premise: db.premise.findOne({ name: "290A" })._id,
        id_device: "1000000044888d31"
    }
]);

print("Database and collections initialized successfully.");

