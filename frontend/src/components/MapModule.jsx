/**
 * MapModule Component — Campus Map Placeholder
 * ==============================================
 * Placeholder for future Leaflet.js interactive campus map.
 * Displays a premium "Coming Soon" card with SPUS gold accents.
 */

export default function MapModule() {
  return (
    <div className="glass-card rounded-2xl p-6 flex flex-col items-center justify-center h-full min-h-[300px] relative overflow-hidden">
      {/* Background shimmer */}
      <div className="absolute inset-0 map-shimmer rounded-2xl" />

      {/* Content */}
      <div className="relative z-10 flex flex-col items-center text-center gap-4">
        {/* Floating map icon */}
        <div className="animate-float">
          <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-spus-green/15 to-spus-gold/10 border border-glass-border flex items-center justify-center">
            <svg viewBox="0 0 24 24" width="40" height="40" fill="none" stroke="currentColor" strokeWidth="1.5" className="text-spus-gold">
              <path strokeLinecap="round" strokeLinejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
            </svg>
          </div>
        </div>

        {/* Title */}
        <div>
          <h3 className="text-lg font-semibold text-gradient-gold mb-1" style={{ fontFamily: 'var(--font-family-heading)' }}>
            Campus Map
          </h3>
          <p className="text-sm text-text-secondary font-light">Coming Soon</p>
        </div>

        {/* Description */}
        <p className="text-xs text-text-muted max-w-[220px] leading-relaxed">
          An interactive map of Saint Paul University Surigao with building locations,
          offices, and navigation — powered by Leaflet.js.
        </p>

        {/* Status badge */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full border border-spus-gold/20 bg-spus-gold/5">
          <span className="w-1.5 h-1.5 rounded-full bg-spus-gold animate-pulse" />
          <span className="text-[0.65rem] text-spus-gold-300 font-medium uppercase tracking-wider">
            In Development
          </span>
        </div>
      </div>

      {/* Decorative grid */}
      <div
        className="absolute inset-0 opacity-[0.03] pointer-events-none"
        style={{
          backgroundImage:
            'linear-gradient(rgba(197,160,89,0.5) 1px, transparent 1px), linear-gradient(90deg, rgba(197,160,89,0.5) 1px, transparent 1px)',
          backgroundSize: '40px 40px',
        }}
      />
    </div>
  );
}
