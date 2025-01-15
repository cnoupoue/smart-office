db = db.getSiblingDB('reservationDB');

// Drop existing collections if they exist
db.client.drop();
db.premise.drop();
db.reservation.drop();
db.device.drop();
db.log.drop();

// Create the 'log' collection
db.createCollection("log");
db.log.insertMany([
    {
        _id: ObjectId(),
        topic: "smartoffice/2/1000000044888d31/rfid",
        date_log: ISODate("2024-12-25T09:15:00Z"),
        value_log: "0000AEC6680",
        id_premise: "1",
        id_device: "1000000044888d311"
    },
    {
        _id: ObjectId(),
        topic: "smartoffice/2/1000000044888d31/sound_sensor",
        date_log: ISODate("2024-12-25T09:20:00Z"),
        value_log: "OPEN",
        id_premise: db.premise.findOne({ name: "290A" })._id,
        id_device: db.device.findOne({ name: "MyRPI-IoT" })._id
    }
]);

print("Database and collections initialized successfully.");

