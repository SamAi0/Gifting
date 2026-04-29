import { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Menu, X, Gift, ShoppingCart, User, LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';
import { motion, AnimatePresence } from 'framer-motion';

const Navbar = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const { cart } = useCart();

  const cartCount = cart?.items?.length || 0;

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Close mobile menu when route changes - using event handler instead of effect
  const handleNavLinkClick = () => {
    setIsMobileMenuOpen(false);
  };

  const navLinks = [
    { name: 'Home', path: '/' },
    { name: 'Products', path: '/products' },
    { name: 'About Us', path: '/about' },
    { name: 'Contact', path: '/contact' },
  ];

  return (
    <nav 
      className={`fixed w-full z-50 transition-all duration-500 ${
        isScrolled 
          ? 'glass-nav py-3' 
          : 'bg-transparent py-6'
      }`}
    >
      <div className="container-custom">
        <div className="flex justify-between items-center">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-3 group">
            <motion.div 
              whileHover={{ rotate: 15 }}
              className="bg-primary p-2.5 rounded-xl shadow-lg shadow-primary/30"
            >
              <Gift className="text-white w-6 h-6" />
            </motion.div>
            <span className={`text-2xl font-bold font-display tracking-tight transition-colors duration-300 ${
              isScrolled ? 'text-slate-900' : location.pathname === '/' ? 'text-white' : 'text-slate-900'
            }`}>
              Soham <span className="text-primary">Gift</span>
            </span>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-10">
            <div className="flex items-center space-x-8">
              {navLinks.map((link) => (
                <Link
                  key={link.path}
                  to={link.path}
                  className={`relative font-semibold text-sm tracking-wide transition-all duration-300 hover:text-primary ${
                    location.pathname === link.path 
                      ? 'text-primary' 
                      : isScrolled ? 'text-slate-600' : location.pathname === '/' ? 'text-slate-200' : 'text-slate-600'
                  }`}
                >
                  {link.name}
                  {location.pathname === link.path && (
                    <motion.div 
                      layoutId="nav-underline"
                      className="absolute -bottom-1 left-0 w-full h-0.5 bg-primary rounded-full"
                    />
                  )}
                </Link>
              ))}
            </div>

            <div className="flex items-center space-x-5 border-l border-slate-200/50 pl-8">
              <Link 
                to="/cart" 
                className={`relative p-2 rounded-full transition-all duration-300 hover:bg-primary/10 hover:text-primary ${
                  isScrolled ? 'text-slate-600' : location.pathname === '/' ? 'text-white' : 'text-slate-600'
                }`}
              >
                <ShoppingCart size={22} />
                {cartCount > 0 && (
                  <span className="absolute top-0 right-0 bg-primary text-white text-[10px] font-bold w-5 h-5 rounded-full flex items-center justify-center border-2 border-white shadow-sm">
                    {cartCount}
                  </span>
                )}
              </Link>

              {user ? (
                <div className="flex items-center gap-4">
                  <div className={`flex items-center gap-2.5 font-bold text-sm ${
                    isScrolled ? 'text-slate-700' : location.pathname === '/' ? 'text-white' : 'text-slate-700'
                  }`}>
                    <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary border border-primary/20">
                      <User size={16} />
                    </div>
                    <span className="hidden lg:inline">{user.username}</span>
                  </div>
                  <button 
                    onClick={() => { logout(); navigate('/login'); }}
                    className="p-2 text-slate-400 hover:text-red-500 transition-colors"
                    title="Logout"
                  >
                    <LogOut size={20} />
                  </button>
                </div>
              ) : (
                <Link 
                  to="/login" 
                  className="btn-primary py-2.5 px-6 text-sm"
                >
                  Login
                </Link>
              )}
            </div>
          </div>

          {/* Mobile Menu Toggle */}
          <div className="flex items-center gap-3 md:hidden">
            <Link 
                to="/cart" 
                className="relative p-2 text-slate-600"
            >
                <ShoppingCart size={24} />
                {cartCount > 0 && (
                <span className="absolute -top-1 -right-1 bg-primary text-white text-[10px] font-bold w-5 h-5 rounded-full flex items-center justify-center border-2 border-white">
                    {cartCount}
                </span>
                )}
            </Link>
            <button 
                className={`p-2 rounded-lg transition-colors ${isScrolled ? 'text-slate-600 bg-slate-100' : 'text-white bg-white/10'}`}
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            >
                {isMobileMenuOpen ? <X /> : <Menu />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {isMobileMenuOpen && (
          <motion.div 
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden bg-white border-t border-slate-100 overflow-hidden shadow-2xl"
          >
            <div className="flex flex-col p-6 space-y-5">
              {navLinks.map((link) => (
                <Link
                  key={link.path}
                  to={link.path}
                  onClick={handleNavLinkClick}
                  className={`text-lg font-bold transition-colors ${
                    location.pathname === link.path ? 'text-primary' : 'text-slate-600'
                  }`}
                >
                  {link.name}
                </Link>
              ))}
              
              {user ? (
                 <div className="border-t border-slate-100 pt-5 flex justify-between items-center">
                   <div className="flex items-center gap-3 text-slate-900 font-bold">
                      <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center text-primary">
                        <User size={20} />
                      </div>
                      {user.username}
                   </div>
                   <button 
                    onClick={() => { logout(); navigate('/login'); }}
                    className="text-red-500 font-bold flex items-center gap-2 px-4 py-2 bg-red-50 rounded-xl"
                  >
                    <LogOut size={18} /> Logout
                  </button>
                 </div>
              ) : (
                <Link 
                  to="/login" 
                  className="btn-primary w-full text-center py-4"
                >
                  Login to Account
                </Link>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
};

export default Navbar;

