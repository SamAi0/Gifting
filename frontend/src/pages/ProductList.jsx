import { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { Search, Filter, Package, LayoutGrid, List, ChevronRight } from 'lucide-react';
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
  const [currentPage, setCurrentPage] = useState(parseInt(searchParams.get('page')) || 1);
  const [totalCount, setTotalCount] = useState(0);

  useEffect(() => {
    const updateURL = () => {
      const params = {};
      if (selectedCategory) params.category = selectedCategory;
      if (searchQuery) params.search = searchQuery;
      if (minPrice) params.min_price = minPrice;
      if (maxPrice) params.max_price = maxPrice;
      if (sortBy) params.ordering = sortBy;
      if (currentPage > 1) params.page = currentPage;
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
        params.page = currentPage;
        
        const prodRes = await fetchProducts(params);
        setProducts(prodRes.data.results || prodRes.data);
        setTotalCount(prodRes.data.count || (prodRes.data.results ? prodRes.data.results.length : prodRes.data.length));
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
  }, [selectedCategory, searchQuery, sortBy, minPrice, maxPrice, currentPage, setSearchParams]);

  return (
    <div className="pt-32 pb-32 bg-slate-50 min-h-screen">
      <div className="container-wide">
        {/* Header Section */}
        <div className="flex flex-col md:flex-row justify-between items-end mb-12 gap-8">
          <div className="max-w-2xl">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
            >
              <h1 className="text-4xl md:text-5xl font-bold text-slate-900 mb-4 tracking-tight">
                Our Premium <span className="text-primary italic">Catalog</span>
              </h1>
              <p className="text-base text-slate-500 leading-relaxed font-light">
                Discover curated corporate gifts designed for impact and quality.
              </p>
            </motion.div>
          </div>
          
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="relative w-full md:w-96 group"
          >
            <div className="absolute left-5 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-primary transition-colors">
              <Search size={18} />
            </div>
            <input 
              type="text" 
              placeholder="Search gifts..."
              className="w-full pl-12 pr-6 py-4 rounded-2xl bg-white border border-slate-200 focus:outline-none focus:ring-4 focus:ring-primary/5 focus:border-primary shadow-sm transition-all text-sm"
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value);
                setCurrentPage(1);
              }}
            />
          </motion.div>
        </div>

        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar Filters */}
          <aside className="w-full lg:w-72 space-y-6">
            <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden sticky top-32">
              {/* Category Filter */}
              <div className="p-6 border-b border-slate-100">
                <div className="flex items-center gap-2 mb-6 font-bold text-slate-900 text-sm uppercase tracking-widest">
                  <LayoutGrid size={16} className="text-primary" />
                  Categories
                </div>
                <div className="space-y-1 max-h-[400px] overflow-y-auto pr-2 scrollbar-hide">
                  <button 
                    onClick={() => {
                      setSelectedCategory("");
                      setCurrentPage(1);
                    }}
                    className={`w-full text-left px-4 py-2.5 rounded-xl transition-all duration-200 font-bold text-xs flex items-center justify-between group ${
                      selectedCategory === "" 
                      ? 'bg-primary text-white shadow-md shadow-primary/20' 
                      : 'text-slate-600 hover:bg-slate-50 hover:text-primary'
                    }`}
                  >
                    All Collections
                  </button>
                  {categories.map((cat) => (
                    <button 
                      key={cat.id}
                      onClick={() => {
                        setSelectedCategory(cat.id.toString());
                        setCurrentPage(1);
                      }}
                      className={`w-full text-left px-4 py-2.5 rounded-xl transition-all duration-200 font-bold text-xs flex justify-between items-center group ${
                        selectedCategory === cat.id.toString() 
                        ? 'bg-primary text-white shadow-md shadow-primary/20' 
                        : 'text-slate-600 hover:bg-slate-50 hover:text-primary'
                      }`}
                    >
                      <span className="truncate pr-2">{cat.name}</span>
                      <span className={`px-1.5 py-0.5 rounded-md text-[9px] font-black ${
                        selectedCategory === cat.id.toString() ? 'bg-white/20 text-white' : 'bg-slate-100 text-slate-400 group-hover:bg-primary/10 group-hover:text-primary'
                      }`}>
                        {cat.product_count}
                      </span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Price Filter */}
              <div className="p-6">
                <div className="flex items-center gap-2 mb-6 font-bold text-slate-900 text-sm uppercase tracking-widest">
                  <Filter size={16} className="text-primary" />
                  Price Range
                </div>
                <div className="space-y-4">
                  <div className="flex items-center gap-3">
                    <div className="flex-grow relative">
                      <span className="absolute left-3 top-1/2 -translate-y-1/2 text-[10px] text-slate-400 font-bold">₹</span>
                      <input 
                        type="number" 
                        placeholder="Min"
                        className="w-full pl-6 pr-3 py-2.5 rounded-xl bg-slate-50 border border-slate-100 focus:outline-none focus:border-primary text-xs font-bold"
                        value={minPrice}
                        onChange={(e) => {
                          setMinPrice(e.target.value);
                          setCurrentPage(1);
                        }}
                      />
                    </div>
                    <div className="w-2 h-px bg-slate-300"></div>
                    <div className="flex-grow relative">
                      <span className="absolute left-3 top-1/2 -translate-y-1/2 text-[10px] text-slate-400 font-bold">₹</span>
                      <input 
                        type="number" 
                        placeholder="Max"
                        className="w-full pl-6 pr-3 py-2.5 rounded-xl bg-slate-50 border border-slate-100 focus:outline-none focus:border-primary text-xs font-bold"
                        value={maxPrice}
                        onChange={(e) => {
                          setMaxPrice(e.target.value);
                          setCurrentPage(1);
                        }}
                      />
                    </div>
                  </div>
                  {(minPrice || maxPrice) && (
                    <button 
                      onClick={() => {
                        setMinPrice(""); 
                        setMaxPrice("");
                        setCurrentPage(1);
                      }}
                      className="w-full py-2 text-[10px] font-black text-primary hover:bg-primary/5 rounded-lg transition-all uppercase tracking-widest"
                    >
                      Reset Price
                    </button>
                  )}
                </div>
              </div>
            </div>
          </aside>

          {/* Product Grid Area */}
          <main className="flex-grow">
            <div className="flex flex-wrap justify-between items-center mb-8 gap-4">
               <div className="flex items-center gap-3">
                 <span className="text-slate-900 font-black text-xs uppercase tracking-widest">
                    {totalCount} Products
                 </span>
                 <div className="h-4 w-px bg-slate-300"></div>
                 <div className="flex gap-2">
                    <button 
                      onClick={() => setViewMode('grid')}
                      className={`p-1.5 rounded-lg transition-all ${viewMode === 'grid' ? 'bg-primary text-white shadow-sm' : 'text-slate-400 hover:bg-slate-200'}`}
                    >
                      <LayoutGrid size={16} />
                    </button>
                    <button 
                      onClick={() => setViewMode('list')}
                      className={`p-1.5 rounded-lg transition-all ${viewMode === 'list' ? 'bg-primary text-white shadow-sm' : 'text-slate-400 hover:bg-slate-200'}`}
                    >
                      <List size={16} />
                    </button>
                 </div>
               </div>
               
               <div className="flex items-center gap-2">
                  <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Sort:</span>
                  <select 
                    value={sortBy}
                    onChange={(e) => {
                      setSortBy(e.target.value);
                      setCurrentPage(1);
                    }}
                    className="bg-white border border-slate-200 rounded-xl px-4 py-2 text-xs font-bold text-slate-700 outline-none focus:border-primary transition-all cursor-pointer shadow-sm"
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
                  className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-6"
                >
                   {[1,2,3,4,5,6,7,8].map(n => <ProductCardSkeleton key={n} />)}
                </motion.div>
              ) : products.length > 0 ? (
                <motion.div 
                  key="content"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className={`grid gap-6 ${
                    viewMode === 'grid' 
                      ? 'grid-cols-1 sm:grid-cols-2 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4' 
                      : 'grid-cols-1'
                  }`}
                >
                  {products.map((product, idx) => (
                    <motion.div 
                      key={product.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: idx * 0.03 }}
                      className="group"
                    >
                      <div className={`bg-white rounded-3xl border border-slate-100 hover:border-primary/20 transition-all duration-300 overflow-hidden shadow-sm hover:shadow-xl ${viewMode === 'list' ? 'flex flex-col md:flex-row' : ''}`}>
                        <div className={`relative overflow-hidden bg-slate-50 ${viewMode === 'list' ? 'md:w-64 aspect-square' : 'aspect-[4/5]'}`}>
                          <img 
                            src={getImageUrl(product.image) || `https://images.unsplash.com/photo-1513201099705-a9746e1e201f?auto=format&fit=crop&w=800&q=80`} 
                            className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                            alt={product.name}
                          />
                          
                          {/* Badges */}
                          <div className="absolute top-4 left-4 flex flex-col gap-2">
                            {product.badge_text ? (
                              <div 
                                className="text-[8px] font-black px-2.5 py-1 rounded-full uppercase tracking-widest z-10 shadow-lg text-white"
                                style={{ backgroundColor: product.badge_color || 'var(--color-primary)' }}
                              >
                                {product.badge_text}
                              </div>
                            ) : null}
                          </div>

                          <div className="absolute inset-0 bg-slate-900/40 backdrop-blur-[2px] flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-300">
                             <Link to={`/products/${product.id}`} className="bg-white text-slate-900 font-bold px-6 py-2.5 rounded-xl text-sm transform translate-y-4 group-hover:translate-y-0 transition-all duration-300">
                               Details
                             </Link>
                          </div>
                        </div>

                        <div className={`p-6 flex flex-col flex-grow ${viewMode === 'list' ? 'justify-center' : ''}`}>
                          <div className="flex justify-between items-start mb-2">
                            <p className="text-primary text-[9px] font-black uppercase tracking-widest">{product.category_name}</p>
                            <span className="text-[10px] font-bold text-slate-400">ID: #{product.id}</span>
                          </div>
                          <h3 className="text-lg font-bold text-slate-900 mb-2 group-hover:text-primary transition-colors line-clamp-1">{product.name}</h3>
                          <p className="text-slate-500 text-xs mb-6 line-clamp-2 leading-relaxed font-light">{product.description}</p>
                          
                          <div className="mt-auto flex justify-between items-center pt-4 border-t border-slate-50">
                            <div>
                              <div className="flex items-center gap-2">
                                <p className="text-xl font-bold text-slate-900 tracking-tight">₹{product.price}</p>
                                {product.discount_price && (
                                  <p className="text-xs text-slate-400 line-through">₹{product.discount_price}</p>
                                )}
                              </div>
                            </div>
                            <Link 
                              to={`/products/${product.id}`} 
                              className="w-10 h-10 rounded-xl bg-slate-50 text-slate-400 flex items-center justify-center group-hover:bg-primary group-hover:text-white transition-all"
                            >
                               <ChevronRight size={18} />
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
                  className="text-center py-32 bg-white rounded-3xl border-2 border-dashed border-slate-100"
                >
                   <div className="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-6 text-slate-200">
                      <Package size={40} />
                   </div>
                   <h3 className="text-xl font-bold text-slate-900 mb-2">No gifts found</h3>
                   <p className="text-slate-400 text-sm mb-8 max-w-xs mx-auto">Try adjusting your filters to find what you're looking for.</p>
                   <button 
                    onClick={() => {setSelectedCategory(""); setSearchQuery(""); setMinPrice(""); setMaxPrice("");}} 
                    className="btn-primary py-2.5 px-6 text-xs"
                   >
                     Clear Filters
                   </button>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Pagination Controls */}
            {totalCount > 20 && (
              <div className="mt-12 flex justify-center items-center gap-2">
                <button 
                  onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                  disabled={currentPage === 1}
                  className="p-2 rounded-xl bg-white border border-slate-200 text-slate-400 hover:text-primary disabled:opacity-50 transition-all"
                >
                  <ChevronRight size={20} className="rotate-180" />
                </button>
                
                {Array.from({ length: Math.ceil(totalCount / 20) }).map((_, i) => (
                  <button
                    key={i}
                    onClick={() => setCurrentPage(i + 1)}
                    className={`w-10 h-10 rounded-xl font-bold text-xs transition-all ${
                      currentPage === i + 1 
                        ? 'bg-primary text-white shadow-lg shadow-primary/20' 
                        : 'bg-white border border-slate-200 text-slate-600 hover:border-primary/40'
                    }`}
                  >
                    {i + 1}
                  </button>
                ))}

                <button 
                  onClick={() => setCurrentPage(p => Math.min(Math.ceil(totalCount / 20), p + 1))}
                  disabled={currentPage === Math.ceil(totalCount / 20)}
                  className="p-2 rounded-xl bg-white border border-slate-200 text-slate-400 hover:text-primary disabled:opacity-50 transition-all"
                >
                  <ChevronRight size={20} />
                </button>
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  );
};

export default ProductList;

