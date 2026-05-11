import React from 'react';
import { AlertTriangle, RefreshCw, Home } from 'lucide-react';
import { Link } from 'react-router-dom';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught an error", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-[3rem] p-12 max-w-xl w-full text-center shadow-premium border border-slate-100">
            <div className="w-20 h-20 bg-red-50 text-red-500 rounded-full flex items-center justify-center mx-auto mb-8">
               <AlertTriangle size={40} />
            </div>
            <h2 className="text-3xl font-bold text-slate-900 mb-4 tracking-tight">Something went wrong</h2>
            <p className="text-slate-500 mb-10 font-medium leading-relaxed">
              We encountered an unexpected error while loading this page. Our team has been notified.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
               <button 
                 onClick={() => window.location.reload()}
                 className="btn-primary px-8 py-4 flex items-center justify-center gap-2"
               >
                  <RefreshCw size={18} /> Reload Page
               </button>
               <Link 
                 to="/" 
                 onClick={() => this.setState({ hasError: false })}
                 className="btn-secondary px-8 py-4 flex items-center justify-center gap-2"
               >
                  <Home size={18} /> Back Home
               </Link>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children; 
  }
}

export default ErrorBoundary;
