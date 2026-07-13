import { useState, useEffect, useCallback } from 'react';
import api, { getImageUrl } from '../../api';
import { 
  Search, 
  Filter, 
  Eye,
  X,
  Package,
  Wand2
} from 'lucide-react';

const OrderManagement = () => {
  const [orders, setOrders] = useState([]);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const filteredOrders = orders; // Simple mapping for now

  const fetchOrders = useCallback(async () => {
    try {
      const response = await api.get('orders/all-orders/');
      setOrders(response.data);
    } catch (err) {
      console.error("Failed to fetch orders:", err);
    }
  }, []);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchOrders();
  }, [fetchOrders]);

  const updateStatus = async (id, status) => {
    try {
      await api.patch(`orders/all-orders/${id}/`, { status });
      fetchOrders();
    } catch (err) {
      console.error("Status update failed:", err);
    }
  };

  const getStatusStyle = (status) => {
    switch (status) {
      case 'PENDING': return 'bg-amber-500/10 text-amber-500';
      case 'PAID': return 'bg-blue-500/10 text-blue-500';
      case 'SHIPPED': return 'bg-purple-500/10 text-purple-500';
      case 'DELIVERED': return 'bg-emerald-500/10 text-emerald-500';
      case 'CANCELLED': return 'bg-rose-500/10 text-rose-500';
      default: return 'bg-gray-500/10 text-gray-500';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="relative w-full sm:w-96">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" size={18} />
          <input 
            type="text" 
            placeholder="Search orders..." 
            className="w-full bg-[#161b2a] border border-white/5 rounded-xl py-3 pl-12 pr-4 focus:outline-none focus:border-[#D91656] transition-colors"
          />
        </div>
        <div className="flex gap-2 w-full sm:w-auto">
          <button className="flex-1 sm:flex-none flex items-center justify-center bg-[#161b2a] border border-white/5 px-4 py-3 rounded-xl hover:bg-white/5 transition-colors">
            <Filter size={18} className="mr-2" /> Filter
          </button>
          <button className="flex-1 sm:flex-none bg-[#D91656] text-white px-6 py-3 rounded-xl font-bold hover:bg-[#ff1e66] transition-all">
            Export List
          </button>
        </div>
      </div>

      <div className="bg-[#161b2a] border border-white/5 rounded-2xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="text-gray-500 text-sm border-b border-white/5 bg-white/5">
                <th className="px-6 py-4 font-medium uppercase">Order Details</th>
                <th className="px-6 py-4 font-medium uppercase">Customer</th>
                <th className="px-6 py-4 font-medium uppercase">Date</th>
                <th className="px-6 py-4 font-medium uppercase">Items</th>
                <th className="px-6 py-4 font-medium uppercase">Status</th>
                <th className="px-6 py-4 font-medium uppercase">Total</th>
                <th className="px-6 py-4 font-medium uppercase text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {filteredOrders.map((order) => (
                <tr key={order.id} className="hover:bg-white/5 transition-colors">
                  <td className="px-6 py-4 font-bold text-white">#ORD-{order.id}</td>
                  <td className="px-6 py-4">{order.user_name || order.user}</td>
                  <td className="px-6 py-4 text-gray-400">{new Date(order.created_at).toLocaleDateString()}</td>
                  <td className="px-6 py-4">{order.items?.length || 0} items</td>
                  <td className="px-6 py-4">
                    <select 
                      value={order.status}
                      onChange={(e) => updateStatus(order.id, e.target.value)}
                      className={`px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider bg-transparent outline-none cursor-pointer ${getStatusStyle(order.status)}`}
                    >
                      <option value="PENDING">Pending</option>
                      <option value="PAID">Paid</option>
                      <option value="SHIPPED">Shipped</option>
                      <option value="DELIVERED">Delivered</option>
                      <option value="CANCELLED">Cancelled</option>
                    </select>
                  </td>
                  <td className="px-6 py-4 font-bold text-white">₹{order.total_amount}</td>
                  <td className="px-6 py-4 text-right">
                    <button 
                      onClick={() => setSelectedOrder(order)}
                      className="p-2 hover:bg-white/10 rounded-lg text-[#D91656] transition-all"
                      title="View Order Details & Mockups"
                    >
                      <Eye size={18} />
                    </button>
                  </td>
                </tr>
              ))}
              {filteredOrders.length === 0 && (
                <tr>
                  <td colSpan="7" className="px-6 py-10 text-center text-gray-500">No orders found matching your search.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Order Details Modal */}
      {selectedOrder && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
          <div className="bg-[#161b2a] border border-white/10 w-full max-w-4xl rounded-2xl shadow-2xl overflow-hidden max-h-[90vh] flex flex-col">
            <div className="p-6 border-b border-white/10 flex justify-between items-center bg-white/5">
              <div>
                <h3 className="text-xl font-bold text-white">Order #ORD-{selectedOrder.id}</h3>
                <p className="text-gray-400 text-sm mt-1">Customer: {selectedOrder.user_name || selectedOrder.user}</p>
              </div>
              <button onClick={() => setSelectedOrder(null)} className="p-2 hover:bg-white/10 rounded-lg text-gray-400 transition-all">
                <X size={24} />
              </button>
            </div>
            
            <div className="p-6 overflow-y-auto space-y-6">
              <h4 className="text-lg font-bold text-white flex items-center gap-2">
                <Package size={18} className="text-[#D91656]" /> Items & Customizations
              </h4>
              
              <div className="space-y-4">
                {selectedOrder.items?.map((item) => {
                  let parsedData = null;
                  try {
                    if (item.customization_data) {
                      parsedData = typeof item.customization_data === 'string' 
                        ? JSON.parse(item.customization_data) 
                        : item.customization_data;
                    }
                  } catch (e) {
                    console.error("Failed to parse customization data:", e);
                  }

                  const hasCustomization = item.customization_text || item.customization_image || item.logo_image || parsedData;

                  return (
                  <div key={item.id} className="bg-white/5 border border-white/10 rounded-xl p-4 flex flex-col sm:flex-row gap-6">
                    <div className="w-24 h-24 bg-white/10 rounded-lg p-2 flex-shrink-0">
                      {item.product_details?.image ? (
                        <img src={getImageUrl(item.product_details.image)} alt={item.product_details.name} className="w-full h-full object-contain" />
                      ) : (
                         <div className="w-full h-full flex items-center justify-center text-gray-500"><Package size={24} /></div>
                      )}
                    </div>
                    
                    <div className="flex-grow space-y-3">
                      <div className="flex justify-between items-start">
                        <div>
                          <h5 className="font-bold text-white text-lg">{item.product_details?.name || 'Unknown Product'}</h5>
                          <p className="text-sm text-gray-400">Qty: {item.quantity}</p>
                        </div>
                        <p className="font-bold text-[#D91656]">₹{item.price}</p>
                      </div>

                      {hasCustomization && (
                        <div className="bg-black/20 p-4 rounded-lg border border-white/5 space-y-3 mt-2">
                          <div className="flex items-center gap-2 text-xs font-bold text-gray-300 uppercase tracking-wider mb-2">
                            <Wand2 size={14} className="text-[#D91656]" /> Customization Details
                          </div>
                          
                          {item.customization_text && (
                            <p className="text-sm text-gray-300 bg-white/5 p-2 rounded border border-white/10">
                              Text: <span className="font-mono text-white">"{item.customization_text}"</span>
                            </p>
                          )}

                          {/* Render parsed customization data (texts, color, instructions) */}
                          {parsedData && (
                            <div className="space-y-2">
                              {parsedData.texts && parsedData.texts.length > 0 && (
                                <p className="text-sm text-gray-300 bg-white/5 p-2 rounded border border-white/10">
                                  Custom Texts: <span className="font-mono text-white">"{parsedData.texts.map(t => t.text).join('", "')}"</span>
                                </p>
                              )}
                              {parsedData.instructions && (
                                <p className="text-sm text-gray-300 bg-white/5 p-2 rounded border border-white/10">
                                  Instructions: <span className="text-white">"{parsedData.instructions}"</span>
                                </p>
                              )}
                              {parsedData.color && (
                                <p className="text-sm text-gray-300 flex items-center gap-2">
                                  Selected Color: 
                                  <span className="w-4 h-4 rounded-full border border-white/20 inline-block" style={{ backgroundColor: parsedData.color }}></span>
                                  <span className="font-mono text-white text-xs">{parsedData.color}</span>
                                </p>
                              )}
                            </div>
                          )}
                          
                          {(item.customization_image || item.logo_image) && (
                            <div className="flex flex-wrap gap-6 mt-3">
                              {item.customization_image && (
                                <div>
                                  <p className="text-xs text-gray-400 mb-2">Mockup Preview (Click to view full size)</p>
                                  <a href={getImageUrl(item.customization_image)} target="_blank" rel="noopener noreferrer" className="block w-24 h-24 rounded-lg bg-white/10 border border-white/20 hover:border-[#D91656] transition-colors cursor-zoom-in overflow-hidden flex items-center justify-center">
                                    <img src={getImageUrl(item.customization_image)} alt="Mockup Preview" className="w-full h-full object-contain" />
                                  </a>
                                </div>
                              )}
                              {item.logo_image && (
                                <div>
                                  <p className="text-xs text-gray-400 mb-2">Uploaded Logo (Click to view full size)</p>
                                  <a href={getImageUrl(item.logo_image)} target="_blank" rel="noopener noreferrer" className="block w-24 h-24 rounded-lg bg-white/10 border border-white/20 hover:border-[#D91656] transition-colors cursor-zoom-in overflow-hidden flex items-center justify-center">
                                    <img src={getImageUrl(item.logo_image)} alt="Logo" className="w-full h-full object-contain" />
                                  </a>
                                </div>
                              )}
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                )})}
              </div>
            </div>
            
            <div className="p-6 border-t border-white/10 bg-white/5 flex justify-end">
               <button onClick={() => setSelectedOrder(null)} className="px-6 py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg transition-colors font-bold">
                 Close
               </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default OrderManagement;
