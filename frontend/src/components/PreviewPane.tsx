'use client';

import { useState } from 'react';
import { CloneResult } from '../types';

interface PreviewPaneProps {
  result: CloneResult;
}

export default function PreviewPane({ result }: PreviewPaneProps) {
  const [viewMode, setViewMode] = useState<'side-by-side' | 'full-clone'>('full-clone');
  const [frameHeight, setFrameHeight] = useState(800);

  if (!result.cloned_html) {
    return null;
  }

  return (
    <div className="max-w-7xl mx-auto p-6">
      <div className="bg-white/80 backdrop-blur-sm rounded-xl shadow-xl overflow-hidden border border-pink-100">
        <div className="bg-gradient-to-r from-pink-500 to-rose-500 px-8 py-6 text-white">
          <h3 className="text-2xl font-bold mb-2">
            🌸 Beautiful Website Clone Preview
          </h3>
          <p className="text-pink-100">
            Original: {result.original_url}
          </p>
        </div>

        <div className="p-8">
          {/* Toggle View Buttons */}
          <div className="mb-8 flex justify-center">
            <div className="bg-white/60 p-1 rounded-lg border border-pink-200 shadow-sm">
              <button
                onClick={() => setViewMode('side-by-side')}
                className={`px-6 py-2 rounded-md text-sm font-medium transition-all ${
                  viewMode === 'side-by-side'
                    ? 'bg-gradient-to-r from-pink-500 to-rose-500 text-white shadow-sm'
                    : 'text-gray-600 hover:text-pink-600'
                }`}
              >
                Side by Side
              </button>
              <button
                onClick={() => setViewMode('full-clone')}
                className={`px-6 py-2 rounded-md text-sm font-medium transition-all ${
                  viewMode === 'full-clone'
                    ? 'bg-gradient-to-r from-pink-500 to-rose-500 text-white shadow-sm'
                    : 'text-gray-600 hover:text-pink-600'
                }`}
              >
                Full Clone View
              </button>
            </div>
          </div>

          {/* Side by Side View */}
          {viewMode === 'side-by-side' && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Original Website */}
              <div className="space-y-4">
                <h4 className="font-semibold text-gray-800 flex items-center">
                  <svg className="w-5 h-5 mr-2 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9" />
                  </svg>
                  Original Website
                </h4>
                <div className="border-2 border-pink-200 rounded-xl overflow-hidden bg-gradient-to-br from-pink-50 to-rose-50 flex items-center justify-center h-96 shadow-lg">
                  <div className="text-center p-8">
                    <div className="text-6xl mb-6">🌐</div>
                    <p className="text-gray-600 mb-6 max-w-md">
                      Original website preview - Click below to view the source website
                    </p>
                    <a 
                      href={result.original_url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-pink-500 to-rose-500 text-white rounded-lg hover:from-pink-600 hover:to-rose-600 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 font-medium"
                    >
                      <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                      </svg>
                      View Original Website →
                    </a>
                  </div>
                </div>
              </div>

              {/* Cloned Website */}
              <div className="space-y-4">
                <h4 className="font-semibold text-gray-800 flex items-center">
                  <svg className="w-5 h-5 mr-2 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                  AI-Enhanced Clone
                </h4>
                <div className="border-2 border-pink-200 rounded-xl overflow-hidden shadow-lg">
                  <iframe
                    srcDoc={result.cloned_html}
                    className="w-full h-96"
                    title="Cloned Website"
                    sandbox="allow-scripts"
                  />
                </div>
              </div>
            </div>
          )}

          {/* Full Clone View */}
          {viewMode === 'full-clone' && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h4 className="text-xl font-bold text-gray-800 flex items-center">
                  <svg className="w-6 h-6 mr-3 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                  🌸 AI-Enhanced Clone - Full View
                </h4>
                <div className="flex gap-2">
                  <button
                    onClick={() => setFrameHeight(600)}
                    className={`px-3 py-1 text-xs rounded ${frameHeight === 600 ? 'bg-pink-500 text-white' : 'bg-gray-200 text-gray-600'}`}
                  >
                    Medium
                  </button>
                  <button
                    onClick={() => setFrameHeight(800)}
                    className={`px-3 py-1 text-xs rounded ${frameHeight === 800 ? 'bg-pink-500 text-white' : 'bg-gray-200 text-gray-600'}`}
                  >
                    Large
                  </button>
                  <button
                    onClick={() => setFrameHeight(1000)}
                    className={`px-3 py-1 text-xs rounded ${frameHeight === 1000 ? 'bg-pink-500 text-white' : 'bg-gray-200 text-gray-600'}`}
                  >
                    XL
                  </button>
                </div>
              </div>
              
              <div className="border-2 border-pink-200 rounded-xl overflow-hidden shadow-xl">
                <div className="bg-gradient-to-r from-gray-100 to-gray-200 px-4 py-2 flex items-center space-x-2 border-b border-pink-200">
                  <div className="flex space-x-1">
                    <div className="w-3 h-3 rounded-full bg-red-400"></div>
                    <div className="w-3 h-3 rounded-full bg-yellow-400"></div>
                    <div className="w-3 h-3 rounded-full bg-green-400"></div>
                  </div>
                  <div className="bg-white rounded px-3 py-1 text-xs text-gray-600 font-mono">
                    🌸 cloned-website.html
                  </div>
                </div>
                <iframe
                  srcDoc={result.cloned_html}
                  className="w-full"
                  style={{ height: `${frameHeight}px` }}
                  title="Cloned Website - Full View"
                  sandbox="allow-scripts"
                />
              </div>
              
              <div className="text-center">
                <p className="text-sm text-gray-600 mb-4">
                  🔍 This is your full cloned website. Scroll within the frame to see the complete layout.
                </p>
                <div className="flex justify-center gap-4">
                  <a 
                    href={result.original_url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="inline-flex items-center px-4 py-2 bg-white border-2 border-pink-500 text-pink-600 rounded-lg hover:bg-pink-50 transition-all duration-300 font-medium text-sm"
                  >
                    Compare with Original →
                  </a>
                </div>
              </div>
            </div>
          )}

          {/* Enhancement Notice */}
          <div className="mt-8 bg-gradient-to-r from-pink-50 to-rose-50 p-6 rounded-xl border border-pink-200">
            <div className="flex items-start">
              <div className="text-pink-500 mr-4 mt-1">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <div>
                <h4 className="font-semibold text-pink-800 mb-2">✨ AI Enhancement Applied</h4>
                <p className="text-pink-700 text-sm leading-relaxed">
                  Your clone has been enhanced with modern design patterns, responsive layouts, smooth animations, 
                  and professional styling while preserving the original content structure and visual hierarchy.
                </p>
              </div>
            </div>
          </div>

          {/* HTML Code Display */}
          <div className="mt-8">
            <div className="flex items-center justify-between mb-4">
              <h4 className="font-semibold text-gray-800 flex items-center">
                <svg className="w-5 h-5 mr-2 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                </svg>
                Generated HTML Code
              </h4>
              <div className="text-sm text-gray-500 bg-gray-100 px-3 py-1 rounded-full">
                {result.cloned_html.length.toLocaleString()} characters
              </div>
            </div>
            <div className="bg-gray-900 text-green-400 p-6 rounded-xl overflow-auto max-h-64 border border-gray-700 shadow-lg">
              <pre className="text-xs leading-relaxed">
                <code>{result.cloned_html}</code>
              </pre>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={() => {
                const blob = new Blob([result.cloned_html || ''], { type: 'text/html' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'orchids-cloned-website.html';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
              }}
              className="flex items-center justify-center px-8 py-4 bg-gradient-to-r from-pink-500 to-rose-500 text-white rounded-xl hover:from-pink-600 hover:to-rose-600 transition-all duration-300 font-semibold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              🌸 Download HTML File
            </button>
            
            <button
              onClick={() => {
                navigator.clipboard.writeText(result.cloned_html || '');
                // You could add a toast notification here
              }}
              className="flex items-center justify-center px-8 py-4 bg-white text-pink-600 border-2 border-pink-500 rounded-xl hover:bg-pink-50 transition-all duration-300 font-semibold shadow-lg hover:shadow-xl"
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              Copy HTML Code
            </button>
          </div>

          {/* Stats Section */}
          <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-gradient-to-br from-pink-50 to-rose-50 p-6 rounded-xl border border-pink-200 text-center">
              <div className="text-2xl font-bold text-pink-600 mb-1">
                {Math.round(result.cloned_html.length / 1000)}K
              </div>
              <div className="text-sm text-gray-600">Characters Generated</div>
            </div>
            
            <div className="bg-gradient-to-br from-pink-50 to-rose-50 p-6 rounded-xl border border-pink-200 text-center">
              <div className="text-2xl font-bold text-pink-600 mb-1">
                {(result.cloned_html.match(/<[^>]+>/g) || []).length}
              </div>
              <div className="text-sm text-gray-600">HTML Elements</div>
            </div>
            
            <div className="bg-gradient-to-br from-pink-50 to-rose-50 p-6 rounded-xl border border-pink-200 text-center">
              <div className="text-2xl font-bold text-pink-600 mb-1">
                100%
              </div>
              <div className="text-sm text-gray-600">Responsive Design</div>
            </div>
          </div>

          {/* Footer */}
          <div className="mt-8 text-center text-sm text-gray-500">
            <p>🌸 Created with Orchids AI Website Cloner • Modern • Responsive • Beautiful</p>
          </div>
        </div>
      </div>
    </div>
  );
}