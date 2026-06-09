import { Link } from "react-router-dom";
import { useEffect, useState } from "react";

import Sidebar from "../../components/Sidebar";

import api from "../../services/api";

function Rooms() {

    const [rooms, setRooms] = useState([]);
    console.log(rooms);

    useEffect(() => {

        api.get(
            "http://127.0.0.1:5000/rooms"
        )
            .then((response) => {

                setRooms(
                    response.data
                );

            })
            .catch((error) => {

                console.log(
                    error
                );

            });

    }, []);
    

    return (

        <div
            style={{
                display: "flex"
            }}
        >

            <Sidebar />

            <div
                style={{
                    padding: "20px",
                    flex: 1
                }}
            >

                <h1>
                    Rooms
                </h1>
                <h3>Total Rooms: {rooms.length}</h3>
                <div
                    className="d-flex gap-3 flex-wrap"
                >

                    {
                        rooms.map((room) => (

                            <div
                                key={room.resource_id}
                                className="card p-3"
                                style={{
                                    width: "250px"
                                }}
                            >

                                <h4>
                                    {room.resource_name}
                                </h4>

                                <p>
                                    Capacity:
                                    {" "}
                                    {room.capacity}
                                </p>

                                <Link
                                    to={`/book-room/${room.resource_id}`}
                                    className="btn btn-primary"
                                >
                                    Book Room
                                </Link>

                            </div>

                        ))
                    }

                </div>

            </div>

        </div>

    );
}

export default Rooms;