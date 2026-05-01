import React, { useState, useEffect } from 'react';
import { 
  Plus, 
  Search, 
  Edit2, 
  Trash2, 
  ChevronRight,
  Filter,
  Eye,
  Settings as SettingsIcon,
  CheckCircle2,
  XCircle
} from 'lucide-react';

const ProductManagement = () => {
  const [products, setProducts] = useState([]);
  const [isModalOpen, setModalOpen] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState(null);

  // Mock Products with Customization Zones
  const [mockProducts] = useState([
    {
      id: 1,
      name: "Premium Ceramic Mug",
      category: "Gift Hampers",
      price: 499,
      stock: 120,
      customization_config: [
        { id: "text-1", type: "text", name: "Front Name", placeholder: "Your Name" }
      ],
      is_trending: true
    },
    {
      id: 2,
      name: "Luxury Leather Notebook",
      category: "Office Gifts",
      price: 899,
      stock: 50,
      customization_config: [
        { id: "text-1", type: "text", name: "Logo Text", placeholder: "COMPANY" }
      ],
      is_trending: false
    }
  ]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="relative w-full sm:w-96">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" size={18} />
          <input 
            type="text" 
            placeholder="Search products..." 
            className="w-full bg-[#161b2a] border border-white/5 rounded-xl py-3 pl-12 pr-4 focus:outline-none focus:border-[#D91656] transition-colors"
          />
        </div>
        <button 
          onClick={() => {
            setSelectedProduct(null);
            setModalOpen(true);
          }}
          className="w-full sm:w-auto bg-[#D91656] hover:bg-[#ff1e66] text-white px-6 py-3 rounded-xl font-bold flex items-center justify-center transition-all duration-300 shadow-lg shadow-[#D91656]/20"
        >
          <Plus size={20} className="mr-2" />
          Add Product
        </button>
      </div>

      <div className="bg-[#161b2a] border border-white/5 rounded-2xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="text-gray-500 text-sm border-b border-white/5 bg-white/5">
                <th className="px-6 py-4 font-medium uppercase tracking-wider">Product</th>
                <th className="px-6 py-4 font-medium uppercase tracking-wider">Category</th>
                <th className="px-6 py-4 font-medium uppercase tracking-wider">Price</th>
                <th className="px-6 py-4 font-medium uppercase tracking-wider">Stock</th>
                <th className="px-6 py-4 font-medium uppercase tracking-wider">Customizations</th>
                <th className="px-6 py-4 font-medium uppercase tracking-wider">Trending</th>
                <th className="px-6 py-4 font-medium uppercase tracking-wider text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {mockProducts.map((product) => (
                <tr key={product.id} className="hover:bg-white/5 transition-colors group">
                  <td className="px-6 py-4">
                    <div className="flex items-center">
                      <div className="w-12 h-12 rounded-lg bg-gray-800 mr-4 border border-white/5"></div>
                      <span className="font-semibold">{product.name}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-gray-400">{product.category}</td>
                  <td className="px-6 py-4 font-bold text-white">₹{product.price}</td>
                  <td className="px-6 py-4">
                    <span className={`font-medium ${product.stock < 20 ? 'text-rose-500' : 'text-emerald-500'}`}>
                      {product.stock}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex flex-wrap gap-2">
                      {product.customization_config.map(zone => (
                        <span key={zone.id} className="px-2 py-1 rounded bg-[#D91656]/10 text-[#D91656] text-[10px] font-bold uppercase tracking-tight">
                          {zone.name}
                        </span>
                      ))}
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    {product.is_trending ? (
                      <CheckCircle2 size={20} className="text-emerald-500" />
                    ) : (
                      <XCircle size={20} className="text-gray-600" />
                    )}
                  </td>
                  <td className="px-6 py-4 text-right">
                    <div className="flex items-center justify-end space-x-2">
                      <button className="p-2 hover:bg-white/10 rounded-lg text-gray-400 hover:text-white transition-all">
                        <Edit2 size={18} />
                      </button>
                      <button className="p-2 hover:bg-white/10 rounded-lg text-gray-400 hover:text-rose-500 transition-all">
                        <Trash2 size={18} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal - Simplified for now */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <div className="bg-[#161b2a] border border-white/5 rounded-3xl w-full max-w-2xl overflow-hidden shadow-2xl">
            <div className="p-8 border-b border-white/5 flex items-center justify-between">
              <h2 className="text-2xl font-bold">Add New Product</h2>
              <button onClick={() => setModalOpen(false)} className="p-2 hover:bg-white/5 rounded-full">
                <XCircle size={24} className="text-gray-500" />
              </button>
            </div>
            
            <form className="p-8 space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">Product Name</label>
                  <input type="text" className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:border-[#D91656] outline-none" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">Category</label>
                  <select className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:border-[#D91656] outline-none">
                    <option>Gift Hampers</option>
                    <option>Office Gifts</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2">Customization Zones</label>
                <div className="space-y-4">
                  <div className="flex items-center gap-4 bg-white/5 p-4 rounded-xl border border-white/5">
                    <input type="text" placeholder="Zone Name (e.g. Front Text)" className="flex-1 bg-transparent border-b border-white/10 focus:border-[#D91656] outline-none py-1" />
                    <input type="text" placeholder="Placeholder" className="flex-1 bg-transparent border-b border-white/10 focus:border-[#D91656] outline-none py-1" />
                    <button className="text-rose-500 p-2"><Trash2 size={18} /></button>
                  </div>
                  <button type="button" className="text-sm text-[#D91656] font-bold flex items-center hover:opacity-80">
                    <Plus size={16} className="mr-1" /> Add Zone
                  </button>
                </div>
              </div>

              <div className="flex justify-end gap-4 mt-8 pt-6 border-t border-white/5">
                <button type="button" onClick={() => setModalOpen(false)} className="px-6 py-3 rounded-xl border border-white/10 hover:bg-white/5 transition-all">Cancel</button>
                <button type="submit" className="px-8 py-3 rounded-xl bg-[#D91656] text-white font-bold shadow-lg shadow-[#D91656]/20">Save Product</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProductManagement;
