import { Link } from "react-router-dom";
function Sidebar() {

    return (

        <div
            style={{
                width: "250px",
                height: "100vh",
                background: "#1e293b",
                color: "white",
                padding: "20px"
            }}
        >

            <h3>
                Student Portal
            </h3>

            <hr />

            <Link
                to="/"
                style={{
                    color: "white",
                    textDecoration: "none",
                    display: "block",
                    marginBottom: "20px"
                }}
            >
                Dashboard
            </Link>

            <Link
                to="/rooms"
                style={{
                    color: "white",
                    textDecoration: "none",
                    display: "block",
                    marginBottom: "20px"
                }}
            >
                Rooms
            </Link>

            <Link
                to="/requests"
                style={{
                    color: "white",
                    textDecoration: "none",
                    display: "block",
                    marginBottom: "20px"
                }}
            >
                My Requests
            </Link>

            <Link
                to="/notifications"
                style={{
                    color: "white",
                    textDecoration: "none",
                    display: "block",
                    marginBottom: "20px"
                }}
            >
                Notifications
            </Link>

        </div>

    );
}

export default Sidebar;