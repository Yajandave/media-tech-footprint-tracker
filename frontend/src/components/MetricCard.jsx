export default function MetricCard({ label, value }) {
  return (
    <div className="metric-card">
      <p>{label}</p>
      <h2>{value}</h2>
    </div>
  );
}
