import React, { useState, useEffect } from 'react';
import { Search, Activity, BookOpen, Clock, FileText, Database, Settings, AlertTriangle, Link } from 'lucide-react';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [casePath, setCasePath] = useState('');
  const [timeline, setTimeline] = useState([]);
  const [flags, setFlags] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filterType, setFilterType] = useState('all');

  const fetchTimeline = async () => {
    if (!casePath) return;
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:8000/api/timeline?case_path=${encodeURIComponent(casePath)}`);
      const data = await res.json();
      if (!data.error) setTimeline(data);
      
      const flagRes = await fetch(`http://localhost:8000/api/flags?case_path=${encodeURIComponent(casePath)}`);
      const flagData = await flagRes.json();
      if (!flagData.error) setFlags(flagData);
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  const filteredTimeline = timeline.filter(event => {
    if (filterType === 'all') return true;
    if (filterType === 'financial') return event.event_type === 'financial_transaction';
    if (filterType === 'dfir') return event.event_type !== 'financial_transaction';
    return true;
  });

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-title">
          <Activity size={24} color="var(--accent)" />
          ForensicAI
        </div>
        
        <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          <div className={`nav-item ${activeTab === 'dashboard' ? 'active' : ''}`} onClick={() => setActiveTab('dashboard')}>
            <BookOpen size={20} /> Dashboard
          </div>
          <div className={`nav-item ${activeTab === 'timeline' ? 'active' : ''}`} onClick={() => setActiveTab('timeline')}>
            <Clock size={20} /> Unified Timeline
          </div>
          <div className={`nav-item ${activeTab === 'flags' ? 'active' : ''}`} onClick={() => setActiveTab('flags')}>
            <AlertTriangle size={20} /> Anomaly Flags
          </div>
          <div className={`nav-item ${activeTab === 'insights' ? 'active' : ''}`} onClick={() => setActiveTab('insights')}>
            <Search size={20} /> AI Evidence Trace
          </div>
          <div className={`nav-item ${activeTab === 'report' ? 'active' : ''}`} onClick={() => setActiveTab('report')}>
            <FileText size={20} /> Final Report
          </div>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <header className="header">
          <h1>{activeTab.charAt(0).toUpperCase() + activeTab.slice(1).replace(/([A-Z])/g, ' $1').trim()}</h1>
          
          <div className="case-input">
            <Database size={20} color="var(--text-muted)" />
            <input 
              type="text" 
              placeholder="Case Folder Path (e.g., C:/cases/case_01)" 
              value={casePath}
              onChange={(e) => setCasePath(e.target.value)}
            />
            <button onClick={fetchTimeline}>Load Evidence</button>
          </div>
        </header>

        {activeTab === 'dashboard' && (
          <div>
            <div className="dashboard-grid">
              <div className="glass-panel stat-card">
                <span className="stat-label">Events Parsed</span>
                <span className="stat-value">{timeline.length || '--'}</span>
              </div>
              <div className="glass-panel stat-card">
                <span className="stat-label">Anomaly Flags Detected</span>
                <span className="stat-value">{flags.length || '--'}</span>
              </div>
              <div className="glass-panel stat-card">
                <span className="stat-label">Verified Findings</span>
                <span className="stat-value">--</span>
              </div>
            </div>
            
            <div className="glass-panel">
              <h2 style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Settings size={20} /> System Status
              </h2>
              <p style={{ color: 'var(--text-muted)' }}>Ready for dual-purpose DFIR + Financial ingestion.</p>
            </div>
          </div>
        )}

        {activeTab === 'timeline' && (
          <div className="glass-panel">
            <div style={{ marginBottom: '1.5rem', display: 'flex', gap: '1rem' }}>
              <button style={{ opacity: filterType === 'all' ? 1 : 0.5 }} onClick={() => setFilterType('all')}>All Events</button>
              <button style={{ opacity: filterType === 'dfir' ? 1 : 0.5 }} onClick={() => setFilterType('dfir')}>DFIR Only</button>
              <button style={{ opacity: filterType === 'financial' ? 1 : 0.5, backgroundColor: 'var(--success)' }} onClick={() => setFilterType('financial')}>Financial Only</button>
            </div>

            {loading ? (
              <p>Loading timeline data...</p>
            ) : filteredTimeline.length > 0 ? (
              <div className="timeline-container">
                {filteredTimeline.map((event, i) => (
                  <div key={i} className="timeline-event" style={{ borderLeft: event.event_type === 'financial_transaction' ? '3px solid var(--success)' : '3px solid var(--accent)' }}>
                    <div className="event-time">{new Date(event.timestamp).toLocaleString()}</div>
                    <div className="event-source" style={{ color: event.event_type === 'financial_transaction' ? 'var(--success)' : 'var(--warning)' }}>{event.source}</div>
                    <div className="event-details">{event.event_type} - {JSON.stringify(event.details)}</div>
                  </div>
                ))}
              </div>
            ) : (
              <p style={{ color: 'var(--text-muted)' }}>No timeline events matching filter.</p>
            )}
          </div>
        )}

        {activeTab === 'flags' && (
          <div className="glass-panel">
            {flags.length > 0 ? (
              <div className="timeline-container">
                {flags.map((flag, i) => (
                  <div key={i} className="timeline-event" style={{ borderLeft: '3px solid var(--danger)' }}>
                    <div className="event-time" style={{ color: 'var(--danger)' }}>{flag.severity} RISK</div>
                    <div className="event-source">{flag.rule_name}</div>
                    <div className="event-details">
                      <p>{flag.description}</p>
                      <p style={{ marginTop: '0.5rem', fontSize: '0.875rem', color: 'var(--accent)' }}>
                        <Link size={14} style={{ marginRight: '4px' }}/> 
                        Evidence Refs: {flag.evidence_refs}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p style={{ color: 'var(--text-muted)' }}>No anomalies detected yet. Try running the 'analyze' command.</p>
            )}
          </div>
        )}

        {activeTab === 'insights' && (
          <div className="glass-panel">
            <h2 style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
               Evidence Trace Panel
            </h2>
            <p style={{ color: 'var(--text-muted)' }}>
              (Work in Progress) When AI Findings are generated, you will be able to click on a finding here to view the specific timeline events and deterministic flags that support it, ensuring 100% traceability.
            </p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
