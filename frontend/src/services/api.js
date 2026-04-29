const API_BASE = "http://127.0.0.1:8000";

export async function getSummary() {
  const response = await fetch(`${API_BASE}/analytics/summary`);
  if (!response.ok) throw new Error("Failed to fetch summary");
  return response.json();
}

export async function getTechnologyAdoption() {
  const response = await fetch(`${API_BASE}/analytics/technology-adoption`);
  if (!response.ok) throw new Error("Failed to fetch technology adoption");
  return response.json();
}

export async function getRegionalUsage() {
  const response = await fetch(`${API_BASE}/analytics/regional-usage`);
  if (!response.ok) throw new Error("Failed to fetch regional usage");
  return response.json();
}

export async function getIntegrationHealth() {
  const response = await fetch(`${API_BASE}/analytics/integration-health`);
  if (!response.ok) throw new Error("Failed to fetch integration health");
  return response.json();
}
