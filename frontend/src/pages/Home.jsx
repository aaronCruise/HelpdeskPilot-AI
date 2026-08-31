import './Home.css';

const TECH_BADGES = ['FastAPI', 'React', 'SQLite', 'ChromaDB', 'Gemini API'];

const FEATURES = [
  {
    title: 'AI Ticket Classification',
    description: 'Every incoming ticket is automatically categorized and prioritized.',
  },
  {
    title: 'Smart Recommendations',
    description: 'One click analyzes a ticket and suggests a fix using RAG over internal docs.',
  },
  {
    title: 'Equipment Tracking',
    description: 'Manage hardware inventory and track who has what checked out.',
  },
];

export function Home({ onEnter }) {
  return (
    <>
      <div className="hero">
        <h1>HelpdeskPilot AI</h1>
        <p className="hero-tagline">
          An AI-powered IT support assistant that classifies tickets and suggests fixes
          by retrieving answers from your own internal docs.
        </p>
        <div className="hero-actions">
          <button className="primary" onClick={onEnter}>Open Dashboard</button>
          <a href="https://github.com/aaronCruise/HelpdeskPilot-AI" target="_blank" rel="noreferrer">
            <button type="button">View on GitHub</button>
          </a>
        </div>
        <div className="badge-row">
          {TECH_BADGES.map((badge) => (
            <span className="badge" key={badge}>{badge}</span>
          ))}
        </div>
      </div>

      <div className="feature-grid">
        {FEATURES.map((feature) => (
          <div className="feature-card" key={feature.title}>
            <h3>{feature.title}</h3>
            <p>{feature.description}</p>
          </div>
        ))}
      </div>
    </>
  );
}
