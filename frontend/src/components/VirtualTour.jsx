import React, { useRef, useState, useEffect } from 'react';
import { ReactPhotoSphereViewer } from 'react-photo-sphere-viewer';
import { MarkersPlugin } from '@photo-sphere-viewer/markers-plugin';
import '@photo-sphere-viewer/core/index.css';
import '@photo-sphere-viewer/markers-plugin/index.css';

// Define the nodes and their connections
const NODES = {
  'cafeteria': {
    id: 'cafeteria',
    name: 'Cafeteria Hallway',
    description: 'The main campus dining hall hallway.',
    top: '26.00%', 
    left: '78.35%',
    panorama: '/images/SmartVirtualTour/cafeteria_hallway_1.jpg',
    markers: [
      {
        id: 'to_church',
        longitude: '180deg',
        latitude: '0deg',
        html: '<div style="background: rgba(212,175,55,0.9); padding: 8px 12px; border-radius: 8px; color: white; cursor: pointer; font-weight: bold; border: 2px solid white; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">Go to Church Hallway ➔</div>',
        anchor: 'center center',
        tooltip: 'Walk to Church',
        style: { cursor: 'pointer' },
        data: { targetNode: 'church' }
      }
    ]
  },
  'church': {
    id: 'church',
    name: 'Church Hallway',
    description: 'The exterior hallway next to the chapel.',
    top: '33.53%',
    left: '52.29%',
    panorama: '/images/SmartVirtualTour/church_x_hallway__1.jpg',
    markers: [
      {
        id: 'to_cafeteria',
        longitude: '0deg',
        latitude: '0deg',
        html: '<div style="background: rgba(212,175,55,0.9); padding: 8px 12px; border-radius: 8px; color: white; cursor: pointer; font-weight: bold; border: 2px solid white; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">Go to Cafeteria Hallway ➔</div>',
        anchor: 'center center',
        tooltip: 'Walk to Cafeteria',
        style: { cursor: 'pointer' },
        data: { targetNode: 'cafeteria' }
      }
    ]
  },
  'main_entrance': {
    id: 'main_entrance',
    name: 'Main Entrance',
    description: 'The main gateway to the SPUS campus.',
    top: '47.63%',
    left: '84.11%',
    panorama: '/images/SmartVirtualTour/Main_Entrance.jpg',
    markers: []
  },
  'court': {
    id: 'court',
    name: 'Campus Court',
    description: 'The main sports and activity court.',
    top: '28.44%',
    left: '63.50%',
    panorama: '/images/SmartVirtualTour/COURT.jpg',
    markers: []
  }
};

export default function VirtualTour({ className = "" }) {
  const [viewMode, setViewMode] = useState('aerial'); // 'aerial' | '360'
  const [currentNodeId, setCurrentNodeId] = useState(null);
  const [hoveredNode, setHoveredNode] = useState(null);
  const [tappedNode, setTappedNode] = useState(null);
  const psvRef = useRef(null);

  // Update viewer when the node changes
  const currentNode = NODES[currentNodeId] || NODES['cafeteria'];

  // Handle marker clicks to traverse nodes
  const handleReady = (instance) => {
    psvRef.current = instance;
    const markersPlugin = instance.getPlugin(MarkersPlugin);
    
    if (markersPlugin) {
      markersPlugin.addEventListener('select-marker', ({ marker }) => {
        if (marker.config.data && marker.config.data.targetNode) {
          const nextNode = marker.config.data.targetNode;
          setCurrentNodeId(nextNode);
        }
      });
    }
  };

  // When node changes, we want the viewer to update its panorama and markers.
  // We can do this programmatically or just let React re-mount/update the component.
  // Using useEffect to update an existing instance is often smoother.
  useEffect(() => {
    if (psvRef.current) {
      const markersPlugin = psvRef.current.getPlugin(MarkersPlugin);
      
      // Update panorama
      psvRef.current.setPanorama(currentNode.panorama).then(() => {
        // Clear and add new markers
        if (markersPlugin) {
          markersPlugin.clearMarkers();
          currentNode.markers.forEach(m => markersPlugin.addMarker(m));
        }
      });
    }
  }, [currentNodeId]);

  const handleImageClickCoordLogger = (e) => {
    const rect = e.target.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const xPercent = ((x / rect.width) * 100).toFixed(2);
    const yPercent = ((y / rect.height) * 100).toFixed(2);
    
    console.log(`Node Coordinate -> top: '${yPercent}%', left: '${xPercent}%'`);
    alert(`Node Target Coordinates copied to console!\nTop: ${yPercent}%\nLeft: ${xPercent}%\n\nPaste these replacing the placeholder coordinates in VirtualTour.jsx NODES object.`);
  };

  // Handle node tap on mobile (toggle tooltip) or click to enter
  const handleNodeInteraction = (e, node) => {
    e.stopPropagation();
    // On mobile, first tap shows tooltip, second tap enters 360
    if ('ontouchstart' in window) {
      if (tappedNode === node.id) {
        // Second tap - enter 360 view
        setCurrentNodeId(node.id);
        setViewMode('360');
        setTappedNode(null);
      } else {
        // First tap - show tooltip
        setTappedNode(node.id);
        setHoveredNode(node.id);
      }
    } else {
      // Desktop - direct click enters 360
      setCurrentNodeId(node.id);
      setViewMode('360');
    }
  };

  // Clear tapped node when tapping elsewhere
  const handleContainerTap = (e) => {
    if (tappedNode) {
      setTappedNode(null);
      setHoveredNode(null);
    }
    handleImageClickCoordLogger(e);
  };

  if (viewMode === 'aerial') {
    return (
      <div className={`virtual-tour-container relative w-full h-full rounded-2xl overflow-hidden shadow-lg border border-gray-200 bg-[#E8EAE6] flex flex-col ${className}`}>
        {/* Header */}
        <div className="vt-header absolute top-3 left-3 z-10 bg-white/90 backdrop-blur px-3 py-1.5 rounded-xl shadow border border-gray-200 pointer-events-none">
          <span className="text-xs text-spus-green font-bold uppercase tracking-wider block">Smart Virtual Tour</span>
          <span className="vt-header-subtitle text-sm font-semibold text-gray-800">Select a Location</span>
        </div>

        {/* Aerial Image Container */}
        <div className="flex-1 w-full h-full relative flex items-center justify-center p-2 sm:p-4">
          <div className="relative w-full h-full flex items-center justify-center">
            <img 
              src="/images/SmartVirtualTour/SPUS_aerial_view.png" 
              alt="SPUS Aerial View" 
              className="vt-aerial-img max-h-full w-auto h-auto object-contain shadow-lg rounded-xl cursor-crosshair border border-gray-300"
              onClick={handleContainerTap}
            />

            {/* Render interactive nodes */}
            {Object.values(NODES).map(node => (
              <div 
                key={node.id}
                className="absolute -translate-x-1/2 -translate-y-1/2 flex flex-col items-center group cursor-pointer z-10"
                style={{ top: node.top, left: node.left }}
                onMouseEnter={() => setHoveredNode(node.id)}
                onMouseLeave={() => { if (tappedNode !== node.id) setHoveredNode(null); }}
                onClick={(e) => handleNodeInteraction(e, node)}
              >
                {/* Visual Pin */}
                <div className="relative">
                  <div className="absolute inset-0 bg-spus-gold rounded-full animate-ping opacity-75"></div>
                  <div className="vt-pin relative w-6 h-6 sm:w-7 sm:h-7 bg-spus-green border-2 sm:border-[3px] border-white rounded-full shadow-lg flex items-center justify-center text-white text-[10px] sm:text-xs font-bold ring-2 ring-spus-gold/50 hover:scale-110 transition-transform">
                    {node.id.charAt(0).toUpperCase()}
                  </div>
                </div>

                {/* Info Tooltip Hook into Hover */}
                <div className={`
                  vt-tooltip absolute top-8 sm:top-9 w-40 sm:w-48 bg-white/95 backdrop-blur shadow-xl rounded-xl p-2.5 sm:p-3 border border-gray-200/80 
                  transition-all duration-200 ease-out origin-top pointer-events-none z-20
                  ${(hoveredNode === node.id || tappedNode === node.id) ? 'opacity-100 scale-100 translate-y-0' : 'opacity-0 scale-95 -translate-y-2'}
                `}>
                   <h4 className="font-bold text-spus-green mb-1 text-xs sm:text-sm">{node.name}</h4>
                   <p className="text-[10px] sm:text-xs text-gray-600 leading-tight border-b border-gray-100 pb-2 mb-2">{node.description}</p>
                   <div className="flex items-center gap-2 text-[9px] sm:text-[10px] font-bold text-spus-gold uppercase tracking-wider">
                     <span>📸</span> {('ontouchstart' in window) ? 'Tap again to enter 360°' : 'Click to Enter 360°'}
                   </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  const plugins = [
    [MarkersPlugin, {
      markers: currentNode?.markers || []
    }]
  ];

  return (
    <div className={`virtual-tour-container relative w-full h-full rounded-2xl overflow-hidden shadow-lg border border-gray-200 ${className}`}>
      {/* Overlay header */}
      <div className="vt-header absolute top-3 left-3 z-10 bg-white/90 backdrop-blur px-3 py-1.5 rounded-xl shadow border border-gray-200 flex flex-col pointer-events-none">
        <span className="text-xs text-spus-gold font-bold uppercase tracking-wider">Smart Virtual Tour</span>
        <span className="vt-header-subtitle text-sm font-semibold text-gray-800">{currentNode?.name}</span>
      </div>

      <button 
        className="vt-back-btn absolute bottom-3 left-3 z-10 bg-white shadow py-2 px-3 sm:px-4 rounded-xl font-bold flex items-center gap-2 hover:bg-gray-50 border border-gray-200 text-sm"
        onClick={() => setViewMode('aerial')}
      >
        <span>🔙</span> <span className="vt-back-label">Back to Aerial View</span>
      </button>
      
      <ReactPhotoSphereViewer
        src={currentNode?.panorama}
        height="100%"
        width="100%"
        plugins={plugins}
        onReady={handleReady}
        navbar={['zoom', 'fullscreen']}
        defaultZoomLvl={30}
      />
    </div>
  );
}
