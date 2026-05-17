import { useState, useEffect, useRef } from 'react';
import api from '../../api';
import { Search, X, Package, ShoppingBag, User, ExternalLink } from 'lucide-react';
import { Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';

const AdminGlobalSearch = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState({ products: [], orders: [], users: [] });
  const [showResults, setShowResults] = useState(false);
  const [loading, setLoading] = useState(false);
  const searchRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setShowResults(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    const fetchResults = async () => {
      if (query.length < 2) {
        setResults({ products: [], orders: [], users: [] });
        return;
      }
      setLoading(true);
      try {
        const response = await api.get(`/admin/search/?q=${query}`);
        setResults(response.data);
      } catch (err) {
        console.error("Search failed", err);
      } finally {
        setLoading(false);
      }
    };

    const timer = setTimeout(fetchResults, 300);
    return () => clearTimeout(timer);
  }, [query]);

  return (
    <div className="relative w-full max-w-2xl" ref={searchRef}>
      <div className="relative group">
        <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 group-focus-within:text-[#D91656] transition-colors">
          <Search size={20} />
        </div>
        <input
          type="text"
          placeholder="Search products, orders, users..."
          className="w-full pl-12 pr-12 py-3 bg-[#161b2a] border border-white/5 rounded-2xl focus:outline-none focus:border-[#D91656]/50 transition-all text-white placeholder-gray-500"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setShowResults(true);
          }}
          onFocus={() => setShowResults(true)}
        />
        {query && (
          <button
            onClick={() => setQuery('')}
            className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500 hover:text-white"
          >
            <X size={18} />
          </button>
        )}
      </div>

      <AnimatePresence>
        {showResults && (query.length >= 2) && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            className="absolute top-full left-0 right-0 mt-3 bg-[#1c2237] border border-white/10 rounded-2xl shadow-2xl z-[200] overflow-hidden max-h-[80vh] overflow-y-auto"
          >
            {loading ? (
              <div className="p-8 text-center">
                <div className="w-8 h-8 border-2 border-[#D91656] border-t-transparent rounded-full animate-spin mx-auto"></div>
              </div>
            ) : (
              <div className="divide-y divide-white/5">
                {/* Products */}
                {results.products?.length > 0 && (
                  <div className="p-4">
                    <h4 className="text-[10px] font-black text-gray-500 uppercase tracking-widest mb-3 flex items-center gap-2">
                      <Package size={12} /> Products
                    </h4>
                    <div className="space-y-2">
                      {results.products.map(product => (
                        <Link key={product.id} to={`/admin/products?edit=${product.id}`} className="flex items-center gap-3 p-2 rounded-xl hover:bg-white/5 transition-colors group">
                          <img src={product.image} className="w-10 h-10 rounded-lg object-cover" alt="" />
                          <div className="flex-grow">
                            <p className="text-sm font-semibold text-white group-hover:text-[#D91656]">{product.name}</p>
                            <p className="text-[10px] text-gray-500">₹{product.price} • SKU: {product.sku}</p>
                          </div>
                          <ExternalLink size={14} className="text-gray-600 opacity-0 group-hover:opacity-100 transition-opacity" />
                        </Link>
                      ))}
                    </div>
                  </div>
                )}

                {/* Orders */}
                {results.orders?.length > 0 && (
                  <div className="p-4">
                    <h4 className="text-[10px] font-black text-gray-500 uppercase tracking-widest mb-3 flex items-center gap-2">
                      <ShoppingBag size={12} /> Orders
                    </h4>
                    <div className="space-y-2">
                      {results.orders.map(order => (
                        <Link key={order.id} to={`/admin/orders?id=${order.id}`} className="flex items-center gap-3 p-2 rounded-xl hover:bg-white/5 transition-colors group">
                          <div className="w-10 h-10 rounded-lg bg-white/5 flex items-center justify-center text-gray-400">
                            #
                          </div>
                          <div className="flex-grow">
                            <p className="text-sm font-semibold text-white group-hover:text-[#D91656]">Order #ORD-{order.id}</p>
                            <p className="text-[10px] text-gray-500">{order.user_name} • ₹{order.total_amount}</p>
                          </div>
                          <div className="text-[9px] px-2 py-0.5 rounded-full bg-[#D91656]/10 text-[#D91656] font-bold">
                            {order.status}
                          </div>
                        </Link>
                      ))}
                    </div>
                  </div>
                )}

                {/* Users */}
                {results.users?.length > 0 && (
                  <div className="p-4">
                    <h4 className="text-[10px] font-black text-gray-500 uppercase tracking-widest mb-3 flex items-center gap-2">
                      <User size={12} /> Users
                    </h4>
                    <div className="space-y-2">
                      {results.users.map(user => (
                        <div key={user.id} className="flex items-center gap-3 p-2 rounded-xl hover:bg-white/5 transition-colors group">
                          <div className="w-10 h-10 rounded-lg bg-[#D91656]/10 flex items-center justify-center text-[#D91656]">
                            <User size={18} />
                          </div>
                          <div className="flex-grow">
                            <p className="text-sm font-semibold text-white">{user.username}</p>
                            <p className="text-[10px] text-gray-500">{user.email}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {results.products?.length === 0 && results.orders?.length === 0 && results.users?.length === 0 && (
                  <div className="p-12 text-center text-gray-500 text-sm">
                    No results found for "{query}"
                  </div>
                )}
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default AdminGlobalSearch;
