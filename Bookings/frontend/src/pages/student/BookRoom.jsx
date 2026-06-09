import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import Sidebar from "../../components/Sidebar";
import api from "../../services/api";

function BookRoom() {

    const { roomId } = useParams();
    const [bookingDate, setBookingDate] = useState("");
    const [availableSlots, setAvailableSlots] = useState([]);
    const [selectedSlot, setSelectedSlot] = useState("");
    const [customStartTime, setCustomStartTime] = useState("");
    const [customEndTime, setCustomEndTime] = useState("");
    const [participants, setParticipants] = useState("");
    const [eventName, setEventName] = useState("");
    const [eventCategory, setEventCategory] = useState("");
    const [alternativeRoom, setAlternativeRoom] = useState(null);
    useEffect(() => {

        if (!bookingDate)
            return;

        console.log("DATE:", bookingDate);

        api.get(
            `/available-slots/${roomId}/${bookingDate}`
        )
        .then((response) => {

            console.log(
                "SLOTS:",
                response.data
            );
            setAvailableSlots(
                response.data
            );

        });

    }, [bookingDate]);
        const handleSubmit = () => {

            if (!bookingDate) {

                alert("Select Booking Date");
                return;

            }

            if (!eventName) {

                alert("Enter Event Name");
                return;

            }

            if (!eventCategory) {

                alert("Select Event Category");
                return;

            }

            if (participants <= 0) {

                alert("Participants must be greater than 0");
                return;

            }

            if (!selectedSlot && (!customStartTime || !customEndTime)) {

                alert(
                    "Select a slot or enter custom time"
                );

                return;

            }

            api.post(
                "/book-room",
                {
                    booking_id: Math.floor(Math.random() * 10000),

                    requester_id: "STU001",

                    requester_type: "Student Coordinator",

                    event_name: eventName,

                    purpose: eventName,

                    event_category: eventCategory,

                    participant_count: Number(participants),

                    request_reason: eventName,

                    resource_id: Number(roomId),

                    booking_date: bookingDate,

                    start_time: selectedSlot
                        ? selectedSlot.split("-")[0]
                        : customStartTime,

                    end_time: selectedSlot
                        ? selectedSlot.split("-")[1]
                        : customEndTime
                }
            )
            .then((response) => {

                alert(JSON.stringify(response.data));

            })
            .catch((error) => {

                console.log(error);

                alert("Error while submitting");

            });

        };
        
        const handleCheckAvailability = () => {

            api.post(
                "/check-availability",
                {
                    room_id: roomId,
                    booking_date: bookingDate,
                    start_time: customStartTime,
                    end_time: customEndTime
                }
            )
            .then((response) => {

                if (response.data.available) {

                    alert("✅ Room Available");

                }
                else {

                    alert("❌ Room Not Available");

                    api.post(
                        "/alternative-room",
                        {
                            participant_count: Number(participants),
                            booking_date: bookingDate,
                            start_time: customStartTime,
                            end_time: customEndTime
                        }
                    )
                    .then((altResponse) => {

                        setAlternativeRoom(
                            altResponse.data
                        );

                    });

                }

            });

        };

        /*{
            alternativeRoom && (

                <div
                    className="alert alert-info mt-3"
                >

                    <h5>
                        Alternative Room Found
                    </h5>

                    <p>
                        Room:
                        {" "}
                        {alternativeRoom.resource_name}
                    </p>

                    <p>
                        Capacity:
                        {" "}
                        {alternativeRoom.capacity}
                    </p>

                    <button
                        className="btn btn-success"
                        onClick={() => {

                            alert(
                                "Alternative Room Accepted"
                            );

                        }}
                    >
                        Accept Alternative Room
                    </button>

                </div>

            )
        }
*/

    {
        alternativeRoom && (

            <div
                className="card mt-3 p-3"
            >

                <h5>
                    Suggested Alternative Room
                </h5>

                <p>
                    Room:
                    {" "}
                    {alternativeRoom.resource_name}
                </p>

                <p>
                    Room Number:
                    {" "}
                    {alternativeRoom.room_number}
                </p>

                <p>
                    Capacity:
                    {" "}
                    {alternativeRoom.capacity}
                </p>

                <button
                    className="btn btn-success me-2"
                    onClick={() => {

                        alert(
                            "Alternative Room Accepted"
                        );

                    }}
                >
                    Accept Alternative
                </button>

                <button
                    className="btn btn-danger"
                    onClick={() => {

                    api.post(
                        "/send-notification",
                        {
                            case_id: 1,
                            receiver_id: "FAC002",
                            receiver_role: "Faculty",
                            message:
                                "Another user requested your booked slot."
                        }
                    )
                    .then((response) => {

                        alert(response.data.message);

                    });

                    }}
                >
                    Reject Alternative
                </button>

            </div>

        )
    }
    return (

        <div style={{ display: "flex" }}>

            <Sidebar />

            <div
                style={{
                    padding: "20px",
                    flex: 1
                }}
            >

                <h1>Book Room</h1>

                <h3>
                    Room ID: {roomId}
                </h3>

                <br />

                <label>
                    Booking Date
                </label>

                <input
                    type="date"
                    className="form-control"
                    value={bookingDate}
                    onChange={(e) => {
                        setBookingDate(e.target.value);
                    }}
                />

                <br />


                <label>
                    Event Name
                </label>

                <input
                    type="text"
                    className="form-control"
                    value={eventName}
                    onChange={(e) =>
                        setEventName(e.target.value)
                    }
                />

                <br />

                <label>
                    Event Category
                </label>

                <select
                    className="form-control"
                    value={eventCategory}
                    onChange={(e) => {

                        setEventCategory(
                            e.target.value
                        );

                    }}
                >

                    <option value="">
                        Select Category
                    </option>

                    <option value="Placement">
                        Placement
                    </option>

                    <option value="Workshop">
                        Workshop
                    </option>

                    <option value="Seminar">
                        Seminar
                    </option>

                    <option value="Club Activity">
                        Club Activity
                    </option>

                </select>

                <br />

                

                <br />

                <label>
                    Participants
                </label>

                <input
                    type="number"
                    min="1"
                    className="form-control"
                    value={participants}
                    onChange={(e) => {

                        setParticipants(
                            e.target.value
                        );

                    }}
                />

                <br />


                


                <h4>
                    Available Slots
                </h4>

                {
                    availableSlots.map((slot) => (

                        <button
                            key={slot}
                            className={
                                selectedSlot === slot
                                ? "btn btn-primary m-2"
                                : "btn btn-success m-2"
                            }
                            onClick={() => {

                                setSelectedSlot(slot);

                            }}
                        >
                            {slot}
                        </button>

                    ))
                }
                {
                    selectedSlot && (

                        <h5>

                            Selected Slot:
                            {" "}
                            {selectedSlot}

                        </h5>

                    )
                }
                <br />


                <hr />

                <h4>
                    Need Another Time?
                </h4>

                <label>
                    Custom Start Time
                </label>

                <input
                    type="time"
                    className="form-control"
                    value={customStartTime}
                    onChange={(e) => {

                        setCustomStartTime(
                            e.target.value
                        );

                    }}
                />

                <br />

                <label>
                    Custom End Time
                </label>

                <input
                    type="time"
                    className="form-control"
                    value={customEndTime}
                    onChange={(e) => {

                        setCustomEndTime(
                            e.target.value
                        );

                    }}
                />

                <br />

                <button
                    className="btn btn-warning"
                    onClick={handleCheckAvailability}
                >
                    Check Availability
                </button>

                <br />
                <br />
                
                <button
                    className="btn btn-primary"
                    onClick={handleSubmit}
                >
                    Submit Booking Request
                </button>

            </div>

        </div>

    );
}

export default BookRoom;