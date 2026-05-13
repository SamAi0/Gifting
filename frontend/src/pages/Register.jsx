import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { UserPlus, User, Mail, Lock, ArrowRight, ShieldCheck } from 'lucide-react';
import { motion } from 'framer-motion';

const Register = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    first_name: '',
    last_name: '',
  });
  const [error, setError] = useState('');
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(''); // Clear previous errors
    try {
      await register(formData);
      navigate('/login');
    } catch (err) {
      console.error('Registration error:', err);
      setError('Registration failed. The username or email might already be registered in our system.');
    }
  };

  return (
    <div className="min-h-screen pt-20 flex items-center justify-center bg-slate-50 relative overflow-hidden">
      {/* Background Decor */}
      <div className="absolute top-0 left-0 w-[600px] h-[600px] bg-primary/5 rounded-full blur-[120px] -ml-60 -mt-60"></div>
      <div className="absolute bottom-0 right-0 w-[400px] h-[400px] bg-primary/5 rounded-full blur-[100px] -mr-40 -mb-40"></div>
      
      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="max-w-2xl w-full mx-4 z-10 py-12"
      >
        <div className="bg-white rounded-[3rem] shadow-premium p-10 md:p-16 border border-slate-100 relative overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-2 bg-primary"></div>
          
          <div className="text-center mb-12">
            <div className="inline-flex items-center justify-center w-20 h-20 rounded-3xl bg-slate-50 text-primary mb-6 shadow-sm">
              <UserPlus size={36} />
            </div>
            <h2 className="text-4xl font-bold text-slate-900 tracking-tight">Create Enterprise Account</h2>
            <p className="text-slate-400 mt-3 font-medium">Join our ecosystem of premium corporate partners</p>
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
            
            <div className="grid md:grid-cols-2 gap-8">
                <div className="space-y-2 group">
                    <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-4 group-focus-within:text-primary transition-colors">First Name</label>
                    <input
                        type="text"
                        value={formData.first_name}
                        onChange={(e) => setFormData({...formData, first_name: e.target.value})}
                        className="w-full px-6 py-4 bg-slate-50 border border-slate-100 rounded-2xl focus:bg-white focus:ring-4 focus:ring-primary/5 focus:border-primary transition-all outline-none text-slate-700 font-bold"
                        placeholder="John"
                        required
                    />
                </div>
                <div className="space-y-2 group">
                    <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-4 group-focus-within:text-primary transition-colors">Last Name</label>
                    <input
                        type="text"
                        value={formData.last_name}
                        onChange={(e) => setFormData({...formData, last_name: e.target.value})}
                        className="w-full px-6 py-4 bg-slate-50 border border-slate-100 rounded-2xl focus:bg-white focus:ring-4 focus:ring-primary/5 focus:border-primary transition-all outline-none text-slate-700 font-bold"
                        placeholder="Doe"
                        required
                    />
                </div>
            </div>

            <div className="space-y-2 group">
              <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-4 group-focus-within:text-primary transition-colors flex items-center gap-2">
                <User size={14} /> Desired Username
              </label>
              <input
                type="text"
                value={formData.username}
                onChange={(e) => setFormData({...formData, username: e.target.value})}
                className="w-full px-8 py-5 bg-slate-50 border border-slate-100 rounded-2xl focus:bg-white focus:ring-4 focus:ring-primary/5 focus:border-primary transition-all outline-none text-slate-700 font-bold"
                placeholder="Choose a unique ID"
                required
              />
            </div>

            <div className="space-y-2 group">
              <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-4 group-focus-within:text-primary transition-colors flex items-center gap-2">
                <Mail size={14} /> Work Email Address
              </label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                className="w-full px-8 py-5 bg-slate-50 border border-slate-100 rounded-2xl focus:bg-white focus:ring-4 focus:ring-primary/5 focus:border-primary transition-all outline-none text-slate-700 font-bold"
                placeholder="name@company.com"
                required
              />
            </div>

            <div className="space-y-2 group">
              <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-4 group-focus-within:text-primary transition-colors flex items-center gap-2">
                <Lock size={14} /> Account Security Key
              </label>
              <input
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                className="w-full px-8 py-5 bg-slate-50 border border-slate-100 rounded-2xl focus:bg-white focus:ring-4 focus:ring-primary/5 focus:border-primary transition-all outline-none text-slate-700 font-bold"
                placeholder="Minimum 8 characters"
                required
              />
            </div>

            <button
              type="submit"
              className="w-full btn-primary py-6 text-xl flex items-center justify-center gap-3 group shadow-2xl shadow-primary/30"
            >
              Initialize Account <ArrowRight size={22} className="group-hover:translate-x-2 transition-transform" />
            </button>
          </form>

          <div className="mt-12 text-center">
            <p className="text-slate-400 font-medium mb-4">Already part of our network?</p>
            <Link to="/login" className="inline-flex items-center gap-2 text-slate-900 font-black uppercase tracking-widest text-xs hover:text-primary transition-colors pb-1 border-b-2 border-slate-900 hover:border-primary">
              Sign In to Dashboard
            </Link>
          </div>
          
          <div className="mt-12 flex items-center justify-center gap-6 pt-10 border-t border-slate-100">
             <div className="flex items-center gap-2 text-[10px] font-black text-slate-300 uppercase tracking-widest">
                <ShieldCheck size={14} /> Encrypted
             </div>
             <div className="w-1 h-1 rounded-full bg-slate-200"></div>
             <div className="flex items-center gap-2 text-[10px] font-black text-slate-300 uppercase tracking-widest">
                GDPR Compliant
             </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Register;

