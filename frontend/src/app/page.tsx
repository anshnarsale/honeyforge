"use client";

import { useEffect, useState } from "react";

interface HoneyEvent {
  id: string;
  honeypot_id: string;
  service: string;
  source_ip: string;
  source_port: number | null;
  event_type: string;
  session_id: string | null;
  timestamp: string;
  event_metadata: Record<string, unknown> | null;
}

export default function Home() {
  const [events, setEvents] = useState<HoneyEvent[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/events/")
      .then((res) => res.json())
      .then((data) => setEvents(data))
      .catch(() => setError("Could not reach HoneyForge API"));
  }, []);

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 font-mono p-8">
      <h1 className="text-xl font-semibold tracking-tight mb-1">HoneyForge</h1>
      <p className="text-zinc-500 text-sm mb-6">Forge deception. Observe attackers.</p>

      {error && <p className="text-red-400 text-sm">{error}</p>}

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

      {events.length === 0 && !error && (
        <p className="text-zinc-600 text-sm mt-4">No events yet.</p>
      )}
    </div>
  );
}
