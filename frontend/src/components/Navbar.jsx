import { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Menu, X, Gift, ShoppingCart, User, LogOut, Heart } from 'lucide-react';
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
  const [isUserDropdownOpen, setIsUserDropdownOpen] = useState(false);

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
                <div className="relative">
                  <button 
                    onMouseEnter={() => setIsUserDropdownOpen(true)}
                    onClick={() => setIsUserDropdownOpen(!isUserDropdownOpen)}
                    className={`flex items-center gap-3 p-1.5 rounded-2xl transition-all duration-300 ${
                      isScrolled ? 'hover:bg-slate-100' : 'hover:bg-white/10'
                    } ${isUserDropdownOpen ? (isScrolled ? 'bg-slate-100' : 'bg-white/10') : ''}`}
                  >
                    <div className="w-9 h-9 rounded-xl bg-primary shadow-lg shadow-primary/20 flex items-center justify-center text-white">
                      <User size={18} />
                    </div>
                    <div className={`hidden lg:flex flex-col items-start pr-2 ${
                      isScrolled ? 'text-slate-900' : location.pathname === '/' ? 'text-white' : 'text-slate-900'
                    }`}>
                      <span className="text-[10px] font-black uppercase tracking-widest opacity-60">Account</span>
                      <span className="text-sm font-bold truncate max-w-[100px]">{user.username}</span>
                    </div>
                  </button>

                  <AnimatePresence>
                    {isUserDropdownOpen && (
                      <motion.div 
                        initial={{ opacity: 0, y: 10, scale: 0.95 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: 10, scale: 0.95 }}
                        onMouseLeave={() => setIsUserDropdownOpen(false)}
                        className="absolute right-0 mt-3 w-64 bg-white rounded-3xl shadow-2xl border border-slate-100 overflow-hidden z-[100]"
                      >
                        <div className="p-5 bg-slate-50 border-b border-slate-100">
                          <p className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mb-1">Signed in as</p>
                          <p className="font-bold text-slate-900">{user.email || user.username}</p>
                        </div>
                        
                        <div className="p-2">
                          <Link 
                            to="/orders" 
                            onClick={() => setIsUserDropdownOpen(false)}
                            className="flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-bold text-slate-600 hover:bg-primary/5 hover:text-primary transition-all group"
                          >
                            <div className="w-8 h-8 rounded-lg bg-slate-100 flex items-center justify-center group-hover:bg-primary/10 transition-colors">
                              <Gift size={16} />
                            </div>
                            My Orders
                          </Link>
                          
                          <Link 
                            to="/wishlist" 
                            onClick={() => setIsUserDropdownOpen(false)}
                            className="flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-bold text-slate-600 hover:bg-primary/5 hover:text-primary transition-all group"
                          >
                            <div className="w-8 h-8 rounded-lg bg-slate-100 flex items-center justify-center group-hover:bg-primary/10 transition-colors">
                              <Heart size={16} className="text-red-400" />
                            </div>
                            Wishlist
                          </Link>

                          {user.is_staff && (
                            <Link 
                              to="/admin-panel" 
                              onClick={() => setIsUserDropdownOpen(false)}
                              className="flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-bold text-primary hover:bg-primary/5 transition-all group"
                            >
                              <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center transition-colors">
                                <User size={16} />
                              </div>
                              Admin Dashboard
                            </Link>
                          )}
                        </div>

                        <div className="p-2 border-t border-slate-50">
                          <button 
                            onClick={() => { logout(); navigate('/login'); setIsUserDropdownOpen(false); }}
                            className="w-full flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-bold text-red-500 hover:bg-red-50 transition-all group"
                          >
                            <div className="w-8 h-8 rounded-lg bg-red-50 flex items-center justify-center group-hover:bg-red-100 transition-colors">
                              <LogOut size={16} />
                            </div>
                            Logout Account
                          </button>
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
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
              
              <Link
                to="/orders"
                onClick={handleNavLinkClick}
                className={`flex items-center gap-3 text-lg font-bold transition-colors ${
                  location.pathname === '/orders' ? 'text-primary' : 'text-slate-600'
                }`}
              >
                <Gift size={20} /> My Orders
              </Link>
              
              <Link
                to="/wishlist"
                onClick={handleNavLinkClick}
                className={`flex items-center gap-3 text-lg font-bold transition-colors ${
                  location.pathname === '/wishlist' ? 'text-primary' : 'text-slate-600'
                }`}
              >
                <Heart size={20} className="text-red-400" /> Wishlist
              </Link>
              
              {user?.is_staff && (
                <Link
                  to="/admin-panel"
                  onClick={handleNavLinkClick}
                  className="text-lg font-bold text-primary"
                >
                  Admin Dashboard
                </Link>
              )}

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

