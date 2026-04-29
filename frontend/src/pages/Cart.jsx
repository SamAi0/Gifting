import { Link } from 'react-router-dom';
import { Trash2, Plus, Minus, ShoppingBag, ArrowRight, ChevronLeft, ShieldCheck, Truck, Package } from 'lucide-react';
import { useCart } from '../context/CartContext';
import { motion, AnimatePresence } from 'framer-motion';

const Cart = () => {
  const { cart, loading, removeFromCart, updateQuantity } = useCart();

  if (loading && !cart) {
    return (
      <div className="pt-40 pb-40 text-center bg-slate-50 min-h-screen flex flex-col items-center justify-center">
        <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mb-6"></div>
        <h2 className="text-2xl font-bold text-slate-900 animate-pulse">Loading Your Selection...</h2>
      </div>
    );
  }

  if (!cart || cart.items.length === 0) {
    return (
      <div className="pt-40 pb-40 text-center bg-slate-50 min-h-screen flex flex-col items-center justify-center px-4">
        <div className="w-32 h-32 bg-white rounded-full shadow-premium flex items-center justify-center text-slate-200 mb-8">
          <ShoppingBag size={64} />
        </div>
        <h2 className="text-4xl font-bold text-slate-900 mb-4 tracking-tight">Your cart is currently empty</h2>
        <p className="text-slate-500 mb-10 max-w-sm mx-auto font-light">Explore our curated collections and add some premium gifts to your cart.</p>
        <Link to="/products" className="btn-primary px-10 py-5 text-lg">
          Browse Catalog
        </Link>
      </div>
    );
  }

  return (
    <div className="pt-32 pb-32 bg-slate-50 min-h-screen">
      <div className="container-custom">
        <div className="flex items-center justify-between mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-slate-900 tracking-tight">Your <span className="text-primary">Selection</span></h1>
          <Link to="/products" className="text-slate-400 hover:text-primary font-bold text-sm flex items-center gap-2 transition-colors">
            <ChevronLeft size={18} /> Continue Shopping
          </Link>
        </div>

        <div className="grid lg:grid-cols-12 gap-12 items-start">
          {/* Cart Items */}
          <div className="lg:col-span-8 space-y-6">
            <AnimatePresence>
              {cart.items.map((item) => (
                <motion.div 
                  key={item.id} 
                  layout
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="bg-white rounded-[2.5rem] p-6 md:p-8 shadow-premium border border-slate-100 flex flex-col md:flex-row gap-8 relative group overflow-hidden"
                >
                  <div className="w-full md:w-40 h-40 bg-slate-50 rounded-3xl overflow-hidden flex-shrink-0 border border-slate-100 p-2">
                    <img 
                      src={item.customization_image || item.product_details.image} 
                      alt={item.product_details.name}
                      className="w-full h-full object-contain mix-blend-multiply"
                    />
                  </div>
                  <div className="flex-grow flex flex-col justify-between">
                    <div>
                      <div className="flex justify-between items-start mb-2">
                        <div>
                           <span className="text-primary font-black uppercase tracking-[0.2em] text-[10px] mb-2 block">{item.product_details.category_name}</span>
                           <h3 className="text-2xl font-bold text-slate-900 leading-tight">{item.product_details.name}</h3>
                        </div>
                        <button 
                          onClick={() => removeFromCart(item.id)}
                          className="w-10 h-10 rounded-xl bg-slate-50 text-slate-300 hover:bg-red-50 hover:text-red-500 transition-all flex items-center justify-center"
                        >
                          <Trash2 size={18} />
                        </button>
                      </div>
                      
                      {item.customization_text && (
                         <div className="mt-4 inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-primary/5 border border-primary/10">
                            <span className="text-[10px] font-black text-primary uppercase tracking-widest">Custom branding:</span>
                            <span className="text-xs font-bold text-slate-600 italic">"{item.customization_text}"</span>
                         </div>
                      )}
                    </div>

                    <div className="flex justify-between items-end mt-8">
                      <div className="flex items-center gap-6 bg-slate-50 rounded-2xl p-1.5 border border-slate-100">
                        <button 
                          onClick={() => updateQuantity(item.id, Math.max(1, item.quantity - 1))}
                          className="w-10 h-10 flex items-center justify-center text-slate-400 hover:bg-white hover:text-primary rounded-xl transition-all shadow-sm active:scale-95"
                        >
                          <Minus size={16} />
                        </button>
                        <span className="font-bold text-slate-900 w-6 text-center">{item.quantity}</span>
                        <button 
                          onClick={() => updateQuantity(item.id, item.quantity + 1)}
                          className="w-10 h-10 flex items-center justify-center text-slate-400 hover:bg-white hover:text-primary rounded-xl transition-all shadow-sm active:scale-95"
                        >
                          <Plus size={16} />
                        </button>
                      </div>
                      <div className="text-right">
                         <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest mb-1">Unit Price: ₹{item.product_details.price}</p>
                         <p className="text-3xl font-black text-slate-900 tracking-tighter">₹{item.subtotal}</p>
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
            
            {/* Trust Badges */}
            <div className="grid md:grid-cols-3 gap-6 pt-10">
               {[
                 { icon: ShieldCheck, title: 'Secure Payment', desc: 'PCI-DSS Compliant' },
                 { icon: Truck, title: 'Tracked Delivery', desc: 'Updates via WhatsApp' },
                 { icon: Package, title: 'Safe Packaging', desc: 'Gift ready condition' },
               ].map((badge, idx) => (
                 <div key={idx} className="flex items-center gap-4 p-4">
                    <div className="w-10 h-10 rounded-xl bg-white shadow-sm flex items-center justify-center text-primary flex-shrink-0">
                       <badge.icon size={20} />
                    </div>
                    <div>
                       <p className="text-xs font-bold text-slate-900">{badge.title}</p>
                       <p className="text-[10px] text-slate-400 font-medium">{badge.desc}</p>
                    </div>
                 </div>
               ))}
            </div>
          </div>

          {/* Summary Card */}
          <div className="lg:col-span-4 sticky top-32">
            <motion.div 
               initial={{ opacity: 0, x: 20 }}
               animate={{ opacity: 1, x: 0 }}
               className="bg-slate-900 rounded-[3rem] p-10 text-white shadow-3xl relative overflow-hidden"
            >
              <div className="absolute top-0 right-0 w-32 h-32 bg-primary/20 rounded-full blur-3xl"></div>
              
              <h2 className="text-2xl font-bold mb-10 tracking-tight">Order Summary</h2>
              
              <div className="space-y-6 mb-10">
                <div className="flex justify-between items-center text-slate-400">
                  <span className="text-sm font-medium">Subtotal ({cart.items.length} units)</span>
                  <span className="text-white font-bold">₹{cart.total_price}</span>
                </div>
                <div className="flex justify-between items-center text-slate-400">
                  <span className="text-sm font-medium">Bulk Discount</span>
                  <span className="text-green-400 font-bold">-₹0.00</span>
                </div>
                <div className="flex justify-between items-center text-slate-400">
                  <span className="text-sm font-medium">Estimated Delivery</span>
                  <span className="text-white font-bold text-xs uppercase tracking-widest">Calculated Next</span>
                </div>
                
                <div className="pt-6 border-t border-white/10 flex justify-between items-end">
                  <div>
                     <p className="text-[10px] font-black text-primary uppercase tracking-[0.3em] mb-1">Total to Pay</p>
                     <span className="text-lg font-bold">Inc. Taxes</span>
                  </div>
                  <span className="text-5xl font-black text-white tracking-tighter">₹{cart.total_price}</span>
                </div>
              </div>

              <div className="space-y-4">
                 <Link 
                   to="/checkout" 
                   className="btn-primary w-full py-6 text-xl shadow-2xl shadow-primary/30 group"
                 >
                   Process Checkout <ArrowRight size={22} className="group-hover:translate-x-2 transition-transform" />
                 </Link>
                 <p className="text-center text-slate-500 text-[10px] font-bold uppercase tracking-widest">
                   Free Delivery for orders above ₹5,000
                 </p>
              </div>
            </motion.div>
            
            {/* Promo Area */}
            <div className="mt-8 p-8 bg-white rounded-[2.5rem] border border-slate-100 shadow-sm">
               <p className="text-xs font-black text-slate-400 uppercase tracking-widest mb-4">Have a corporate code?</p>
               <div className="flex gap-2">
                  <input type="text" placeholder="GIFT20" className="flex-grow bg-slate-50 border border-slate-100 rounded-xl px-4 text-xs font-bold focus:outline-none focus:border-primary transition-all" />
                  <button className="bg-slate-900 text-white px-6 py-3 rounded-xl text-xs font-bold hover:bg-primary transition-colors">Apply</button>
               </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Cart;

