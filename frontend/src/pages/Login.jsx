import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LogIn, User, Lock, ArrowRight, ShieldCheck } from 'lucide-react';
import { motion } from 'framer-motion';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(username, password);
      navigate('/');
    } catch {
      setError('The credentials you entered do not match our records.');
    }
  };

  return (
    <div className="min-h-screen pt-20 flex items-center justify-center bg-slate-50 relative overflow-hidden">
      {/* Background Decor */}
      <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-primary/5 rounded-full blur-[120px] -mr-60 -mt-60"></div>
      <div className="absolute bottom-0 left-0 w-[400px] h-[400px] bg-primary/5 rounded-full blur-[100px] -ml-40 -mb-40"></div>
      
      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="max-w-xl w-full mx-4 z-10"
      >
        <div className="bg-white rounded-[3rem] shadow-premium p-10 md:p-16 border border-slate-100 relative overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-2 bg-primary"></div>
          
          <div className="text-center mb-12">
            <div className="inline-flex items-center justify-center w-20 h-20 rounded-3xl bg-slate-50 text-primary mb-6 shadow-sm">
              <LogIn size={36} />
            </div>
            <h2 className="text-4xl font-bold text-slate-900 tracking-tight">Corporate Portal</h2>
            <p className="text-slate-400 mt-3 font-medium">Access your personalized gifting dashboard</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-8">
            {error && (
              <motion.div 
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-red-50 text-red-600 p-5 rounded-2xl text-sm font-bold border border-red-100 flex items-center gap-3"
              >
                <div className="w-2 h-2 rounded-full bg-red-600 animate-pulse"></div>
                {error}
              </motion.div>
            )}
            
            <div className="space-y-2 group">
              <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-4 group-focus-within:text-primary transition-colors flex items-center gap-2">
                <User size={14} /> Identity / Username
              </label>
              <div className="relative">
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full px-8 py-5 bg-slate-50 border border-slate-100 rounded-2xl focus:bg-white focus:ring-4 focus:ring-primary/5 focus:border-primary transition-all outline-none text-slate-700 font-bold"
                  placeholder="e.g. corporate_admin"
                  required
                />
              </div>
            </div>

            <div className="space-y-2 group">
               <div className="flex justify-between items-center px-4">
                  <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest group-focus-within:text-primary transition-colors flex items-center gap-2">
                    <Lock size={14} /> Security Key
                  </label>
                  <button type="button" className="text-[10px] font-black text-primary uppercase tracking-widest hover:underline">Forgot Key?</button>
               </div>
              <div className="relative">
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-8 py-5 bg-slate-50 border border-slate-100 rounded-2xl focus:bg-white focus:ring-4 focus:ring-primary/5 focus:border-primary transition-all outline-none text-slate-700 font-bold"
                  placeholder="••••••••"
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              className="w-full btn-primary py-6 text-xl flex items-center justify-center gap-3 group shadow-2xl shadow-primary/30"
            >
              Authorize Access <ArrowRight size={22} className="group-hover:translate-x-2 transition-transform" />
            </button>
          </form>

          <div className="mt-12 text-center">
            <p className="text-slate-400 font-medium mb-4">New to Soham Gift?</p>
            <Link to="/register" className="inline-flex items-center gap-2 text-slate-900 font-black uppercase tracking-widest text-xs hover:text-primary transition-colors pb-1 border-b-2 border-slate-900 hover:border-primary">
              Create Enterprise Account
            </Link>
          </div>
          
          <div className="mt-12 flex items-center justify-center gap-6 pt-10 border-t border-slate-100">
             <div className="flex items-center gap-2 text-[10px] font-black text-slate-300 uppercase tracking-widest">
                <ShieldCheck size={14} /> 256-Bit SSL
             </div>
             <div className="w-1 h-1 rounded-full bg-slate-200"></div>
             <div className="flex items-center gap-2 text-[10px] font-black text-slate-300 uppercase tracking-widest">
                Protected by Soham Safe
             </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Login;

