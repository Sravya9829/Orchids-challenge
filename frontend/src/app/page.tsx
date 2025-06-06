'use client';

import { useState, useEffect, useRef } from 'react';
import URLInput from '../components/URLInputs';
import CloneStatus from '../components/CloneStatus';
import PreviewPane from '../components/PreviewPane';
import { CloneResponse, CloneResult, CloneStatus as Status } from '../types';

export default function Home() {
  const [cloneResponse, setCloneResponse] = useState<CloneResponse | null>(null);
  const [cloneResult, setCloneResult] = useState<CloneResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const pollIntervalRef = useRef<NodeJS.Timeout | null>(null);

  // Poll for results when we have a job ID
  useEffect(() => {
    if (!cloneResponse) return;

    const pollResult = async () => {
      try {
        console.log(`🔍 Polling for job: ${cloneResponse.job_id}`);
        
        const { api } = await import('../utils/api');
        const result = await api.getCloneResult(cloneResponse.job_id);
        
        console.log(`📊 Job status: ${result.status}`);
        setCloneResult(result);
        setError(null);

        // Stop polling if completed or failed
        if (result.status === Status.COMPLETED || result.status === Status.FAILED) {
          setLoading(false);
          if (pollIntervalRef.current) {
            clearInterval(pollIntervalRef.current);
            pollIntervalRef.current = null;
          }
        }
      } catch (error) {
        console.error('❌ Failed to get clone result:', error);
        setError(error instanceof Error ? error.message : 'Unknown error');
        
        // Stop polling on persistent errors
        if (pollIntervalRef.current) {
          clearInterval(pollIntervalRef.current);
          pollIntervalRef.current = null;
        }
        setLoading(false);
      }
    };

    // Poll immediately
    pollResult();

    // Then poll every 3 seconds until complete
    pollIntervalRef.current = setInterval(pollResult, 3000);

    return () => {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
        pollIntervalRef.current = null;
      }
    };
  }, [cloneResponse]);

  const handleCloneStart = async (response: CloneResponse) => {
    console.log(`🚀 Clone started with job ID: ${response.job_id}`);
    setCloneResponse(response);
    setCloneResult(null);
    setLoading(true);
    setError(null);
  };

  const handleReset = () => {
    if (pollIntervalRef.current) {
      clearInterval(pollIntervalRef.current);
      pollIntervalRef.current = null;
    }
    setCloneResponse(null);
    setCloneResult(null);
    setLoading(false);
    setError(null);
  };

  return (
    <main className="min-h-screen relative overflow-hidden">
      {/* Flower Pattern Background */}
      <div className="absolute inset-0 z-0">
        <svg className="w-full h-full opacity-10" viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="flowerPattern" x="0" y="0" width="100" height="100" patternUnits="userSpaceOnUse">
              {/* Large Flower */}
              <g transform="translate(50, 50)">
                <circle cx="0" cy="-15" r="8" fill="#ec4899" opacity="0.6"/>
                <circle cx="10" cy="-7" r="8" fill="#f472b6" opacity="0.6"/>
                <circle cx="10" cy="7" r="8" fill="#ec4899" opacity="0.6"/>
                <circle cx="0" cy="15" r="8" fill="#f472b6" opacity="0.6"/>
                <circle cx="-10" cy="7" r="8" fill="#ec4899" opacity="0.6"/>
                <circle cx="-10" cy="-7" r="8" fill="#f472b6" opacity="0.6"/>
                <circle cx="0" cy="0" r="6" fill="#fde047" opacity="0.8"/>
              </g>
              
              {/* Small Flowers */}
              <g transform="translate(20, 20)">
                <circle cx="0" cy="-6" r="3" fill="#f472b6" opacity="0.4"/>
                <circle cx="4" cy="-3" r="3" fill="#ec4899" opacity="0.4"/>
                <circle cx="4" cy="3" r="3" fill="#f472b6" opacity="0.4"/>
                <circle cx="0" cy="6" r="3" fill="#ec4899" opacity="0.4"/>
                <circle cx="-4" cy="3" r="3" fill="#f472b6" opacity="0.4"/>
                <circle cx="-4" cy="-3" r="3" fill="#ec4899" opacity="0.4"/>
                <circle cx="0" cy="0" r="2" fill="#fde047" opacity="0.6"/>
              </g>
              
              <g transform="translate(80, 80)">
                <circle cx="0" cy="-6" r="3" fill="#ec4899" opacity="0.4"/>
                <circle cx="4" cy="-3" r="3" fill="#f472b6" opacity="0.4"/>
                <circle cx="4" cy="3" r="3" fill="#ec4899" opacity="0.4"/>
                <circle cx="0" cy="6" r="3" fill="#f472b6" opacity="0.4"/>
                <circle cx="-4" cy="3" r="3" fill="#ec4899" opacity="0.4"/>
                <circle cx="-4" cy="-3" r="3" fill="#f472b6" opacity="0.4"/>
                <circle cx="0" cy="0" r="2" fill="#fde047" opacity="0.6"/>
              </g>
              
              {/* Leaves */}
              <ellipse cx="25" cy="70" rx="3" ry="8" fill="#22c55e" opacity="0.3" transform="rotate(45 25 70)"/>
              <ellipse cx="75" cy="30" rx="3" ry="8" fill="#22c55e" opacity="0.3" transform="rotate(-45 75 30)"/>
              <ellipse cx="15" cy="40" rx="2" ry="6" fill="#16a34a" opacity="0.3" transform="rotate(30 15 40)"/>
              <ellipse cx="85" cy="60" rx="2" ry="6" fill="#16a34a" opacity="0.3" transform="rotate(-30 85 60)"/>
            </pattern>
          </defs>
          
          <rect width="100%" height="100%" fill="url(#flowerPattern)"/>
        </svg>
      </div>

      {/* Gradient Background Overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-pink-50 via-white to-rose-50 z-10"></div>

      {/* Content */}
      <div className="relative z-20 py-8">
        {!cloneResponse ? (
          <URLInput onCloneStart={handleCloneStart} loading={loading} />
        ) : (
          <div className="space-y-8">
            {error && (
              <div className="max-w-4xl mx-auto p-6">
                <div className="bg-rose-50 border border-rose-200 rounded-lg p-4">
                  <div className="flex items-center">
                    <div className="text-rose-400 mr-3">
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <div>
                      <h3 className="text-sm font-medium text-rose-800">Connection Error</h3>
                      <p className="text-sm text-rose-700 mt-1">{error}</p>
                    </div>
                  </div>
                  <div className="mt-4">
                    <button
                      onClick={handleReset}
                      className="text-sm bg-rose-100 text-rose-800 px-3 py-1 rounded hover:bg-rose-200 transition-colors"
                    >
                      Try Again
                    </button>
                  </div>
                </div>
              </div>
            )}
            
            {cloneResult && (
              <CloneStatus result={cloneResult} onReset={handleReset} />
            )}
            
            {cloneResult && cloneResult.status === Status.COMPLETED && (
              <PreviewPane result={cloneResult} />
            )}
          </div>
        )}
      </div>
    </main>
  );
}