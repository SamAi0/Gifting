import { useState, useEffect } from 'react';
import api from '../../api';
import { 
  Package, 
  ShoppingCart, 
  TrendingUp, 
  ArrowUpRight,
  ArrowDownRight,
  MessageSquare
} from 'lucide-react';

import AdminGlobalSearch from '../../components/admin/AdminGlobalSearch';

const StatCard = ({ title, value, icon, trend, trendValue, color }) => (
  <div className="bg-[#161b2a] border border-white/5 rounded-2xl p-6 hover:border-[#D91656]/50 transition-all duration-300">
    <div className="flex items-center justify-between mb-4">
      <div className={`p-3 rounded-xl bg-${color}/10 text-${color}`}>
        {icon}
      </div>
      {trend && (
        <div className={`flex items-center text-xs ${trend === 'up' ? 'text-emerald-500' : 'text-rose-500'}`}>
          {trend === 'up' ? <ArrowUpRight size={16} /> : <ArrowDownRight size={16} />}
          <span className="font-semibold ml-1">{trendValue}</span>
        </div>
      )}
    </div>
    <p className="text-gray-400 text-sm font-medium">{title}</p>
    <h3 className="text-2xl font-bold mt-1">{value}</h3>
  </div>
);

const Dashboard = () => {
  const [stats, setStats] = useState({
    total_products: 0,
    total_orders: 0,
    pending_orders: 0,
    total_inquiries: 0,
    total_revenue: 0
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await api.get('/admin/stats/');
        setStats(response.data);
      } catch (err) {
        console.error("Failed to fetch stats:", err);
      }
    };
    fetchStats();
  }, []);

  return (
    <div className="space-y-8">
      {/* Search Bar */}
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Dashboard</h2>
        <AdminGlobalSearch />
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard 
          title="Total Revenue" 
          value={`₹${stats.total_revenue.toLocaleString()}`} 
          icon={<TrendingUp size={24} />} 
          trend="up" 
          trendValue="+12.5%"
          color="emerald-500"
        />
        <StatCard 
          title="Total Orders" 
          value={stats.total_orders} 
          icon={<ShoppingCart size={24} />} 
          trend="up" 
          trendValue="+8.2%"
          color="blue-500"
        />
        <StatCard 
          title="Active Products" 
          value={stats.total_products} 
          icon={<Package size={24} />} 
          color="[#D91656]"
        />
        <StatCard 
          title="New Inquiries" 
          value={stats.total_inquiries} 
          icon={<MessageSquare size={24} />} 
          trend="up" 
          trendValue="+5"
          color="purple-500"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Recent Orders */}
        <div className="bg-[#161b2a] border border-white/5 rounded-2xl p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-bold">Recent Orders</h3>
            <button className="text-sm text-[#D91656] hover:underline font-medium">View All</button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="text-gray-500 text-sm border-b border-white/5">
                  <th className="pb-4 font-medium">Order ID</th>
                  <th className="pb-4 font-medium">Customer</th>
                  <th className="pb-4 font-medium">Status</th>
                  <th className="pb-4 font-medium">Amount</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {stats.recent_orders?.map((order) => (
                  <tr key={order.id} className="hover:bg-white/5 transition-colors group">
                    <td className="py-4 font-medium">#ORD-{order.id}</td>
                    <td className="py-4 text-gray-300">{order.user_name}</td>
                    <td className="py-4">
                      <span className={`px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider ${
                        order.status === 'PAID' ? 'bg-emerald-500/10 text-emerald-500' : 
                        order.status === 'PENDING' ? 'bg-amber-500/10 text-amber-500' :
                        'bg-blue-500/10 text-blue-500'
                      }`}>
                        {order.status}
                      </span>
                    </td>
                    <td className="py-4 font-bold text-white">₹{order.total_amount}</td>
                  </tr>
                ))}
                {(!stats.recent_orders || stats.recent_orders.length === 0) && (
                  <tr>
                    <td colSpan="4" className="py-8 text-center text-gray-500">No recent orders</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Popular Products */}
        <div className="bg-[#161b2a] border border-white/5 rounded-2xl p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-bold">Popular Products</h3>
            <button className="text-sm text-[#D91656] hover:underline font-medium">View All</button>
          </div>
          <div className="space-y-4">
            {stats.popular_products?.map((product) => (
              <div key={product.id} className="flex items-center justify-between p-3 rounded-xl hover:bg-white/5 transition-colors">
                <div className="flex items-center">
                  <img src={product.image} alt={product.name} className="w-12 h-12 rounded-lg bg-gray-800 mr-4 object-cover border border-white/5" />
                  <div>
                    <p className="font-semibold text-sm">{product.name}</p>
                    <p className="text-xs text-gray-500">{product.category_name}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="font-bold text-sm text-white">₹{product.price}</p>
                  <p className="text-xs text-emerald-400 font-medium">{product.stock} in stock</p>
                </div>
              </div>
            ))}
            {(!stats.popular_products || stats.popular_products.length === 0) && (
              <p className="py-8 text-center text-gray-500">No products found</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
