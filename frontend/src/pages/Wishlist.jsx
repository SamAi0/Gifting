import { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { Heart, Trash2, ArrowRight } from 'lucide-react';
import { fetchWishlist, removeFromWishlist, getImageUrl } from '../api';
import { motion, AnimatePresence } from 'framer-motion';


const Wishlist = () => {
  const [wishlist, setWishlist] = useState([]);
  const [loading, setLoading] = useState(true);
  const loadWishlist = useCallback(async () => {
    try {
      const res = await fetchWishlist();
      setWishlist(res.data);
    } catch (err) {
      console.error("Error loading wishlist", err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadWishlist();
  }, [loadWishlist]);

  const handleRemove = async (id) => {
    try {
      await removeFromWishlist(id);
      setWishlist(wishlist.filter(item => item.id !== id));
    } catch (err) {
      console.error("Error removing from wishlist", err);
    }
  };

  if (loading) {
    return (
      <div className="pt-40 pb-40 text-center bg-slate-50 min-h-screen flex flex-col items-center justify-center">
        <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mb-6"></div>
        <h2 className="text-2xl font-bold text-slate-900 animate-pulse">Loading Your Wishlist...</h2>
      </div>
    );
  }

  return (
    <div className="pt-32 pb-32 bg-slate-50 min-h-screen">
      <div className="container-custom">
        <div className="flex flex-col md:flex-row justify-between items-end mb-16 gap-8">
           <div>
              <span className="text-primary font-black uppercase tracking-[0.3em] text-xs mb-4 inline-block">My Collection</span>
              <h1 className="text-4xl md:text-5xl font-bold text-slate-900 tracking-tight">Your <span className="text-primary italic">Wishlist</span></h1>
           </div>
           <Link to="/products" className="btn-secondary py-3 px-6 text-sm">Continue Shopping</Link>
        </div>

        <AnimatePresence mode="wait">
           {wishlist.length > 0 ? (
             <motion.div 
               key="wishlist-grid"
               initial={{ opacity: 0 }}
               animate={{ opacity: 1 }}
               className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8"
             >
                {wishlist.map((item) => (
                  <motion.div 
                    key={item.id}
                    layout
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, scale: 0.9 }}
                    className="bg-white rounded-[2.5rem] overflow-hidden border border-slate-100 shadow-sm hover:shadow-xl transition-all group"
                  >
                     <div className="aspect-square bg-slate-50 relative overflow-hidden">
                        <img 
                          src={getImageUrl(item.product_details.image)} 
                          alt={item.product_details.name} 
                          className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" 
                        />
                        <button 
                          onClick={() => handleRemove(item.id)}
                          className="absolute top-4 right-4 w-10 h-10 rounded-xl bg-white/90 backdrop-blur-md text-slate-400 hover:text-red-500 flex items-center justify-center transition-all shadow-sm"
                        >
                           <Trash2 size={18} />
                        </button>
                     </div>
                     <div className="p-8">
                        <h3 className="font-bold text-slate-900 mb-2 truncate group-hover:text-primary transition-colors">{item.product_details.name}</h3>
                        <p className="text-2xl font-black text-slate-900 mb-6">₹{item.product_details.price}</p>
                        
                        <div className="flex gap-3">
                           <Link 
                             to={`/products/${item.product}`}
                             className="flex-grow btn-primary py-3 text-xs flex items-center justify-center gap-2"
                           >
                              View Details <ArrowRight size={14} />
                           </Link>
                        </div>
                     </div>
                  </motion.div>
                ))}
             </motion.div>
           ) : (
             <motion.div 
               key="empty-wishlist"
               initial={{ opacity: 0 }}
               animate={{ opacity: 1 }}
               className="text-center py-32 bg-white rounded-[3rem] border-2 border-dashed border-slate-100"
             >
                <div className="w-24 h-24 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-8 text-slate-200">
                   <Heart size={48} />
                </div>
                <h3 className="text-2xl font-bold text-slate-900 mb-4">Your wishlist is empty</h3>
                <p className="text-slate-400 mb-10 max-w-sm mx-auto">Save items you love to your wishlist and they will appear here.</p>
                <Link to="/products" className="btn-primary py-4 px-12 text-sm shadow-xl shadow-primary/20">
                   Discover Gifts
                </Link>
             </motion.div>
           )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default Wishlist;
