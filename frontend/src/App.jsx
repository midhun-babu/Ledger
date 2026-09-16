import React, { useState, useEffect } from 'react';
import { Search, Activity, BookOpen, Clock, FileText, Database, Settings } from 'lucide-react';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [casePath, setCasePath] = useState('');
  const [timeline, setTimeline] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchTimeline = async () => {
    if (!casePath) return;
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:8000/api/timeline?case_path=${encodeURIComponent(casePath)}`);
      const data = await res.json();
      if (!data.error) {
        setTimeline(data);
      }
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-title">
          <Activity size={24} color="var(--accent)" />
          ForensicAI
        </div>
        
        <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          <div 
            className={`nav-item ${activeTab === 'dashboard' ? 'active' : ''}`}
            onClick={() => setActiveTab('dashboard')}
          >
            <BookOpen size={20} /> Dashboard
          </div>
          <div 
            className={`nav-item ${activeTab === 'timeline' ? 'active' : ''}`}
            onClick={() => setActiveTab('timeline')}
          >
            <Clock size={20} /> Timeline
          </div>
          <div 
            className={`nav-item ${activeTab === 'insights' ? 'active' : ''}`}
            onClick={() => setActiveTab('insights')}
          >
            <Search size={20} /> AI Insights
          </div>
          <div 
            className={`nav-item ${activeTab === 'report' ? 'active' : ''}`}
            onClick={() => setActiveTab('report')}
          >
            <FileText size={20} /> Final Report
          </div>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <header className="header">
          <h1>{activeTab.charAt(0).toUpperCase() + activeTab.slice(1)}</h1>
          
          <div className="case-input">
            <Database size={20} color="var(--text-muted)" />
            <input 
              type="text" 
              placeholder="Case Folder Path (e.g., C:/cases/case_01)" 
              value={casePath}
              onChange={(e) => setCasePath(e.target.value)}
            />
            <button onClick={fetchTimeline}>Load</button>
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
                <span className="stat-label">Active Hypotheses</span>
                <span className="stat-value">--</span>
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
              <p style={{ color: 'var(--text-muted)' }}>AI Assistant is standing by. Enter a case path to load database.</p>
            </div>
          </div>
        )}

        {activeTab === 'timeline' && (
          <div className="glass-panel">
            {loading ? (
              <p>Loading timeline data...</p>
            ) : timeline.length > 0 ? (
              <div className="timeline-container">
                {timeline.map((event, i) => (
                  <div key={i} className="timeline-event">
                    <div className="event-time">{new Date(event.timestamp).toLocaleString()}</div>
                    <div className="event-source">{event.source}</div>
                    <div className="event-details">{event.event_type} - {JSON.stringify(event.details)}</div>
                  </div>
                ))}
              </div>
            ) : (
              <p style={{ color: 'var(--text-muted)' }}>No timeline events loaded.</p>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
