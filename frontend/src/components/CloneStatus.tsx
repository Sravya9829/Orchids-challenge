'use client';

import { CloneResult, CloneStatus as Status } from '../types';

interface CloneStatusProps {
  result: CloneResult;
  onReset: () => void;
}

export default function CloneStatus({ result, onReset }: CloneStatusProps) {
  const getStatusColor = (status: Status) => {
    switch (status) {
      case Status.PENDING:
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case Status.PROCESSING:
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case Status.COMPLETED:
        return 'bg-green-100 text-green-800 border-green-200';
      case Status.FAILED:
        return 'bg-red-100 text-red-800 border-red-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getStatusIcon = (status: Status) => {
    switch (status) {
      case Status.PENDING:
        return '⏳';
      case Status.PROCESSING:
        return '⚙️';
      case Status.COMPLETED:
        return '✅';
      case Status.FAILED:
        return '❌';
      default:
        return '📄';
    }
  };

  const getStatusMessage = (status: Status) => {
    switch (status) {
      case Status.PENDING:
        return 'Initializing cloning process...';
      case Status.PROCESSING:
        return 'AI is analyzing the website and generating your beautiful clone...';
      case Status.COMPLETED:
        return 'Website cloned successfully! Your beautiful recreation is ready! 🌸';
      case Status.FAILED:
        return 'Cloning failed. Please try again with a different website.';
      default:
        return 'Unknown status';
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white/80 backdrop-blur-sm rounded-xl shadow-xl border border-pink-100 p-8">
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-3xl font-bold bg-gradient-to-r from-pink-600 to-rose-600 bg-clip-text text-transparent">
            🌸 Clone Status
          </h2>
          <button
            onClick={onReset}
            className="px-6 py-2 bg-gradient-to-r from-pink-100 to-rose-100 text-pink-700 rounded-lg hover:from-pink-200 hover:to-rose-200 transition-all duration-300 font-medium border border-pink-200 shadow-sm"
          >
            Clone Another Website
          </button>
        </div>

        <div className="space-y-6">
          {/* Status Indicator */}
          <div className="flex items-center space-x-4">
            <div className="text-3xl">{getStatusIcon(result.status)}</div>
            <span className={`px-4 py-2 rounded-full text-sm font-medium border ${getStatusColor(result.status)}`}>
              {result.status.toUpperCase()}
            </span>
          </div>

          {/* Status Message */}
          <div className="bg-gradient-to-r from-pink-50 to-rose-50 rounded-lg p-4 border border-pink-100">
            <p className="text-gray-700 font-medium">{getStatusMessage(result.status)}</p>
          </div>

          {/* Original URL */}
          <div className="bg-white/60 p-6 rounded-xl border border-pink-100 shadow-sm">
            <p className="text-sm font-medium text-gray-600 mb-2">📍 Original URL:</p>
            <p className="font-mono text-sm text-pink-700 break-all bg-pink-50 p-3 rounded-lg border border-pink-100">
              {result.original_url}
            </p>
          </div>

          {/* Job ID */}
          <div className="bg-white/60 p-6 rounded-xl border border-pink-100 shadow-sm">
            <p className="text-sm font-medium text-gray-600 mb-2">🆔 Job ID:</p>
            <p className="font-mono text-sm text-gray-700 bg-gray-50 p-3 rounded-lg border border-gray-200">
              {result.job_id}
            </p>
          </div>

          {/* Error Message */}
          {result.error_message && (
            <div className="bg-rose-50 border border-rose-200 p-6 rounded-xl">
              <div className="flex items-start">
                <div className="text-rose-400 mr-3 mt-0.5">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                </div>
                <div>
                  <h4 className="text-sm font-medium text-rose-800">Error Details</h4>
                  <p className="text-sm text-rose-700 mt-1">{result.error_message}</p>
                </div>
              </div>
            </div>
          )}

          {/* Processing Animation */}
          {result.status === Status.PROCESSING && (
            <div className="bg-gradient-to-r from-pink-50 to-rose-50 p-6 rounded-xl border border-pink-100">
              <div className="flex items-center space-x-3">
                <div className="relative">
                  <div className="w-8 h-8 border-4 border-pink-200 border-t-pink-500 rounded-full animate-spin"></div>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-700">AI is working its magic...</p>
                  <p className="text-xs text-gray-500 mt-1">This may take a few moments while we create something beautiful</p>
                </div>
              </div>
              
              {/* Progress Steps */}
              <div className="mt-6 space-y-3">
                <div className="flex items-center text-sm">
                  <div className="w-2 h-2 bg-green-400 rounded-full mr-3"></div>
                  <span className="text-gray-600">✓ Website successfully scraped</span>
                </div>
                <div className="flex items-center text-sm">
                  <div className="w-2 h-2 bg-pink-400 rounded-full mr-3 animate-pulse"></div>
                  <span className="text-gray-600">🤖 AI analyzing layout and design...</span>
                </div>
                <div className="flex items-center text-sm">
                  <div className="w-2 h-2 bg-gray-300 rounded-full mr-3"></div>
                  <span className="text-gray-400">🎨 Generating beautiful clone...</span>
                </div>
              </div>
            </div>
          )}

          {/* Success Animation */}
          {result.status === Status.COMPLETED && (
            <div className="bg-gradient-to-r from-green-50 to-emerald-50 p-6 rounded-xl border border-green-200">
              <div className="text-center">
                <div className="text-4xl mb-4 animate-bounce">🎉</div>
                <h3 className="text-lg font-semibold text-green-800 mb-2">Clone Created Successfully!</h3>
                <p className="text-sm text-green-700">Your website has been beautifully recreated with modern design enhancements.</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}