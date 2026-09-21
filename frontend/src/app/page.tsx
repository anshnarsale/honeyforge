"use client";

import { useEffect, useState } from "react";

interface HoneyEvent {
  id: string;
  service: string;
  source_ip: string;
  event_type: string;
  timestamp: string;
}

interface Honeypot {
  id: string;
  name: string;
  service_type: string;
  port: number;
  banner: string | null;
  hostname: string | null;
  status: string;
  pid: number | null;
}

const API = "http://127.0.0.1:8000";

export default function Home() {
  const [events, setEvents] = useState<HoneyEvent[]>([]);
  const [honeypots, setHoneypots] = useState<Honeypot[]>([]);
  const [name, setName] = useState("");
  const [serviceType, setServiceType] = useState("http");
  const [port, setPort] = useState("8080");
  const [banner, setBanner] = useState("");
  const [hostname, setHostname] = useState("");
  const [error, setError] = useState<string | null>(null);

  const loadData = () => {
    fetch(`${API}/api/events/`).then((r) => r.json()).then(setEvents).catch(() => setError("Could not reach API"));
    fetch(`${API}/api/honeypots/`).then((r) => r.json()).then(setHoneypots).catch(() => setError("Could not reach API"));
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 5000);
    return () => clearInterval(interval);
  }, []);

  const createHoneypot = async () => {
    setError(null);
    const res = await fetch(`${API}/api/honeypots/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, service_type: serviceType, port: parseInt(port), banner: banner || null, hostname: hostname || null }),
    });
    if (!res.ok) {
      const data = await res.json();
      setError(data.detail || "Failed to create honeypot");
      return;
    }
    setName("");
    setBanner("");
    setHostname("");
    loadData();
  };

  const startHoneypot = async (id: string) => {
    await fetch(`${API}/api/honeypots/${id}/start`, { method: "POST" });
    loadData();
  };

  const stopHoneypot = async (id: string) => {
    await fetch(`${API}/api/honeypots/${id}/stop`, { method: "POST" });
    loadData();
  };

  const deleteHoneypot = async (id: string) => {
    await fetch(`${API}/api/honeypots/${id}`, { method: "DELETE" });
    loadData();
  };

  const activeCount = honeypots.filter((h) => h.status === "running").length;
  const totalEvents = events.length;
  const uniqueSources = new Set(events.map((e) => e.source_ip)).size;
  const today = new Date().toDateString();
  const todaysEvents = events.filter((e) => new Date(e.timestamp).toDateString() === today).length;

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 font-mono p-8">
      <h1 className="text-xl font-semibold tracking-tight mb-1">HoneyForge</h1>
      <p className="text-zinc-500 text-sm mb-6">Forge deception. Observe attackers.</p>

      {error && <p className="text-red-400 text-sm mb-4">{error}</p>}

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-10 max-w-3xl">
        <div className="border border-zinc-800 rounded-md p-4">
          <p className="text-zinc-500 text-xs uppercase tracking-wide mb-1">Active Honeypots</p>
          <p className="text-2xl text-emerald-400">{activeCount}</p>
        </div>
        <div className="border border-zinc-800 rounded-md p-4">
          <p className="text-zinc-500 text-xs uppercase tracking-wide mb-1">Total Events</p>
          <p className="text-2xl">{totalEvents}</p>
        </div>
        <div className="border border-zinc-800 rounded-md p-4">
          <p className="text-zinc-500 text-xs uppercase tracking-wide mb-1">Today&apos;s Events</p>
          <p className="text-2xl">{todaysEvents}</p>
        </div>
        <div className="border border-zinc-800 rounded-md p-4">
          <p className="text-zinc-500 text-xs uppercase tracking-wide mb-1">Unique Sources</p>
          <p className="text-2xl">{uniqueSources}</p>
        </div>
      </div>

      <div className="mb-10 border border-zinc-800 rounded-md p-4 max-w-xl">
        <h2 className="text-sm text-zinc-400 mb-3 uppercase tracking-wide">Create Honeypot</h2>
        <div className="flex flex-col gap-2">
          <input className="bg-zinc-900 border border-zinc-800 rounded px-2 py-1 text-sm" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
          <select className="bg-zinc-900 border border-zinc-800 rounded px-2 py-1 text-sm" value={serviceType} onChange={(e) => setServiceType(e.target.value)}>
            <option value="http">HTTP</option>
            <option value="tcp">TCP</option>
            <option value="ssh">SSH</option>
          </select>
          <input className="bg-zinc-900 border border-zinc-800 rounded px-2 py-1 text-sm" placeholder="Port" value={port} onChange={(e) => setPort(e.target.value)} />
          <input className="bg-zinc-900 border border-zinc-800 rounded px-2 py-1 text-sm" placeholder="Banner (optional)" value={banner} onChange={(e) => setBanner(e.target.value)} />
          <input className="bg-zinc-900 border border-zinc-800 rounded px-2 py-1 text-sm" placeholder="Hostname (optional)" value={hostname} onChange={(e) => setHostname(e.target.value)} />
          <button className="bg-emerald-700 hover:bg-emerald-600 text-white text-sm rounded px-3 py-1.5 mt-2" onClick={createHoneypot}>
            Create
          </button>
        </div>
      </div>

      <div className="mb-10">
        <h2 className="text-sm text-zinc-400 mb-3 uppercase tracking-wide">Honeypots</h2>
        <table className="w-full text-sm border-collapse max-w-3xl">
          <thead>
            <tr className="text-left text-zinc-500 border-b border-zinc-800">
              <th className="py-2 pr-4">NAME</th>
              <th className="py-2 pr-4">TYPE</th>
              <th className="py-2 pr-4">PORT</th>
              <th className="py-2 pr-4">STATUS</th>
              <th className="py-2 pr-4">ACTIONS</th>
            </tr>
          </thead>
          <tbody>
            {honeypots.map((h) => (
              <tr key={h.id} className="border-b border-zinc-900">
                <td className="py-2 pr-4">{h.name}</td>
                <td className="py-2 pr-4 uppercase text-zinc-300">{h.service_type}</td>
                <td className="py-2 pr-4">{h.port}</td>
                <td className="py-2 pr-4">
                  <span className={h.status === "running" ? "text-emerald-400" : "text-zinc-500"}>
                    ● {h.status.toUpperCase()}
                  </span>
                </td>
                <td className="py-2 pr-4 flex gap-2">
                  {h.status === "running" ? (
                    <button className="text-red-400 hover:underline" onClick={() => stopHoneypot(h.id)}>Stop</button>
                  ) : (
                    <button className="text-emerald-400 hover:underline" onClick={() => startHoneypot(h.id)}>Start</button>
                  )}
                  <button className="text-zinc-500 hover:underline" onClick={() => deleteHoneypot(h.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {honeypots.length === 0 && <p className="text-zinc-600 text-sm mt-2">No honeypots yet.</p>}
      </div>

      <div>
        <h2 className="text-sm text-zinc-400 mb-3 uppercase tracking-wide">Recent Events</h2>
        <table className="w-full text-sm border-collapse">
          <thead>
            <tr className="text-left text-zinc-500 border-b border-zinc-800">
              <th className="py-2 pr-4">TIME</th>
              <th className="py-2 pr-4">SOURCE</th>
              <th className="py-2 pr-4">SERVICE</th>
              <th className="py-2 pr-4">EVENT</th>
            </tr>
          </thead>
          <tbody>
            {events.map((e) => (
              <tr key={e.id} className="border-b border-zinc-900 hover:bg-zinc-900/50">
                <td className="py-2 pr-4 text-zinc-400">{new Date(e.timestamp).toLocaleTimeString()}</td>
                <td className="py-2 pr-4">{e.source_ip}</td>
                <td className="py-2 pr-4 uppercase text-zinc-300">{e.service}</td>
                <td className="py-2 pr-4 text-zinc-300">{e.event_type}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {events.length === 0 && <p className="text-zinc-600 text-sm mt-2">No events yet.</p>}
      </div>
    </div>
  );
}
