import { useEffect, useMemo, useState } from "react";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Legend
} from "recharts";

import MetricCard from "./components/MetricCard.jsx";
import {
  getSummary,
  getTechnologyAdoption,
  getRegionalUsage,
  getIntegrationHealth,
  getUsageTrends,
  getTechnologies,
  getProducts
} from "./services/api.js";

const DEFAULT_FILTERS = {
  region: "",
  platform: "",
  technology: ""
};

function uniqueSorted(values) {
  return [...new Set(values.filter(Boolean))].sort((a, b) => a.localeCompare(b));
}

function formatNumber(value) {
  if (value === null || value === undefined) return "-";
  return value.toLocaleString();
}

function formatDecimal(value) {
  if (value === null || value === undefined) return "-";
  return Number(value).toLocaleString(undefined, { maximumFractionDigits: 2 });
}

function EmptyState({ message = "No data matches the selected filters." }) {
  return <p className="empty-state">{message}</p>;
}

export default function App() {
  const [summary, setSummary] = useState(null);
  const [adoption, setAdoption] = useState([]);
  const [regionalUsage, setRegionalUsage] = useState([]);
  const [integrations, setIntegrations] = useState([]);
  const [usageTrends, setUsageTrends] = useState([]);
  const [filters, setFilters] = useState(DEFAULT_FILTERS);
  const [filterOptions, setFilterOptions] = useState({
    regions: [],
    platforms: [],
    technologies: []
  });
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [error, setError] = useState("");

  const activeFilters = useMemo(
    () => Object.fromEntries(Object.entries(filters).filter(([, value]) => value)),
    [filters]
  );

  const activeFilterCount = Object.keys(activeFilters).length;

  useEffect(() => {
    let ignore = false;

    async function loadReferenceData() {
      try {
        const [productsData, technologiesData, integrationData] = await Promise.all([
          getProducts(),
          getTechnologies(),
          getIntegrationHealth()
        ]);

        if (ignore) return;

        setFilterOptions({
          regions: uniqueSorted(productsData.map((product) => product.region)),
          platforms: uniqueSorted(productsData.map((product) => product.platform)),
          technologies: uniqueSorted(technologiesData.map((technology) => technology.name))
        });
        setIntegrations(integrationData);
      } catch (err) {
        if (!ignore) {
          setError("Could not load dashboard reference data. Make sure the FastAPI backend is running.");
        }
      }
    }

    loadReferenceData();

    return () => {
      ignore = true;
    };
  }, []);

  useEffect(() => {
    let ignore = false;

    async function loadDashboard() {
      setError("");
      if (summary) {
        setIsRefreshing(true);
      } else {
        setIsLoading(true);
      }

      try {
        const [summaryData, adoptionData, regionalData, trendData] = await Promise.all([
          getSummary(activeFilters),
          getTechnologyAdoption(activeFilters),
          getRegionalUsage(activeFilters),
          getUsageTrends(activeFilters)
        ]);

        if (ignore) return;

        setSummary(summaryData);
        setAdoption(adoptionData);
        setRegionalUsage(regionalData);
        setUsageTrends(trendData);
      } catch (err) {
        if (!ignore) {
          setError("Could not load dashboard data. Make sure the FastAPI backend is running.");
        }
      } finally {
        if (!ignore) {
          setIsLoading(false);
          setIsRefreshing(false);
        }
      }
    }

    loadDashboard();

    return () => {
      ignore = true;
    };
  }, [activeFilters]);

  function handleFilterChange(event) {
    const { name, value } = event.target;
    setFilters((current) => ({ ...current, [name]: value }));
  }

  function clearFilters() {
    setFilters(DEFAULT_FILTERS);
  }

  if (isLoading && !summary) {
    return (
      <main className="container">
        <section className="hero compact-hero">
          <p className="eyebrow">Portfolio Project</p>
          <h1>Media Technology Footprint Tracker</h1>
        </section>
        <section className="state-card">Loading dashboard data...</section>
      </main>
    );
  }

  if (error && !summary) {
    return (
      <main className="container">
        <section className="hero compact-hero">
          <p className="eyebrow">Portfolio Project</p>
          <h1>Media Technology Footprint Tracker</h1>
        </section>
        <section className="state-card error-state">{error}</section>
      </main>
    );
  }

  return (
    <main className="container">
      <section className="hero dashboard-header">
        <div>
          <p className="eyebrow">Portfolio Project</p>
          <h1>Media Technology Footprint Tracker</h1>
          <p>
            A synthetic internal analytics platform for tracking technology adoption,
            regional usage and integration health across media products.
          </p>
        </div>
        <div className="header-stat">
          <span>{activeFilterCount}</span>
          <p>Active filters</p>
        </div>
      </section>

      <section className="toolbar">
        <div>
          <p className="eyebrow">Dashboard Controls</p>
          <h2>Analytics filters</h2>
        </div>
        <div className="filters-grid">
          <label>
            Region
            <select name="region" value={filters.region} onChange={handleFilterChange}>
              <option value="">All regions</option>
              {filterOptions.regions.map((region) => (
                <option key={region} value={region}>{region}</option>
              ))}
            </select>
          </label>
          <label>
            Platform
            <select name="platform" value={filters.platform} onChange={handleFilterChange}>
              <option value="">All platforms</option>
              {filterOptions.platforms.map((platform) => (
                <option key={platform} value={platform}>{platform}</option>
              ))}
            </select>
          </label>
          <label>
            Technology
            <select name="technology" value={filters.technology} onChange={handleFilterChange}>
              <option value="">All technologies</option>
              {filterOptions.technologies.map((technology) => (
                <option key={technology} value={technology}>{technology}</option>
              ))}
            </select>
          </label>
          <button type="button" onClick={clearFilters} disabled={!activeFilterCount}>
            Clear filters
          </button>
        </div>
      </section>

      {error && <section className="inline-error">{error}</section>}
      {isRefreshing && <p className="refreshing-label">Refreshing dashboard...</p>}

      <section className="metrics-grid">
        <MetricCard label="Technologies" value={formatNumber(summary.total_technologies)} />
        <MetricCard label="Products" value={formatNumber(summary.total_products)} />
        <MetricCard label="Usage Events" value={formatNumber(summary.total_usage_events)} />
        <MetricCard label="Active Users" value={formatNumber(summary.total_active_users)} />
        <MetricCard label="Top Technology" value={summary.highest_adoption_technology || "-"} />
        <MetricCard label="Top Region" value={summary.top_region || "-"} />
      </section>

      <section className="dashboard-grid two-column">
        <section className="card chart-card wide-card">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Trend</p>
              <h2>Usage Trend</h2>
            </div>
            <span>{usageTrends.length} days</span>
          </div>
          {usageTrends.length ? (
            <ResponsiveContainer width="100%" height={320}>
              <LineChart data={usageTrends}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" tickFormatter={(value) => value.slice(5)} />
                <YAxis yAxisId="left" tickFormatter={(value) => value.toLocaleString()} />
                <YAxis yAxisId="right" orientation="right" tickFormatter={(value) => value.toLocaleString()} />
                <Tooltip />
                <Legend />
                <Line
                  yAxisId="left"
                  type="monotone"
                  dataKey="active_users"
                  name="Active users"
                  stroke="#2563eb"
                  strokeWidth={2}
                  dot={false}
                />
                <Line
                  yAxisId="right"
                  type="monotone"
                  dataKey="playback_hours"
                  name="Playback hours"
                  stroke="#059669"
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <EmptyState />
          )}
        </section>

        <section className="card chart-card">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Adoption</p>
              <h2>Technology Adoption</h2>
            </div>
          </div>
          {adoption.length ? (
            <ResponsiveContainer width="100%" height={320}>
              <BarChart data={adoption}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="technology" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="active_users" name="Active users" fill="#2563eb" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <EmptyState />
          )}
        </section>

        <section className="card chart-card">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Playback</p>
              <h2>Playback Hours by Technology</h2>
            </div>
          </div>
          {adoption.length ? (
            <ResponsiveContainer width="100%" height={320}>
              <LineChart data={adoption}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="technology" />
                <YAxis />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="playback_hours"
                  name="Playback hours"
                  stroke="#059669"
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <EmptyState />
          )}
        </section>
      </section>

      <section className="card table-card">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Regional</p>
            <h2>Regional Usage</h2>
          </div>
        </div>
        {regionalUsage.length ? (
          <div className="table-wrap">
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
                    <td>{formatNumber(row.active_users)}</td>
                    <td>{formatDecimal(row.playback_hours)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <EmptyState />
        )}
      </section>

      <section className="card table-card">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Sources</p>
            <h2>Integration Health</h2>
          </div>
        </div>
        {integrations.length ? (
          <div className="table-wrap">
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
                    <td><span className="status-pill">{row.status}</span></td>
                    <td>{formatNumber(row.events_received)}</td>
                    <td>{row.average_error_rate}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <EmptyState message="Integration health data is not available." />
        )}
      </section>
    </main>
  );
}
