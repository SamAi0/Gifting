import { useState, useEffect, useCallback } from 'react';
import api from '../../api';
import { 
  Search, 
  Filter, 
  Eye
} from 'lucide-react';

const OrderManagement = () => {
  const [orders, setOrders] = useState([]);

  const fetchOrders = useCallback(async () => {
    try {
      const response = await api.get('/orders/all-orders/');
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
      await api.patch(`/orders/all-orders/${id}/`, { status });
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
                    <button className="p-2 hover:bg-white/10 rounded-lg text-[#D91656] transition-all">
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
    </div>
  );
};

export default OrderManagement;
