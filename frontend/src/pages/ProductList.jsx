import { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { Search, Filter, Package, LayoutGrid, List, ChevronRight, X, Star } from 'lucide-react';
import { fetchProducts, fetchCategories, getImageUrl } from '../api';
import { ProductCardSkeleton } from '../components/Skeleton';
import { motion, AnimatePresence } from 'framer-motion';
import VoiceSearch from '../components/VoiceSearch';

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
  
  // Advanced Filter States
  const [isAvailable, setIsAvailable] = useState(searchParams.get('is_available') === 'true');
  const [onSale, setOnSale] = useState(searchParams.get('on_sale') === 'true');
  const [minRating, setMinRating] = useState(searchParams.get('min_rating') || "");
  const [isMobileFilterOpen, setIsMobileFilterOpen] = useState(false);
  
  // Search Suggestion States
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [isSearching, setIsSearching] = useState(false);

  useEffect(() => {
    const updateURL = () => {
      const params = {};
      if (selectedCategory) params.category = selectedCategory;
      if (searchQuery) params.search = searchQuery;
      if (minPrice) params.min_price = minPrice;
      if (maxPrice) params.max_price = maxPrice;
      if (isAvailable) params.is_available = 'true';
      if (onSale) params.on_sale = 'true';
      if (minRating) params.min_rating = minRating;
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
        if (isAvailable) params.is_available = 'true';
        if (onSale) params.on_sale = 'true';
        if (minRating) params.min_rating = minRating;
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

    const fetchSuggestions = async () => {
      if (searchQuery.length < 2) {
        setSuggestions([]);
        return;
      }
      setIsSearching(true);
      try {
        const res = await fetchProducts({ search: searchQuery, page_size: 5 });
        setSuggestions(res.data.results || res.data);
      } catch (err) {
        console.error("Suggestion error", err);
      } finally {
        setIsSearching(false);
      }
    };

    const timer = setTimeout(() => {
      loadData();
      updateURL();
      if (searchQuery) fetchSuggestions();
    }, 400); // Debounce

    return () => clearTimeout(timer);
  }, [selectedCategory, searchQuery, sortBy, minPrice, maxPrice, isAvailable, onSale, minRating, currentPage, setSearchParams]);

  const filterContentJsx = (
    <>
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

      {/* Advanced Toggles */}
      <div className="p-6 border-b border-slate-100 space-y-4">
        <div className="flex items-center justify-between group cursor-pointer" onClick={() => setIsAvailable(!isAvailable)}>
           <span className="text-xs font-bold text-slate-700 group-hover:text-primary transition-colors">In Stock Only</span>
           <div className={`w-10 h-5 rounded-full transition-all relative ${isAvailable ? 'bg-primary' : 'bg-slate-200'}`}>
              <div className={`absolute top-1 w-3 h-3 bg-white rounded-full transition-all ${isAvailable ? 'right-1' : 'left-1'}`}></div>
           </div>
        </div>
        <div className="flex items-center justify-between group cursor-pointer" onClick={() => setOnSale(!onSale)}>
           <span className="text-xs font-bold text-slate-700 group-hover:text-primary transition-colors">On Sale</span>
           <div className={`w-10 h-5 rounded-full transition-all relative ${onSale ? 'bg-primary' : 'bg-slate-200'}`}>
              <div className={`absolute top-1 w-3 h-3 bg-white rounded-full transition-all ${onSale ? 'right-1' : 'left-1'}`}></div>
           </div>
        </div>
      </div>

      {/* Rating Filter */}
      <div className="p-6 border-b border-slate-100">
        <div className="flex items-center gap-2 mb-6 font-bold text-slate-900 text-sm uppercase tracking-widest">
          <Star size={16} className="text-primary" />
          Minimum Rating
        </div>
        <div className="grid grid-cols-5 gap-2">
           {[4, 3, 2, 1, 0].map((rating) => (
             <button 
               key={rating}
               onClick={() => setMinRating(rating === 0 ? "" : rating.toString())}
               className={`py-2 rounded-xl border text-[10px] font-black flex items-center justify-center gap-1 transition-all ${
                 (minRating === rating.toString() || (rating === 0 && minRating === "")) 
                   ? 'border-primary bg-primary text-white shadow-sm' 
                   : 'border-slate-100 bg-slate-50 text-slate-400 hover:border-slate-200'
               }`}
             >
               {rating === 0 ? 'ANY' : <>{rating}<Star size={10} fill="currentColor" /></>}
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
          {(minPrice || maxPrice || selectedCategory || isAvailable || onSale || minRating) && (
            <button 
              onClick={() => {
                setMinPrice(""); 
                setMaxPrice("");
                setSelectedCategory("");
                setIsAvailable(false);
                setOnSale(false);
                setMinRating("");
                setCurrentPage(1);
              }}
              className="w-full py-2 text-[10px] font-black text-primary hover:bg-primary/5 rounded-lg transition-all uppercase tracking-widest"
            >
              Clear All Filters
            </button>
          )}
        </div>
      </div>
    </>
  );

  return (
    <div className="pt-32 md:pt-40 pb-20 bg-slate-50 min-h-screen">
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
          
          <div className="flex flex-col md:flex-row gap-4 items-center w-full md:w-auto">
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
                  setShowSuggestions(true);
                }}
                onFocus={() => setShowSuggestions(true)}
              />
              <div className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-2">
                <VoiceSearch onSearch={(val) => {
                  setSearchQuery(val);
                  setCurrentPage(1);
                  setShowSuggestions(true);
                }} />
              </div>
              
              {/* Search Suggestions Dropdown */}
              <AnimatePresence>
                {showSuggestions && (searchQuery.length >= 2) && (
                  <motion.div 
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 10 }}
                    className="absolute top-full left-0 right-0 mt-2 bg-white rounded-2xl shadow-2xl border border-slate-100 z-[100] overflow-hidden"
                  >
                    <div className="p-3 border-b border-slate-50 flex justify-between items-center">
                       <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Suggestions</span>
                       <button onClick={() => setShowSuggestions(false)}><X size={14} className="text-slate-300 hover:text-primary" /></button>
                    </div>
                    {isSearching ? (
                      <div className="p-8 text-center"><div className="w-6 h-6 border-2 border-primary border-t-transparent rounded-full animate-spin mx-auto"></div></div>
                    ) : suggestions.length > 0 ? (
                      <div className="py-2">
                        {suggestions.map((item) => (
                          <Link 
                            key={item.id} 
                            to={`/products/${item.id}`}
                            className="flex items-center gap-4 px-4 py-3 hover:bg-slate-50 transition-colors group"
                            onClick={() => setShowSuggestions(false)}
                          >
                             <div className="w-10 h-10 rounded-lg bg-slate-100 overflow-hidden flex-shrink-0">
                                <img src={getImageUrl(item.image)} className="w-full h-full object-cover" alt="" />
                             </div>
                             <div className="flex-grow">
                                <p className="text-xs font-bold text-slate-900 group-hover:text-primary transition-colors">{item.name}</p>
                                <p className="text-[10px] text-slate-400">₹{item.price} • {item.category_name || item.type}</p>
                             </div>
                          </Link>
                        ))}
                        <button 
                          onClick={() => setShowSuggestions(false)}
                          className="w-full py-3 text-center text-[10px] font-black text-primary hover:bg-primary/5 transition-all uppercase tracking-widest border-t border-slate-50"
                        >
                          View All Results
                        </button>
                      </div>
                    ) : (
                      <div className="p-8 text-center text-xs text-slate-400 font-medium">No matches found for "{searchQuery}"</div>
                    )}
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
            
            {/* Mobile Filter Toggle */}
            <button 
              onClick={() => setIsMobileFilterOpen(true)}
              className="lg:hidden w-full md:w-auto flex items-center justify-center gap-2 px-6 py-4 rounded-2xl bg-white border border-slate-200 text-slate-600 font-bold text-sm shadow-sm"
            >
              <Filter size={18} /> Filters
            </button>
          </div>
        </div>

        {/* Mobile Filter Drawer */}
        <AnimatePresence>
           {isMobileFilterOpen && (
             <>
               <motion.div 
                 initial={{ opacity: 0 }}
                 animate={{ opacity: 1 }}
                 exit={{ opacity: 0 }}
                 onClick={() => setIsMobileFilterOpen(false)}
                 className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[150] lg:hidden"
               />
                <motion.div 
                  initial={{ x: '100%' }}
                  animate={{ x: 0 }}
                  exit={{ x: '100%' }}
                  transition={{ type: 'spring', damping: 25, stiffness: 200 }}
                  className="fixed top-0 right-0 bottom-0 w-full sm:max-w-xs md:max-w-sm bg-white z-[160] lg:hidden shadow-2xl flex flex-col"
                >
                  <div className="p-6 border-b border-slate-100 flex items-center justify-between">
                     <h3 className="text-xl font-bold text-slate-900">Filters</h3>
                     <button onClick={() => setIsMobileFilterOpen(false)} className="w-10 h-10 rounded-xl bg-slate-50 flex items-center justify-center text-slate-400"><X size={20} /></button>
                  </div>
                  <div className="flex-grow overflow-y-auto">
                     {filterContentJsx}
                  </div>
                  <div className="p-6 border-t border-slate-100">
                     <button onClick={() => setIsMobileFilterOpen(false)} className="btn-primary w-full py-4 text-sm uppercase tracking-widest font-black">Show Results</button>
                  </div>
               </motion.div>
             </>
           )}
        </AnimatePresence>

        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar Filters (Desktop) */}
          <aside className="hidden lg:block w-72 space-y-6">
            <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden lg:sticky lg:top-32">
               {filterContentJsx}
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
                    <option value="-popularity_score">Popularity</option>
                    <option value="-average_rating">Top Rated</option>
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
                    <Link 
                      key={product.id}
                      to={`/products/${product.id}`}
                      className="group"
                    >
                      <motion.div 
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: idx * 0.03 }}
                        className={`bg-white rounded-3xl border border-slate-100 hover:border-primary/20 transition-all duration-300 overflow-hidden shadow-sm hover:shadow-xl ${viewMode === 'list' ? 'flex flex-col md:flex-row' : ''}`}
                      >
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
                             <div className="bg-white text-slate-900 font-bold px-6 py-2.5 rounded-xl text-sm transform translate-y-4 group-hover:translate-y-0 transition-all duration-300">
                               Details
                             </div>
                          </div>
                        </div>

                        <div className={`p-6 flex flex-col flex-grow ${viewMode === 'list' ? 'justify-center' : ''}`}>
                          <div className="flex justify-between items-start mb-2">
                            <p className="text-primary text-[9px] font-black uppercase tracking-widest">{product.category_name}</p>
                            <span className="text-[10px] font-bold text-slate-400">ID: #{product.id}</span>
                          </div>
                          <h3 className="text-lg font-bold text-slate-900 mb-2 group-hover:text-primary transition-colors line-clamp-1">{product.name}</h3>
                          <p className="text-slate-500 text-xs mb-6 line-clamp-2 leading-relaxed font-light">{product.description}</p>
                          
                          <div className="mt-auto flex justify-between items-end pt-4 border-t border-slate-50">
                            <div className="space-y-1">
                              <div className="flex items-center gap-1.5 mb-1">
                                <div className="flex text-accent">
                                   {[...Array(5)].map((_, i) => (
                                     <Star key={i} size={10} fill={i < Math.floor(product.average_rating) ? "currentColor" : "none"} className={i < Math.floor(product.average_rating) ? "text-accent" : "text-slate-200"} />
                                   ))}
                                </div>
                                <span className="text-[9px] font-black text-slate-400">({product.review_count})</span>
                              </div>
                              <div className="flex items-center gap-2">
                                <p className="text-xl font-bold text-slate-900 tracking-tight">₹{product.discount_price || product.price}</p>
                                {product.discount_price && (
                                  <p className="text-xs text-slate-400 line-through">₹{product.price}</p>
                                )}
                              </div>
                            </div>
                            <div 
                              className="w-10 h-10 rounded-xl bg-slate-50 text-slate-400 flex items-center justify-center group-hover:bg-primary group-hover:text-white transition-all mb-1"
                            >
                               <ChevronRight size={18} />
                            </div>
                          </div>
                        </div>
                      </motion.div>
                    </Link>
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

