import { useState, useEffect, useCallback } from 'react';
import api, { fetchCategories, createProduct, updateProduct, deleteProduct } from '../../api';
import { 
  Plus, 
  Search, 
  Edit2, 
  Trash2, 
  CheckCircle2,
  XCircle,
  Image as ImageIcon
} from 'lucide-react';

const ProductManagement = () => {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [isModalOpen, setModalOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // Form State
  const [formData, setFormData] = useState({
    name: '',
    category: '',
    price: '',
    discount_price: '',
    stock: '',
    description: '',
    is_trending: false,
    is_bulk_only: false,
    customization_zones: []
  });
  const [selectedImage, setSelectedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);

  const fetchData = useCallback(async () => {
    try {
      const [prodRes, catRes] = await Promise.all([
        api.get('/products/'),
        fetchCategories()
      ]);
      setProducts(prodRes.data);
      setCategories(catRes.data);
    } catch (err) {
      console.error("Failed to fetch data:", err);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
  };

  const filteredProducts = products.filter(p => 
    p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.category_name?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const openModal = (product = null) => {
    if (product) {
      setEditingProduct(product);
      setFormData({
        name: product.name,
        category: product.category,
        price: product.price,
        discount_price: product.discount_price || '',
        stock: product.stock,
        description: product.description,
        is_trending: product.is_trending,
        is_bulk_only: product.is_bulk_only,
        customization_zones: product.customization_zones || []
      });
      setImagePreview(product.image);
    } else {
      setEditingProduct(null);
      setFormData({
        name: '',
        category: categories[0]?.id || '',
        price: '',
        discount_price: '',
        stock: '10',
        description: '',
        is_trending: false,
        is_bulk_only: false,
        customization_zones: []
      });
      setImagePreview(null);
    }
    setSelectedImage(null);
    setModalOpen(true);
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(file);
      setImagePreview(URL.createObjectURL(file));
    }
  };

  const handleAddZone = () => {
    setFormData({
      ...formData,
      customization_zones: [
        ...formData.customization_zones,
        { name: '', placeholder: '', type: 'text', maxLength: 20 }
      ]
    });
  };

  const handleRemoveZone = (idx) => {
    const newZones = [...formData.customization_zones];
    newZones.splice(idx, 1);
    setFormData({ ...formData, customization_zones: newZones });
  };

  const handleZoneChange = (idx, field, value) => {
    const newZones = [...formData.customization_zones];
    newZones[idx][field] = value;
    setFormData({ ...formData, customization_zones: newZones });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const data = new FormData();
      Object.keys(formData).forEach(key => {
        if (key === 'customization_zones') {
          data.append('customization_config', JSON.stringify(formData[key]));
        } else {
          data.append(key, formData[key]);
        }
      });

      if (selectedImage) {
        data.append('image', selectedImage);
      }

      if (editingProduct) {
        await updateProduct(editingProduct.id, data);
      } else {
        await createProduct(data);
      }

      setModalOpen(false);
      fetchData();
    } catch (err) {
      console.error("Save failed:", err);
      alert("Failed to save product. Check console for details.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this product?')) {
      try {
        await deleteProduct(id);
        fetchData();
      } catch (err) {
        console.error("Delete failed:", err);
      }
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="relative w-full sm:w-96">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" size={18} />
          <input 
            type="text" 
            placeholder="Search products or categories..." 
            value={searchTerm}
            onChange={handleSearch}
            className="w-full bg-[#161b2a] border border-white/5 rounded-xl py-3 pl-12 pr-4 focus:outline-none focus:border-[#D91656] transition-colors"
          />
        </div>
        <button 
          onClick={() => openModal()}
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
                <th className="px-6 py-4 font-medium uppercase tracking-wider text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {filteredProducts.map((product) => (
                <tr key={product.id} className="hover:bg-white/5 transition-colors group">
                  <td className="px-6 py-4">
                    <div className="flex items-center">
                      <img src={product.image} alt={product.name} className="w-12 h-12 rounded-lg bg-gray-800 mr-4 border border-white/5 object-cover" />
                      <div>
                        <span className="font-semibold block">{product.name}</span>
                        {product.is_trending && <span className="text-[10px] text-emerald-500 font-bold uppercase">Trending</span>}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-gray-400">{product.category_name}</td>
                  <td className="px-6 py-4">
                    <span className="font-bold text-white">₹{product.price}</span>
                    {product.discount_price && <span className="text-xs text-gray-500 line-through ml-2">₹{product.discount_price}</span>}
                  </td>
                  <td className="px-6 py-4">
                    <span className={`font-medium ${product.stock < 10 ? 'text-rose-500' : 'text-emerald-500'}`}>
                      {product.stock}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex flex-wrap gap-1">
                      {product.customization_zones?.map((zone, idx) => (
                        <span key={idx} className="px-2 py-0.5 rounded bg-white/5 text-gray-400 text-[9px] font-bold uppercase">
                          {zone.name}
                        </span>
                      ))}
                      {(!product.customization_zones || product.customization_zones.length === 0) && <span className="text-gray-600 text-xs">-</span>}
                    </div>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <div className="flex items-center justify-end space-x-2">
                      <button 
                        onClick={() => openModal(product)}
                        className="p-2 hover:bg-white/10 rounded-lg text-gray-400 hover:text-white transition-all"
                      >
                        <Edit2 size={18} />
                      </button>
                      <button 
                        onClick={() => handleDelete(product.id)}
                        className="p-2 hover:bg-white/10 rounded-lg text-gray-400 hover:text-rose-500 transition-all"
                      >
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

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 overflow-y-auto">
          <div className="bg-[#161b2a] border border-white/5 rounded-3xl w-full max-w-3xl overflow-hidden shadow-2xl my-8">
            <div className="p-6 border-b border-white/5 flex items-center justify-between">
              <h2 className="text-2xl font-bold">{editingProduct ? 'Edit Product' : 'Add New Product'}</h2>
              <button onClick={() => setModalOpen(false)} className="p-2 hover:bg-white/5 rounded-full">
                <XCircle size={24} className="text-gray-500" />
              </button>
            </div>
            
            <form onSubmit={handleSubmit} className="p-6 space-y-6 max-h-[70vh] overflow-y-auto custom-scrollbar">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Image Upload */}
                <div className="md:col-span-2">
                   <label className="block text-sm font-medium text-gray-400 mb-2">Product Image</label>
                   <div className="flex items-center gap-6">
                      <div className="w-32 h-32 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center overflow-hidden relative group">
                        {imagePreview ? (
                          <img src={imagePreview} className="w-full h-full object-cover" />
                        ) : (
                          <ImageIcon size={32} className="text-gray-600" />
                        )}
                        <input 
                          type="file" 
                          onChange={handleImageChange}
                          className="absolute inset-0 opacity-0 cursor-pointer"
                          accept="image/*"
                        />
                        <div className="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
                          <span className="text-xs font-bold">Change</span>
                        </div>
                      </div>
                      <div className="text-xs text-gray-500 space-y-1">
                        <p>Click the box to upload a high-quality product image.</p>
                        <p>Recommended size: 800x800px</p>
                      </div>
                   </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">Product Name</label>
                  <input 
                    type="text" 
                    required
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:border-[#D91656] outline-none transition-colors" 
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">Category</label>
                  <select 
                    value={formData.category}
                    onChange={(e) => setFormData({...formData, category: e.target.value})}
                    className="w-full bg-[#161b2a] border border-white/10 rounded-xl px-4 py-3 focus:border-[#D91656] outline-none transition-colors"
                  >
                    {categories.map(cat => (
                      <option key={cat.id} value={cat.id}>{cat.name}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">Price (₹)</label>
                  <input 
                    type="number" 
                    required
                    value={formData.price}
                    onChange={(e) => setFormData({...formData, price: e.target.value})}
                    className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:border-[#D91656] outline-none" 
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">Stock</label>
                  <input 
                    type="number" 
                    required
                    value={formData.stock}
                    onChange={(e) => setFormData({...formData, stock: e.target.value})}
                    className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:border-[#D91656] outline-none" 
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2">Description</label>
                <textarea 
                  rows="3"
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                  className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:border-[#D91656] outline-none resize-none"
                ></textarea>
              </div>

              <div className="flex gap-6">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input 
                    type="checkbox" 
                    checked={formData.is_trending}
                    onChange={(e) => setFormData({...formData, is_trending: e.target.checked})}
                    className="w-5 h-5 rounded border-white/10 bg-white/5 text-[#D91656] focus:ring-[#D91656]" 
                  />
                  <span className="text-sm font-medium text-gray-300">Trending Product</span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input 
                    type="checkbox" 
                    checked={formData.is_bulk_only}
                    onChange={(e) => setFormData({...formData, is_bulk_only: e.target.checked})}
                    className="w-5 h-5 rounded border-white/10 bg-white/5 text-[#D91656] focus:ring-[#D91656]" 
                  />
                  <span className="text-sm font-medium text-gray-300">Bulk Orders Only</span>
                </label>
              </div>

              <div className="border-t border-white/5 pt-6">
                <div className="flex items-center justify-between mb-4">
                   <label className="text-sm font-medium text-gray-400">Customization Zones</label>
                   <button 
                    type="button" 
                    onClick={handleAddZone}
                    className="text-xs text-[#D91656] font-bold flex items-center hover:opacity-80"
                   >
                     <Plus size={14} className="mr-1" /> Add Zone
                   </button>
                </div>
                <div className="space-y-3">
                  {formData.customization_zones.map((zone, idx) => (
                    <div key={idx} className="flex items-center gap-3 bg-white/5 p-3 rounded-xl border border-white/5">
                      <input 
                        type="text" 
                        placeholder="Zone Name" 
                        value={zone.name}
                        onChange={(e) => handleZoneChange(idx, 'name', e.target.value)}
                        className="flex-1 bg-transparent border-b border-white/10 focus:border-[#D91656] outline-none py-1 text-sm" 
                      />
                      <input 
                        type="text" 
                        placeholder="Placeholder" 
                        value={zone.placeholder}
                        onChange={(e) => handleZoneChange(idx, 'placeholder', e.target.value)}
                        className="flex-1 bg-transparent border-b border-white/10 focus:border-[#D91656] outline-none py-1 text-sm" 
                      />
                      <button 
                        type="button"
                        onClick={() => handleRemoveZone(idx)}
                        className="text-rose-500 p-2 hover:bg-rose-500/10 rounded-lg transition-colors"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                  ))}
                  {formData.customization_zones.length === 0 && (
                    <p className="text-center py-4 text-xs text-gray-600 border-2 border-dashed border-white/5 rounded-xl">
                      No customization zones defined for this product.
                    </p>
                  )}
                </div>
              </div>

              <div className="flex justify-end gap-4 mt-8 pt-6 border-t border-white/5">
                <button 
                  type="button" 
                  onClick={() => setModalOpen(false)} 
                  className="px-6 py-3 rounded-xl border border-white/10 hover:bg-white/5 transition-all text-sm font-medium"
                >
                  Cancel
                </button>
                <button 
                  type="submit" 
                  disabled={isLoading}
                  className="px-8 py-3 rounded-xl bg-[#D91656] text-white font-bold shadow-lg shadow-[#D91656]/20 disabled:opacity-50 flex items-center"
                >
                  {isLoading ? 'Saving...' : (editingProduct ? 'Update Product' : 'Save Product')}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProductManagement;
