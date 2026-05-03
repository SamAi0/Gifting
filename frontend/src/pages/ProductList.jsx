import { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { Search, Filter, ChevronDown, Package, Gift, LayoutGrid, List, ChevronRight } from 'lucide-react';
import { fetchProducts, fetchCategories, getImageUrl } from '../api';
import { ProductCardSkeleton } from '../components/Skeleton';
import { motion, AnimatePresence } from 'framer-motion';

const ProductList = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState(searchParams.get('search') || "");
  const [selectedCategory, setSelectedCategory] = useState(searchParams.get('category') || "");
  const [minPrice, setMinPrice] = useState(searchParams.get('min_price') || "");
  const [maxPrice, setMaxPrice] = useState(searchParams.get('max_price') || "");
  const [viewMode, setViewMode] = useState('grid');
  const [sortBy, setSortBy] = useState(searchParams.get('ordering') || '-created_at');

  useEffect(() => {
    const updateURL = () => {
      const params = {};
      if (selectedCategory) params.category = selectedCategory;
      if (searchQuery) params.search = searchQuery;
      if (minPrice) params.min_price = minPrice;
      if (maxPrice) params.max_price = maxPrice;
      if (sortBy) params.ordering = sortBy;
      setSearchParams(params);
    };

    const loadData = async () => {
      setLoading(true);
      try {
        const catRes = await fetchCategories();
        setCategories(catRes.data);
        
        const params = {};
        if (selectedCategory) params.category = selectedCategory;
        if (searchQuery) params.search = searchQuery;
        if (minPrice) params.min_price = minPrice;
        if (maxPrice) params.max_price = maxPrice;
        if (sortBy) params.ordering = sortBy;
        
        const prodRes = await fetchProducts(params);
        setProducts(prodRes.data);
      } catch (error) {
        console.error("Error loading products:", error);
      } finally {
        setLoading(false);
      }
    };

    const timer = setTimeout(() => {
      loadData();
      updateURL();
    }, 400); // Debounce

    return () => clearTimeout(timer);
  }, [selectedCategory, searchQuery, sortBy, minPrice, maxPrice, setSearchParams]);

  return (
    <div className="pt-32 pb-32 bg-slate-50 min-h-screen">
      <div className="container-custom">
        {/* Header Section */}
        <div className="flex flex-col md:flex-row justify-between items-end mb-16 gap-8">
          <div className="max-w-2xl">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
            >
              <h1 className="text-4xl md:text-6xl font-bold text-slate-900 mb-4 tracking-tight">
                Explore Our <span className="text-primary italic">Catalog</span>
              </h1>
              <p className="text-lg text-slate-500 leading-relaxed font-light">
                Premium corporate gifts curated for quality and impact. Find the perfect appreciation for your team and partners.
              </p>
            </motion.div>
          </div>
          
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="relative w-full md:w-96 group"
          >
            <div className="absolute left-5 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-primary transition-colors">
              <Search size={20} />
            </div>
            <input 
              type="text" 
              placeholder="Search premium gifts..."
              className="w-full pl-14 pr-6 py-5 rounded-[1.5rem] bg-white border border-slate-200 focus:outline-none focus:ring-4 focus:ring-primary/5 focus:border-primary shadow-premium transition-all text-slate-700"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </motion.div>
        </div>

        <div className="flex flex-col lg:flex-row gap-16">
          {/* Sidebar Filters */}
          <aside className="w-full lg:w-80 space-y-10">
            <div className="glass-card p-8 border-slate-200/50">
              <div className="flex items-center gap-3 mb-8 font-bold text-slate-900 text-lg">
                <Filter size={20} className="text-primary" />
                Filter by Category
              </div>
              <div className="space-y-2">
                <button 
                  onClick={() => setSelectedCategory("")}
                  className={`w-full text-left px-5 py-3.5 rounded-xl transition-all duration-300 font-medium text-sm flex items-center justify-between ${
                    selectedCategory === "" 
                    ? 'bg-primary text-white shadow-lg shadow-primary/20' 
                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
                  }`}
                >
                  All Collections
                  <ChevronDown size={14} className={selectedCategory === "" ? 'rotate-180' : ''} />
                </button>
                {categories.map((cat) => (
                  <button 
                    key={cat.id}
                    onClick={() => setSelectedCategory(cat.id.toString())}
                    className={`w-full text-left px-5 py-3.5 rounded-xl transition-all duration-300 font-medium text-sm flex justify-between items-center ${
                      selectedCategory === cat.id.toString() 
                      ? 'bg-primary text-white shadow-lg shadow-primary/20' 
                      : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
                    }`}
                  >
                    <span>{cat.name}</span>
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                      selectedCategory === cat.id.toString() ? 'bg-white/20 text-white' : 'bg-slate-100 text-slate-400'
                    }`}>
                      {cat.product_count}
                    </span>
                  </button>
                ))}
              </div>
            </div>

            {/* Price Filter */}
            <div className="glass-card p-8 border-slate-200/50">
              <div className="flex items-center gap-3 mb-8 font-bold text-slate-900 text-lg">
                <Filter size={20} className="text-primary" />
                Price Range
              </div>
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Min (₹)</label>
                    <input 
                      type="number" 
                      placeholder="0"
                      className="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-100 focus:outline-none focus:border-primary text-sm font-bold"
                      value={minPrice}
                      onChange={(e) => setMinPrice(e.target.value)}
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Max (₹)</label>
                    <input 
                      type="number" 
                      placeholder="5000"
                      className="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-100 focus:outline-none focus:border-primary text-sm font-bold"
                      value={maxPrice}
                      onChange={(e) => setMaxPrice(e.target.value)}
                    />
                  </div>
                </div>
                {(minPrice || maxPrice) && (
                  <button 
                    onClick={() => {setMinPrice(""); setMaxPrice("");}}
                    className="w-full py-2 text-xs font-bold text-primary hover:text-primary-dark transition-colors uppercase tracking-widest"
                  >
                    Clear Price
                  </button>
                )}
              </div>
            </div>

            {/* Bulk Promo Card */}
            <div className="bg-slate-900 rounded-[2.5rem] p-10 text-white relative overflow-hidden shadow-2xl">
                <div className="absolute -top-10 -right-10 w-40 h-40 bg-primary/20 rounded-full blur-3xl"></div>
                <Gift className="text-primary mb-6" size={32} />
                <h4 className="text-2xl font-bold mb-4 leading-tight">Need a Bulk Solution?</h4>
                <p className="text-slate-400 text-sm mb-8 leading-relaxed">
                  Unlock wholesale pricing and dedicated customization experts for orders over 50 units.
                </p>
                <Link to="/bulk-inquiry" className="btn-primary w-full py-4 text-sm font-bold shadow-none hover:bg-white hover:text-slate-900">
                   Get Bulk Quote
                </Link>
            </div>
          </aside>

          {/* Product Grid Area */}
          <main className="flex-grow">
            <div className="flex justify-between items-center mb-10 bg-white p-5 rounded-2xl shadow-sm border border-slate-100">
               <span className="text-slate-500 font-medium text-sm">
                  Showing <span className="text-slate-900 font-bold">{products.length}</span> Premium Results
               </span>
               <div className="flex items-center gap-4">
                  <div className="flex bg-slate-100 p-1 rounded-lg">
                    <button 
                      onClick={() => setViewMode('grid')}
                      className={`p-1.5 rounded-md transition-colors ${viewMode === 'grid' ? 'bg-white text-primary shadow-sm' : 'text-slate-400'}`}
                    >
                      <LayoutGrid size={18} />
                    </button>
                    <button 
                      onClick={() => setViewMode('list')}
                      className={`p-1.5 rounded-md transition-colors ${viewMode === 'list' ? 'bg-white text-primary shadow-sm' : 'text-slate-400'}`}
                    >
                      <List size={18} />
                    </button>
                  </div>
                  <div className="h-6 w-px bg-slate-200"></div>
                  <select 
                    value={sortBy}
                    onChange={(e) => setSortBy(e.target.value)}
                    className="flex items-center gap-2 text-slate-900 font-bold text-sm cursor-pointer hover:text-primary transition-colors bg-transparent border-none outline-none"
                  >
                    <option value="-created_at">Newest First</option>
                    <option value="created_at">Oldest First</option>
                    <option value="price">Price: Low to High</option>
                    <option value="-price">Price: High to Low</option>
                    <option value="name">Name: A-Z</option>
                    <option value="-name">Name: Z-A</option>
                  </select>
               </div>
            </div>

            <AnimatePresence mode="wait">
              {loading ? (
                <motion.div 
                  key="loading"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10"
                >
                   {[1,2,3,4,5,6].map(n => <ProductCardSkeleton key={n} />)}
                </motion.div>
              ) : products.length > 0 ? (
                <motion.div 
                  key="content"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10"
                >
                  {products.map((product, idx) => (
                    <motion.div 
                      key={product.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: idx * 0.05 }}
                      className="group"
                    >
                      <div className="bg-white rounded-[2.5rem] shadow-premium hover-lift transition-all duration-500 overflow-hidden border border-transparent hover:border-slate-100">
                        <div className="relative aspect-[4/5] overflow-hidden bg-slate-50">
                          <img 
                            src={getImageUrl(product.image) || `https://images.unsplash.com/photo-1513201099705-a9746e1e201f?auto=format&fit=crop&w=800&q=80`} 
                            className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                            alt={product.name}
                          />
                          
                          {/* Badges */}
                          <div className="absolute top-5 left-5 flex flex-col gap-2">
                            {product.badge_text ? (
                              <div 
                                className="text-[9px] font-black px-3 py-1.5 rounded-full uppercase tracking-widest z-10 shadow-lg text-white"
                                style={{ backgroundColor: product.badge_color || 'var(--color-primary)' }}
                              >
                                {product.badge_text}
                              </div>
                            ) : null}
                            {product.stock === 0 && (
                              <div className="bg-slate-900 text-white text-[9px] font-black px-3 py-1.5 rounded-full uppercase tracking-widest">Out of Stock</div>
                            )}
                          </div>

                          <div className="absolute inset-0 bg-slate-900/40 backdrop-blur-[2px] flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-300">
                             <Link to={`/products/${product.id}`} className="bg-white text-slate-900 font-bold px-8 py-3 rounded-xl transform translate-y-4 group-hover:translate-y-0 transition-all duration-300 shadow-2xl">
                               View Details
                             </Link>
                          </div>
                        </div>

                        <div className="p-8">
                          <p className="text-primary text-[10px] font-black uppercase tracking-[0.25em] mb-3">{product.category_name}</p>
                          <h3 className="text-xl font-bold text-slate-900 mb-3 group-hover:text-primary transition-colors line-clamp-1">{product.name}</h3>
                          <p className="text-slate-500 text-sm mb-8 line-clamp-2 leading-relaxed font-light">{product.description}</p>
                          
                          <div className="flex justify-between items-center pt-6 border-t border-slate-50">
                            <div>
                              <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest mb-1">Price Est.</p>
                              <div className="flex items-center gap-2">
                                <p className="text-2xl font-bold text-slate-900 tracking-tight">₹{product.price}</p>
                                {product.discount_price && (
                                  <p className="text-sm text-slate-400 line-through">₹{product.discount_price}</p>
                                )}
                              </div>
                              {product.stock > 0 && product.stock <= 5 && (
                                <p className="text-xs text-orange-600 font-semibold mt-1">Only {product.stock} left</p>
                              )}
                            </div>
                            <Link 
                              to={product.stock === 0 ? '#' : `/products/${product.id}`} 
                              className={`p-3 rounded-2xl transition-all duration-300 ${
                                product.stock === 0 ? 'bg-slate-200 text-slate-400 cursor-not-allowed' : 'bg-slate-100 text-slate-600 hover:bg-primary hover:text-white'
                              }`}
                              onClick={(e) => product.stock === 0 && e.preventDefault()}
                            >
                               <ChevronRight size={20} />
                            </Link>
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </motion.div>
              ) : (
                <motion.div 
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="text-center py-40 bg-white rounded-[3rem] border border-dashed border-slate-200"
                >
                   <div className="w-24 h-24 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-6 text-slate-200">
                      <Package size={48} />
                   </div>
                   <h3 className="text-2xl font-bold text-slate-900 mb-2">No results found</h3>
                   <p className="text-slate-400 mb-10 max-w-xs mx-auto">We couldn't find any gifts matching your search or filters.</p>
                   <button 
                    onClick={() => {setSelectedCategory(""); setSearchQuery(""); setMinPrice(""); setMaxPrice("");}} 
                    className="btn-primary"
                   >
                     Clear All Filters
                   </button>
                </motion.div>
              )}
            </AnimatePresence>
          </main>
        </div>
      </div>
    </div>
  );
};

export default ProductList;

