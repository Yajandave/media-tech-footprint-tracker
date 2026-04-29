const API_BASE = "http://127.0.0.1:8000";

function buildUrl(path, filters = {}) {
  const url = new URL(`${API_BASE}${path}`);

  Object.entries(filters).forEach(([key, value]) => {
    if (value) {
      url.searchParams.set(key, value);
    }
  });

  return url.toString();
}

async function fetchJson(path, filters, errorMessage) {
  const response = await fetch(buildUrl(path, filters));
  if (!response.ok) throw new Error(errorMessage);
  return response.json();
}

export async function getSummary(filters) {
  return fetchJson("/analytics/summary", filters, "Failed to fetch summary");
}

export async function getTechnologyAdoption(filters) {
  return fetchJson(
    "/analytics/technology-adoption",
    filters,
    "Failed to fetch technology adoption"
  );
}

export async function getRegionalUsage(filters) {
  return fetchJson("/analytics/regional-usage", filters, "Failed to fetch regional usage");
}

export async function getUsageTrends(filters) {
  return fetchJson("/analytics/usage-trends", filters, "Failed to fetch usage trends");
}

export async function getIntegrationHealth() {
  return fetchJson("/analytics/integration-health", undefined, "Failed to fetch integration health");
}

export async function getTechnologies() {
  return fetchJson("/technologies", undefined, "Failed to fetch technologies");
}

export async function getProducts() {
  return fetchJson("/products", undefined, "Failed to fetch products");
}
