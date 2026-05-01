import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Package, 
  ShoppingCart, 
  Users, 
  MessageSquare, 
  Settings, 
  LogOut,
  Menu,
  X
} from 'lucide-react';

const AdminLayout = ({ children }) => {
  const [isSidebarOpen, setSidebarOpen] = useState(true);
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = [
    { name: 'Dashboard', icon: <LayoutDashboard size={20} />, path: '/admin-panel' },
    { name: 'Products', icon: <Package size={20} />, path: '/admin-panel/products' },
    { name: 'Orders', icon: <ShoppingCart size={20} />, path: '/admin-panel/orders' },
    { name: 'Inquiries', icon: <MessageSquare size={20} />, path: '/admin-panel/inquiries' },
    { name: 'Settings', icon: <Settings size={20} />, path: '/admin-panel/settings' },
  ];

  const handleLogout = () => {
    // Implement logout logic here
    navigate('/login');
  };

  return (
    <div className="flex h-screen bg-[#0f111a] text-gray-100 font-sans">
      {/* Sidebar */}
      <aside 
        className={`${
          isSidebarOpen ? 'w-64' : 'w-20'
        } transition-all duration-300 bg-[#161b2a] border-r border-white/5 flex flex-col`}
      >
        <div className="p-6 flex items-center justify-between">
          {isSidebarOpen && (
            <span className="text-xl font-bold bg-gradient-to-r from-[#D91656] to-[#ff4d8d] bg-clip-text text-transparent">
              Admin Panel
            </span>
          )}
          <button 
            onClick={() => setSidebarOpen(!isSidebarOpen)}
            className="p-2 hover:bg-white/5 rounded-lg transition-colors"
          >
            {isSidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>

        <nav className="flex-1 mt-6 px-4 space-y-2">
          {menuItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center p-3 rounded-xl transition-all duration-200 ${
                location.pathname === item.path 
                  ? 'bg-[#D91656] text-white shadow-lg shadow-[#D91656]/20' 
                  : 'text-gray-400 hover:bg-white/5 hover:text-white'
              }`}
            >
              <span className="min-w-[24px]">{item.icon}</span>
              {isSidebarOpen && <span className="ml-4 font-medium">{item.name}</span>}
            </Link>
          ))}
        </nav>

        <div className="p-4 border-t border-white/5">
          <button 
            onClick={handleLogout}
            className="flex items-center w-full p-3 text-gray-400 hover:bg-red-500/10 hover:text-red-500 rounded-xl transition-all duration-200"
          >
            <LogOut size={20} />
            {isSidebarOpen && <span className="ml-4 font-medium">Logout</span>}
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        <header className="h-20 border-b border-white/5 bg-[#161b2a]/50 backdrop-blur-md sticky top-0 z-10 px-8 flex items-center justify-between">
          <h1 className="text-2xl font-semibold">
            {menuItems.find(item => item.path === location.pathname)?.name || 'Admin'}
          </h1>
          <div className="flex items-center space-y-4 sm:space-y-0 sm:space-x-4">
            <div className="text-right mr-4 hidden sm:block">
              <p className="text-sm font-medium">Super Admin</p>
              <p className="text-xs text-gray-500">admin@sohamgift.com</p>
            </div>
            <div className="w-10 h-10 rounded-full bg-[#D91656] flex items-center justify-center font-bold">
              A
            </div>
          </div>
        </header>
        
        <div className="p-8">
          {children}
        </div>
      </main>
    </div>
  );
};

export default AdminLayout;
