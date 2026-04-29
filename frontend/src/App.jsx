import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from "recharts";

import MetricCard from "./components/MetricCard.jsx";
import {
  getSummary,
  getTechnologyAdoption,
  getRegionalUsage,
  getIntegrationHealth
} from "./services/api.js";

export default function App() {
  const [summary, setSummary] = useState(null);
  const [adoption, setAdoption] = useState([]);
  const [regionalUsage, setRegionalUsage] = useState([]);
  const [integrations, setIntegrations] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadDashboard() {
      try {
        const [summaryData, adoptionData, regionalData, integrationData] =
          await Promise.all([
            getSummary(),
            getTechnologyAdoption(),
            getRegionalUsage(),
            getIntegrationHealth()
          ]);

        setSummary(summaryData);
        setAdoption(adoptionData);
        setRegionalUsage(regionalData);
        setIntegrations(integrationData);
      } catch (err) {
        setError("Could not load dashboard. Make sure the FastAPI backend is running.");
      }
    }

    loadDashboard();
  }, []);

  if (error) {
    return <main className="container"><p className="error">{error}</p></main>;
  }

  if (!summary) {
    return <main className="container"><p>Loading dashboard...</p></main>;
  }

  return (
    <main className="container">
      <section className="hero">
        <p className="eyebrow">Portfolio Project</p>
        <h1>Media Technology Footprint Tracker</h1>
        <p>
          A synthetic internal analytics platform for tracking technology adoption,
          regional usage and integration health across media products.
        </p>
      </section>

      <section className="metrics-grid">
        <MetricCard label="Technologies" value={summary.total_technologies} />
        <MetricCard label="Products" value={summary.total_products} />
        <MetricCard label="Usage Events" value={summary.total_usage_events} />
        <MetricCard label="Active Users" value={summary.total_active_users.toLocaleString()} />
        <MetricCard label="Top Technology" value={summary.highest_adoption_technology} />
        <MetricCard label="Top Region" value={summary.top_region} />
      </section>

      <section className="card">
        <h2>Technology Adoption</h2>
        <ResponsiveContainer width="100%" height={320}>
          <BarChart data={adoption}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="technology" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="active_users" />
          </BarChart>
        </ResponsiveContainer>
      </section>

      <section className="card">
        <h2>Playback Hours by Technology</h2>
        <ResponsiveContainer width="100%" height={320}>
          <LineChart data={adoption}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="technology" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="playback_hours" />
          </LineChart>
        </ResponsiveContainer>
      </section>

      <section className="card">
        <h2>Regional Usage</h2>
        <table>
          <thead>
            <tr>
              <th>Region</th>
              <th>Platform</th>
              <th>Active Users</th>
              <th>Playback Hours</th>
            </tr>
          </thead>
          <tbody>
            {regionalUsage.slice(0, 10).map((row, index) => (
              <tr key={`${row.region}-${row.platform}-${index}`}>
                <td>{row.region}</td>
                <td>{row.platform}</td>
                <td>{row.active_users.toLocaleString()}</td>
                <td>{row.playback_hours.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section className="card">
        <h2>Integration Health</h2>
        <table>
          <thead>
            <tr>
              <th>Source</th>
              <th>Type</th>
              <th>Status</th>
              <th>Events Received</th>
              <th>Average Error Rate</th>
            </tr>
          </thead>
          <tbody>
            {integrations.map((row) => (
              <tr key={row.source_name}>
                <td>{row.source_name}</td>
                <td>{row.source_type}</td>
                <td>{row.status}</td>
                <td>{row.events_received}</td>
                <td>{row.average_error_rate}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </main>
  );
}
