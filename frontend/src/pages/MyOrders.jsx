import { useState, useEffect } from 'react';
import { Package, ChevronRight, ShoppingBag, MapPin, Clock, CheckCircle2, Wand2 } from 'lucide-react';
import api from '../api';
import { motion, AnimatePresence } from 'framer-motion';
import { Link } from 'react-router-dom';

const MyOrders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const res = await api.get('/orders/mine/');
        setOrders(res.data);
      } catch (err) {
        console.error("Error fetching orders", err);
      } finally {
        setLoading(false);
      }
    };
    fetchOrders();
    window.scrollTo(0, 0);
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'PAID': return 'bg-green-100 text-green-600 border-green-200';
      case 'PLACED': return 'bg-blue-100 text-blue-600 border-blue-200';
      case 'PENDING': return 'bg-yellow-100 text-yellow-600 border-yellow-200';
      case 'SHIPPED': return 'bg-purple-100 text-purple-600 border-purple-200';
      case 'DELIVERED': return 'bg-emerald-100 text-emerald-600 border-emerald-200';
      default: return 'bg-slate-100 text-slate-600 border-slate-200';
    }
  };

  if (loading) {
    return (
      <div className="pt-40 pb-40 text-center bg-slate-50 min-h-screen flex flex-col items-center justify-center">
        <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mb-6"></div>
        <h2 className="text-2xl font-bold text-slate-900 animate-pulse">Loading Your History...</h2>
      </div>
    );
  }

  return (
    <div className="pt-32 pb-32 bg-slate-50 min-h-screen">
      <div className="container-custom">
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-16 gap-6">
          <div>
            <span className="text-primary font-black uppercase tracking-[0.3em] text-xs mb-4 inline-block">Order History</span>
            <h1 className="text-4xl md:text-6xl font-bold text-slate-900 tracking-tight">Your <span className="text-primary">Selections</span></h1>
          </div>
          <p className="text-slate-500 font-medium max-w-xs md:text-right">Track your premium gifts and customization details here.</p>
        </div>

        {orders.length === 0 ? (
          <div className="bg-white rounded-[3rem] p-20 text-center shadow-premium border border-slate-100">
            <div className="w-24 h-24 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-8 text-slate-300">
              <ShoppingBag size={48} />
            </div>
            <h2 className="text-3xl font-bold text-slate-900 mb-4">No Orders Yet</h2>
            <p className="text-slate-500 mb-10 max-w-sm mx-auto font-light">You haven't placed any orders. Start your premium gifting journey today.</p>
            <Link to="/products" className="btn-primary px-10 py-5 shadow-xl shadow-primary/30">Browse Collection</Link>
          </div>
        ) : (
          <div className="space-y-10">
            {Array.isArray(orders) && orders.map((order) => (
              <motion.div 
                key={order.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white rounded-[3rem] overflow-hidden shadow-premium border border-slate-100 hover:border-primary/20 transition-all duration-500"
              >
                {/* Order Header */}
                <div className="bg-slate-900 p-8 md:p-10 text-white flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
                  <div className="flex flex-wrap items-center gap-6 md:gap-12">
                    <div>
                      <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Order Identifier</p>
                      <p className="text-lg font-bold">#SG-{order.id.toString().padStart(5, '0')}</p>
                    </div>
                    <div>
                      <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Transaction Date</p>
                      <p className="text-sm font-medium">{new Date(order.created_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' })}</p>
                    </div>
                    <div>
                      <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Total Investment</p>
                      <p className="text-xl font-black text-primary">₹{order.total_amount}</p>
                    </div>
                  </div>
                  <div className={`px-6 py-2.5 rounded-full text-[10px] font-black uppercase tracking-widest border-2 ${getStatusColor(order.status)} shadow-lg shadow-black/20`}>
                    {order.status}
                  </div>
                </div>

                {/* Order Content */}
                <div className="p-8 md:p-12">
                  <div className="grid lg:grid-cols-12 gap-12">
                    {/* Items List */}
                    <div className="lg:col-span-8 space-y-8">
                       <h3 className="text-xl font-bold text-slate-900 flex items-center gap-3 mb-6">
                          <Package size={20} className="text-primary" /> Order Manifest
                       </h3>
                       {order.items.map((item) => (
                         <div key={item.id} className="flex flex-col sm:flex-row gap-8 p-6 rounded-[2rem] bg-slate-50 border border-slate-100/50 hover:bg-white hover:shadow-xl hover:shadow-slate-200/50 transition-all duration-500 group">
                            <div className="w-full sm:w-32 h-32 bg-white rounded-2xl overflow-hidden shadow-sm flex-shrink-0 p-2">
                               <img 
                                 src={item.product_details.image} 
                                 alt={item.product_details.name} 
                                 className="w-full h-full object-contain group-hover:scale-110 transition-transform duration-700" 
                               />
                            </div>
                            <div className="flex-grow space-y-4">
                               <div className="flex justify-between items-start">
                                  <div>
                                     <h4 className="font-bold text-slate-900 text-lg mb-1">{item.product_details.name}</h4>
                                     <p className="text-xs text-slate-400 font-medium">Quantity: <span className="text-slate-900 font-bold">{item.quantity} units</span></p>
                                  </div>
                                  <p className="text-lg font-black text-slate-900">₹{item.price}</p>
                               </div>

                               {(item.customization_text || item.customization_image) && (
                                 <div className="bg-white/80 backdrop-blur-sm p-5 rounded-2xl border border-slate-200/50 space-y-3">
                                    <div className="flex items-center gap-2 text-[10px] font-black text-primary uppercase tracking-widest mb-1">
                                       <Wand2 size={12} /> Branding Details
                                    </div>
                                    {item.customization_text && (
                                       <p className="text-sm text-slate-700 font-medium bg-slate-50 px-3 py-2 rounded-lg border border-slate-100 italic">"{item.customization_text}"</p>
                                    )}
                                    {item.customization_image && (
                                       <div className="flex items-center gap-4">
                                          <div className="w-16 h-16 rounded-lg bg-slate-900 overflow-hidden border-2 border-white shadow-md">
                                             <img src={item.customization_image} alt="Mockup" className="w-full h-full object-contain" />
                                          </div>
                                          <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Custom Mockup Applied</span>
                                       </div>
                                    )}
                                 </div>
                               )}
                            </div>
                         </div>
                       ))}
                    </div>

                    {/* Meta Info */}
                    <div className="lg:col-span-4 space-y-8">
                       <div className="bg-slate-50 rounded-[2rem] p-8 space-y-6">
                          <h4 className="text-sm font-black text-slate-900 uppercase tracking-widest flex items-center gap-3 pb-4 border-b border-slate-200/50">
                             <MapPin size={16} className="text-primary" /> Delivery Node
                          </h4>
                          <div className="space-y-2">
                             <p className="font-bold text-slate-900 text-sm leading-tight">{order.address_details?.street_address}</p>
                             <p className="text-xs text-slate-500 font-medium">{order.address_details?.city}, {order.address_details?.state} - {order.address_details?.pincode}</p>
                          </div>
                       </div>

                       <div className="bg-slate-50 rounded-[2rem] p-8 space-y-6">
                          <h4 className="text-sm font-black text-slate-900 uppercase tracking-widest flex items-center gap-3 pb-4 border-b border-slate-200/50">
                             <Clock size={16} className="text-primary" /> Shipment Status
                          </h4>
                          <div className="relative pl-8 space-y-6">
                             <div className="absolute left-0 top-1 bottom-1 w-0.5 bg-slate-200"></div>
                             <div className="relative">
                                <div className={`absolute -left-[35px] w-4 h-4 rounded-full border-4 border-white ${order.status !== 'CANCELLED' ? 'bg-primary' : 'bg-slate-300'}`}></div>
                                <p className="text-xs font-bold text-slate-900">Order Placed</p>
                                <p className="text-[10px] text-slate-400 font-medium">Successfully received and verified</p>
                             </div>
                             <div className="relative">
                                <div className={`absolute -left-[35px] w-4 h-4 rounded-full border-4 border-white ${['SHIPPED', 'DELIVERED'].includes(order.status) ? 'bg-primary' : 'bg-slate-300'}`}></div>
                                <p className="text-xs font-bold text-slate-900">In Production / Shipped</p>
                                <p className="text-[10px] text-slate-400 font-medium">Our artisans are preparing your gift</p>
                             </div>
                             <div className="relative">
                                <div className={`absolute -left-[35px] w-4 h-4 rounded-full border-4 border-white ${order.status === 'DELIVERED' ? 'bg-primary' : 'bg-slate-300'}`}></div>
                                <p className="text-xs font-bold text-slate-900">Delivered</p>
                                <p className="text-[10px] text-slate-400 font-medium">Final destination reached</p>
                             </div>
                          </div>
                       </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default MyOrders;
