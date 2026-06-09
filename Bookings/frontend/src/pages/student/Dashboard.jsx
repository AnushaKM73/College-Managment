import Sidebar from "../../components/Sidebar";

function Dashboard() {

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
                    Welcome Student
                </h1>

                <div
                    className="d-flex gap-3 mt-4"
                >

                    <div className="card p-3">
                        Total Requests
                        <h2>12</h2>
                    </div>

                    <div className="card p-3">
                        Approved
                        <h2>5</h2>
                    </div>

                    <div className="card p-3">
                        Pending
                        <h2>4</h2>
                    </div>

                    <div className="card p-3">
                        Rejected
                        <h2>3</h2>
                    </div>

                </div>

            </div>

        </div>

    );
}

export default Dashboard;