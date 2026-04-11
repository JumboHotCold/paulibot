import React from 'react';

/**
 * MapModule Component — Campus 2D Interactive Map
 * ==============================================
 * Displays the 2D representation of the campus map.
 */
export default function MapModule({ className = "" }) {
  return (
    <div className={`glass-card rounded-2xl flex flex-col h-full min-h-[300px] relative overflow-hidden bg-white shadow-lg border border-gray-200 ${className}`}>
      {/* Header */}
      <div className="absolute top-4 left-4 z-10 bg-white/90 backdrop-blur px-4 py-2 rounded-xl shadow border border-gray-200 flex flex-col pointer-events-none">
        <span className="text-xs text-spus-green font-bold uppercase tracking-wider">Campus Nav</span>
        <span className="text-sm font-semibold text-gray-800">Saint Paul University Surigao</span>
      </div>

      {/* Map Content */}
      <div className="absolute inset-0 w-full h-full p-4 overflow-auto bg-gray-50 flex items-center justify-center">
        {/* We use an img tag for the 2D map. In a more complex app, this could be a Leaflet map with markers. */}
        <div className="relative max-w-full max-h-full">
            <img 
              src="/images/2D_Mapping/ST.PAUL MAP.png" 
              alt="SPUS Campus Map" 
              className="object-contain rounded-xl shadow-md border border-gray-200 h-auto w-auto max-h-[80vh] md:max-h-full mx-auto"
            />
            {/* Example Hotspot/Pin, placed arbitrarily as an example.
                You can add absolute positioned markers if you want specific location highlights based on what was asked. */}
            {/* 
            <div className="absolute top-[50%] left-[50%] -translate-x-1/2 -translate-y-1/2 flex flex-col items-center animate-bounce">
               <span className="text-3xl">📍</span>
               <span className="bg-white px-2 py-1 text-xs font-bold rounded shadow">Location</span>
            </div> 
            */}
        </div>
      </div>
    </div>
  );
}
