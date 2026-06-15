import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  Activity,
  AlertTriangle,
  Bot,
  Download,
  Globe,
  Play,
  RefreshCw,
  ShieldCheck,
} from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import "./styles.css";

const API_BASE_URL = "https://web-security-assessment-platform.onrender.com/api";

function App() {
  const [targetUrl, setTargetUrl] = useState("https://example.com");
  const [includeNetworkScan, setIncludeNetworkScan] = useState(false);
  const [scans, setScans] = useState([]);
  const [stats, setStats] = useState(null);
  const [selectedScan, setSelectedScan] = useState(null);
  const [assistant, setAssistant] = useState(null);
  const [isScanning, setIsScanning] = useState(false);
  const [message, setMessage] = useState("");

  async function loadDashboard() {
    const [scanResponse, statsResponse] = await Promise.all([
      fetch(`${API_BASE_URL}/scans`),
      fetch(`${API_BASE_URL}/scans/stats/summary`),
    ]);

    const scanData = await scanResponse.json();
    const statsData = await statsResponse.json();
    setScans(scanData);
    setStats(statsData);

    if (scanData.length > 0 && !selectedScan) {
      await loadScan(scanData[0].id);
    }
  }

  async function loadScan(scanId) {
    const [scanResponse, assistantResponse] = await Promise.all([
      fetch(`${API_BASE_URL}/scans/${scanId}`),
      fetch(`${API_BASE_URL}/scans/${scanId}/assistant`),
    ]);

    setSelectedScan(await scanResponse.json());
    setAssistant(await assistantResponse.json());
  }

  async function startScan(event) {
    event.preventDefault();
    setIsScanning(true);
    setMessage("Running assessment...");

    try {
      const response = await fetch(`${API_BASE_URL}/scans`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          target_url: targetUrl,
          include_network_scan: includeNetworkScan,
        }),
      });

      if (!response.ok) {
        throw new Error("The backend rejected the scan request.");
      }

      const scan = await response.json();
      await loadDashboard();
      await loadScan(scan.id);
      setMessage("Assessment completed.");
    } catch (error) {
      setMessage(error.message);
    } finally {
      setIsScanning(false);
    }
  }

  useEffect(() => {
    loadDashboard().catch(() => {
      setMessage("Backend is not reachable. Start FastAPI on port 8000.");
    });
  }, []);

  const chartData = useMemo(() => {
    if (!stats?.risk_counts) return [];
    return Object.entries(stats.risk_counts).map(([name, value]) => ({ name, value }));
  }, [stats]);

  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-100">
      <section className="border-b border-zinc-800 bg-zinc-950">
        <div className="mx-auto flex max-w-7xl flex-col gap-6 px-5 py-6 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <div className="flex items-center gap-3 text-sm text-emerald-300">
              <ShieldCheck size={18} />
              <span>Product Security Assessment Console</span>
            </div>
            <h1 className="mt-3 text-3xl font-semibold tracking-normal text-white">
              Web Security Assessment Platform
            </h1>
          </div>

          <form onSubmit={startScan} className="grid gap-3 rounded border border-zinc-800 bg-zinc-900 p-4 lg:w-[560px]">
            <label className="text-sm text-zinc-300" htmlFor="target-url">
              Target URL
            </label>
            <div className="flex flex-col gap-3 sm:flex-row">
              <input
                id="target-url"
                className="min-w-0 flex-1 rounded border border-zinc-700 bg-zinc-950 px-3 py-2 text-sm outline-none focus:border-emerald-400"
                value={targetUrl}
                onChange={(event) => setTargetUrl(event.target.value)}
                placeholder="https://example.com"
              />
              <button
                className="inline-flex items-center justify-center gap-2 rounded bg-emerald-500 px-4 py-2 text-sm font-medium text-zinc-950 hover:bg-emerald-400 disabled:cursor-not-allowed disabled:opacity-60"
                disabled={isScanning}
                type="submit"
              >
                {isScanning ? <RefreshCw className="animate-spin" size={16} /> : <Play size={16} />}
                Start
              </button>
            </div>
            <label className="flex items-center gap-2 text-sm text-zinc-300">
              <input
                type="checkbox"
                checked={includeNetworkScan}
                onChange={(event) => setIncludeNetworkScan(event.target.checked)}
              />
              Include authorized Nmap reconnaissance
            </label>
            {message && <p className="text-sm text-amber-300">{message}</p>}
          </form>
        </div>
      </section>

      <section className="mx-auto grid max-w-7xl gap-4 px-5 py-5 md:grid-cols-4">
        <Metric label="Total scans" value={stats?.total_scans ?? 0} icon={<Activity size={18} />} />
        <Metric label="Completed" value={stats?.completed_scans ?? 0} icon={<ShieldCheck size={18} />} />
        <Metric label="Failed" value={stats?.failed_scans ?? 0} icon={<AlertTriangle size={18} />} />
        <Metric label="Selected risk" value={selectedScan?.risk_level ?? "none"} icon={<Globe size={18} />} />
      </section>

      <section className="mx-auto grid max-w-7xl gap-5 px-5 pb-8 lg:grid-cols-[360px_1fr]">
        <aside className="rounded border border-zinc-800 bg-zinc-900">
          <div className="flex items-center justify-between border-b border-zinc-800 px-4 py-3">
            <h2 className="text-sm font-semibold text-zinc-100">Scan History</h2>
            <button
              className="rounded p-2 text-zinc-300 hover:bg-zinc-800"
              onClick={loadDashboard}
              title="Refresh scans"
            >
              <RefreshCw size={16} />
            </button>
          </div>
          <div className="max-h-[620px] overflow-auto">
            {scans.map((scan) => (
              <button
                key={scan.id}
                onClick={() => loadScan(scan.id)}
                className={`block w-full border-b border-zinc-800 px-4 py-3 text-left text-sm hover:bg-zinc-800 ${
                  selectedScan?.id === scan.id ? "bg-zinc-800" : ""
                }`}
              >
                <span className="block truncate font-medium text-white">{scan.target_url}</span>
                <span className="mt-1 block text-zinc-400">
                  #{scan.id} · {scan.status} · {scan.risk_level}
                </span>
              </button>
            ))}
          </div>
        </aside>

        <div className="grid gap-5">
          <section className="grid gap-5 xl:grid-cols-[1fr_360px]">
            <div className="rounded border border-zinc-800 bg-zinc-900 p-4">
              <div className="mb-4 flex items-center justify-between gap-3">
                <h2 className="text-sm font-semibold">Findings</h2>
                {selectedScan?.report_path && (
                  <a
                    className="inline-flex items-center gap-2 rounded border border-zinc-700 px-3 py-2 text-sm text-zinc-200 hover:bg-zinc-800"
                    href={`${API_BASE_URL}/scans/${selectedScan.id}/report`}
                  >
                    <Download size={16} />
                    Report
                  </a>
                )}
              </div>

              {!selectedScan && <p className="text-sm text-zinc-400">Run or select a scan to view results.</p>}

              {selectedScan?.findings?.map((finding) => (
                <article key={finding.id} className="mb-3 rounded border border-zinc-800 bg-zinc-950 p-4">
                  <div className="flex flex-wrap items-center gap-2">
                    <SeverityBadge severity={finding.severity} />
                    <h3 className="text-sm font-semibold text-white">{finding.title}</h3>
                  </div>
                  <p className="mt-2 text-sm text-zinc-300">{finding.description}</p>
                  <p className="mt-2 text-sm text-zinc-500">{finding.recommendation}</p>
                </article>
              ))}
            </div>

            <div className="grid gap-5">
              <div className="rounded border border-zinc-800 bg-zinc-900 p-4">
                <h2 className="mb-4 text-sm font-semibold">Risk Distribution</h2>
                <div className="h-56">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#3f3f46" />
                      <XAxis dataKey="name" stroke="#a1a1aa" />
                      <YAxis allowDecimals={false} stroke="#a1a1aa" />
                      <Tooltip />
                      <Bar dataKey="value" fill="#34d399" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              <div className="rounded border border-zinc-800 bg-zinc-900 p-4">
                <div className="mb-3 flex items-center gap-2">
                  <Bot size={18} className="text-sky-300" />
                  <h2 className="text-sm font-semibold">Security Assistant</h2>
                </div>
                <p className="text-sm text-zinc-300">{assistant?.summary ?? "Assistant output appears after a scan."}</p>
                <ul className="mt-3 grid gap-2 text-sm text-zinc-400">
                  {assistant?.remediation_plan?.map((item) => (
                    <li key={item} className="rounded border border-zinc-800 bg-zinc-950 p-3">
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </section>

          <section className="rounded border border-zinc-800 bg-zinc-900 p-4">
            <h2 className="mb-3 text-sm font-semibold">Network Services</h2>
            <div className="grid gap-2 md:grid-cols-2 xl:grid-cols-3">
              {selectedScan?.network_services?.map((service) => (
                <div key={service.id} className="rounded border border-zinc-800 bg-zinc-950 p-3 text-sm">
                  <span className="font-semibold text-white">
                    {service.port}/{service.protocol}
                  </span>
                  <span className="ml-2 text-zinc-400">{service.service_name}</span>
                </div>
              ))}
              {selectedScan && selectedScan.network_services.length === 0 && (
                <p className="text-sm text-zinc-400">No open services stored for this scan.</p>
              )}
            </div>
          </section>
        </div>
      </section>
    </main>
  );
}

function Metric({ label, value, icon }) {
  return (
    <div className="rounded border border-zinc-800 bg-zinc-900 p-4">
      <div className="flex items-center justify-between text-zinc-400">
        <span className="text-sm">{label}</span>
        {icon}
      </div>
      <p className="mt-3 text-2xl font-semibold text-white">{value}</p>
    </div>
  );
}

function SeverityBadge({ severity }) {
  const colors = {
    critical: "border-red-400 text-red-300",
    high: "border-orange-400 text-orange-300",
    medium: "border-amber-400 text-amber-300",
    low: "border-sky-400 text-sky-300",
    info: "border-zinc-500 text-zinc-300",
  };

  return (
    <span className={`rounded border px-2 py-1 text-xs uppercase ${colors[severity] ?? colors.info}`}>
      {severity}
    </span>
  );
}

createRoot(document.getElementById("root")).render(<App />);
