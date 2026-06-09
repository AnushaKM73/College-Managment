import { useEffect, useState } from "react";

import api from "../services/api";

import SummaryCard from "../components/SummaryCard";

function Dashboard() {

    const [summary, setSummary] = useState({});

    useEffect(() => {

        api.get("/workflow-summary")
            .then((response) => {

                setSummary(
                    response.data
                );

            })
            .catch((error) => {

                console.log(error);

            });

    }, []);

    return (

        <div>

            <h1>
                Smart Resource Allocation Dashboard
            </h1>

            <div
                className="d-flex gap-3 mt-4 flex-wrap"
            >

                <SummaryCard
                    title="Approved"
                    value={summary.approved_cases}
                />

                <SummaryCard
                    title="Rejected"
                    value={summary.rejected_cases}
                />

                <SummaryCard
                    title="Pending"
                    value={summary.pending_cases}
                />

                <SummaryCard
                    title="Resolved"
                    value={summary.resolved_cases}
                />

                <SummaryCard
                    title="Notifications"
                    value={summary.notifications}
                />

            </div>

        </div>

    );
}

export default Dashboard;