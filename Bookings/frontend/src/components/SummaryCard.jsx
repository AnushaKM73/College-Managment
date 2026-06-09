function SummaryCard({ title, value }) {

    return (
        <div
            className="card shadow p-3"
            style={{
                width: "220px"
            }}
        >
            <h5>{title}</h5>

            <h2>{value}</h2>
        </div>
    );
}

export default SummaryCard;