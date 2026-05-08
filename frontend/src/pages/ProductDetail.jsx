import { useState, useEffect, useMemo, useRef } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { ShieldCheck, Truck, ArrowLeft, MessageSquare, Wand2, Star, ChevronRight, CheckCircle2, Share2, Heart, Package, Phone, MapPin, AlertCircle } from 'lucide-react';
import { fetchProductById, getImageUrl } from '../api';
import api from '../api';
import CanvasCustomizer from '../components/CanvasCustomizer';
import CustomizerControls from '../components/CustomizerControls';
import { useCart } from '../context/CartContext';
import { motion, AnimatePresence, animate } from 'framer-motion';

// Animated Price Component for the "Rolling" effect
const AnimatedPrice = ({ value, prefix = "₹" }) => {
  const [displayValue, setDisplayValue] = useState(value);
  const prevValue = useRef(value);

  useEffect(() => {
    const controls = animate(prevValue.current, value, {
      duration: 0.8,
      ease: "easeOut",
      onUpdate: (latest) => setDisplayValue(latest)
    });
    prevValue.current = value;
    return () => controls.stop();
  }, [value]);

  return (
    <span>
      {prefix}{Math.round(displayValue).toLocaleString()}
    </span>
  );
};

const ProductDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { addToCart } = useCart();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  
  // Customization State
  const [textEntries, setTextEntries] = useState(() => [{ id: Date.now(), text: '' }]);
  const [textColor, setTextColor] = useState('#000000');
  const [logoFiles, setLogoFiles] = useState([]);
  const [logoPreviews, setLogoPreviews] = useState([]); // Array of preview URLs
  const [mockupImage, setMockupImage] = useState(null);
  const [isCustomizing, setIsCustomizing] = useState(false);
  const [relatedProducts, setRelatedProducts] = useState([]);
  const [warningMessage, setWarningMessage] = useState('');
  const [quantity, setQuantity] = useState(1);
  const [pincode, setPincode] = useState("");
  const [pincodeStatus, setPincodeStatus] = useState(null); // 'checking', 'success', 'error', null
  const [isServiceable, setIsServiceable] = useState(false);
  
  const handlePincodeCheck = async () => {
    if (pincode.length !== 6) {
      setPincodeStatus('error');
      return;
    }
    setPincodeStatus('checking');
    try {
      const res = await api.get(`orders/check-pincode/?pincode=${pincode}`);
      const serviceable = res.data.is_serviceable;
      setIsServiceable(serviceable);
      setPincodeStatus(serviceable ? 'success' : 'not_serviceable');
    } catch (err) {
      console.error("Error checking pincode", err);
      setPincodeStatus('error');
    }
  };
  const [showBulkDetails, setShowBulkDetails] = useState(false);
  
  // UX Flow States
  const [activeStep, setActiveStep] = useState(1); // 1: Branding, 2: Design, 3: Review

  // New States for Placement and Instructions
  const [placement, setPlacement] = useState('Front');
  const [designInstructions, setDesignInstructions] = useState('');

  useEffect(() => {
    const loadProduct = async () => {
      setLoading(true);
      try {
        const res = await fetchProductById(id);
        const productData = res.data;
        console.log('📦 Product loaded:', productData.name, '(ID:', productData.id, ')');
        console.log('🎨 Customization zones:', productData.customization_zones.length, 'zones found');
        setProduct(productData);
        
        if (productData.customization_zones && productData.customization_zones.length > 0) {
           console.log('✅ Customization available for this product');
           
           // Initialize with one empty text entry
           setTextEntries([{ id: Date.now(), text: '' }]);
           setLogoFiles([]);
           setLogoPreviews([]);
        } else {
           console.warn('⚠️ No customization zones found for this product');
           console.log('💡 Run: cd backend && python sync_customization.py to load zones from JSON');
        }

        const relatedRes = await api.get('/products/', { 
          params: { category: productData.category } 
        });
        const relatedData = relatedRes.data.results || relatedRes.data;
        setRelatedProducts(relatedData.filter(p => p.id !== parseInt(id)).slice(0, 4));
        
      } catch (error) {
        console.error("Error loading product:", error);
      } finally {
        setLoading(false);
      }
    };
    loadProduct();
    window.scrollTo(0, 0);
  }, [id]);

  const customizationConfig = useMemo(() => {
    if (!product?.customization_zones?.length) return null;
    return {
      baseImage: product.image,
      zones: product.customization_zones
    };
  }, [product]);

  const bulkPricing = useMemo(() => {
    if (!product) return { unitPrice: 0, total: 0, savings: 0, discount: 0 };
    const basePrice = product.price;
    let discount = 0;
    if (quantity >= 500) discount = 0.15;
    else if (quantity >= 250) discount = 0.10;
    else if (quantity >= 100) discount = 0.05;
    
    const unitPrice = basePrice * (1 - discount);
    const total = unitPrice * quantity;
    const savings = (basePrice * quantity) - total;
    
    return { unitPrice, total, savings, discount: Math.round(discount * 100) };
  }, [product, quantity]);

  const [showToast, setShowToast] = useState(false);

  const handleAddToCart = async () => {
    let imageFile = null;
    if (mockupImage) {
      try {
        const response = await fetch(mockupImage);
        if (!response.ok) throw new Error('Failed to fetch mockup');
        const blob = await response.blob();
        imageFile = new File([blob], `custom-${product.name}.png`, { type: 'image/png' });
      } catch (err) {
        console.error('Failed to create custom image:', err);
      }
    }
    
    const customizationData = {
      texts: textEntries,
      color: textColor,
      placement: placement,
      instructions: designInstructions,
      timestamp: new Date().toISOString()
    };

    addToCart(product.id, quantity, textEntries[0]?.text || '', imageFile, customizationData, logoFiles);
    
    // Show Premium Toast
    setShowToast(true);
    setTimeout(() => setShowToast(false), 3000);
  };

  if (loading) {
    return (
      <div className="pt-40 pb-40 text-center bg-slate-50 min-h-screen flex flex-col items-center justify-center">
        <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mb-6"></div>
        <h2 className="text-2xl font-bold text-slate-900 animate-pulse">Preparing Your Premium Gift...</h2>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="pt-40 pb-40 text-center bg-slate-50 min-h-screen flex flex-col items-center justify-center">
        <Package className="mx-auto text-slate-300 mb-6" size={64} />
        <h2 className="text-3xl font-bold text-slate-900 mb-4">Gift Not Found</h2>
        <Link to="/products" className="btn-primary">Back to Catalog</Link>
      </div>
    );
  }

  return (
    <>
      <div className="pt-32 pb-32 bg-slate-50 min-h-screen">
        <div className="container-custom">
          {/* Breadcrumbs */}
          <nav className="flex items-center gap-3 text-xs font-bold uppercase tracking-widest text-slate-400 mb-10 overflow-x-auto whitespace-nowrap scrollbar-hide">
            <Link to="/" className="hover:text-primary transition-colors">Home</Link>
            <ChevronRight size={12} />
            <Link to="/products" className="hover:text-primary transition-colors">Catalog</Link>
            <ChevronRight size={12} />
            <Link to={`/products?category=${product.category}`} className="hover:text-primary transition-colors">{product.category_name}</Link>
            <ChevronRight size={12} />
            <span className="text-slate-900 truncate">{product.name}</span>
          </nav>

          <div className="grid lg:grid-cols-2 gap-16 items-start">
            {/* Visual Area */}
            <div className="sticky top-32">
               <motion.div 
                 layout
                 className="glass-card overflow-hidden relative border-slate-200/50 bg-white min-h-[450px] md:min-h-[600px] flex items-center justify-center"
               >
                  {isCustomizing && customizationConfig ? (
                    <CanvasCustomizer 
                      productConfig={customizationConfig} 
                      textEntries={textEntries}
                      textColor={textColor}
                      logoPreviews={logoPreviews}
                      onImageExport={setMockupImage} 
                      onWarning={setWarningMessage}
                    />
                  ) : (
                    <motion.img 
                      key="static-image"
                      initial={{ opacity: 0, scale: 0.95 }}
                      animate={{ opacity: 1, scale: 1 }}
                      src={getImageUrl(product.image) || "https://images.unsplash.com/photo-1549465220-1a8b9238cd48?auto=format&fit=crop&q=80&w=1000"} 
                      className="w-full h-full max-h-[600px] object-contain p-8 transition-transform duration-700 hover:scale-105"
                      alt={product.name}
                    />
                  )}

                  {/* Status Badges */}
                  <div className="absolute top-8 left-8 flex flex-col gap-3">
                     {product.is_bulk_only && (
                       <span className="bg-slate-900 text-white text-[10px] font-black px-4 py-2 rounded-full uppercase tracking-[0.2em] shadow-xl">Bulk Exclusive</span>
                     )}
                     {customizationConfig && (
                       <span className="bg-primary/10 backdrop-blur-md text-primary text-[10px] font-black px-4 py-2 rounded-full uppercase tracking-[0.2em] border border-primary/20 shadow-sm">Customizable</span>
                     )}
                  </div>

                  {/* Floating Actions */}
                  <div className="absolute top-8 right-8 flex flex-col gap-3">
                     <button className="w-12 h-12 rounded-2xl bg-white border border-slate-100 flex items-center justify-center text-slate-400 hover:text-primary hover:border-primary/20 transition-all shadow-sm">
                        <Heart size={20} />
                     </button>
                     <button className="w-12 h-12 rounded-2xl bg-white border border-slate-100 flex items-center justify-center text-slate-400 hover:text-primary hover:border-primary/20 transition-all shadow-sm">
                        <Share2 size={20} />
                     </button>
                  </div>
                  
                  {customizationConfig && !isCustomizing && (
                    <motion.button 
                      initial={{ y: 20, opacity: 0 }}
                      animate={{ y: 0, opacity: 1 }}
                      onClick={() => setIsCustomizing(true)}
                      className="absolute bottom-8 right-8 btn-primary px-8 py-4 text-sm z-20 shadow-2xl"
                    >
                      <Wand2 size={18} /> Visualize Your Logo
                    </motion.button>
                  )}
               </motion.div>
            </div>

            {/* Details Section */}
            <div className="flex flex-col">
              <AnimatePresence mode="wait">
                {isCustomizing && customizationConfig ? (
                  <motion.div 
                    key="custom-controls"
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    className="space-y-8"
                  >
                    <div>
                      <div className="flex justify-between items-center mb-6">
                        <div className="flex gap-2">
                           {[1, 2, 3].map((step) => (
                             <div 
                               key={step}
                               className={`w-8 h-8 rounded-full flex items-center justify-center text-[10px] font-black transition-all ${
                                 activeStep === step 
                                   ? 'bg-primary text-white shadow-lg shadow-primary/20 scale-110' 
                                   : activeStep > step 
                                     ? 'bg-green-500 text-white' 
                                     : 'bg-slate-100 text-slate-400'
                               }`}
                             >
                               {activeStep > step ? '✓' : step}
                             </div>
                           ))}
                        </div>
                        <button 
                          onClick={() => setIsCustomizing(false)}
                          className="text-slate-400 hover:text-red-500 font-bold text-xs uppercase tracking-widest flex items-center gap-2"
                        >
                          <ArrowLeft size={14} /> Back
                        </button>
                      </div>
                      <h2 className="text-3xl font-bold text-slate-900 tracking-tight">
                        {activeStep === 1 ? 'Branding Assets' : activeStep === 2 ? 'Personalize Design' : 'Review & Confirm'}
                      </h2>
                      <p className="text-slate-500 mt-1 text-sm font-light">
                        {activeStep === 1 ? 'Upload your corporate logo and brand colors.' : activeStep === 2 ? 'Customize your text entries and placement.' : 'Finalize your design and add instructions.'}
                      </p>
                    </div>
                    
                    <div className="bg-white p-6 rounded-[2rem] border border-slate-200/50 shadow-premium">
                      <CustomizerControls 
                        activeStep={activeStep}
                        setActiveStep={setActiveStep}
                        textEntries={textEntries}
                        setTextEntries={setTextEntries}
                        textColor={textColor}
                        setTextColor={setTextColor}
                        logoFiles={logoFiles}
                        setLogoFiles={setLogoFiles}
                        setLogoPreviews={setLogoPreviews}
                        placement={placement}
                        setPlacement={setPlacement}
                        designInstructions={designInstructions}
                        setDesignInstructions={setDesignInstructions}
                        maxZones={customizationConfig.zones.length}
                        onReset={() => {
                          setTextEntries([{ id: Date.now(), text: '' }]);
                          setTextColor('#000000');
                          setLogoFiles([]);
                          setLogoPreviews([]);
                          setPlacement('Front');
                          setDesignInstructions('');
                          setWarningMessage('');
                        }}
                        warningMessage={warningMessage}
                      />
                    </div>

                     {activeStep === 3 && (
                      <motion.div 
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="space-y-4 pt-4"
                      >
                        <button 
                          id="add-to-cart-btn"
                          onClick={handleAddToCart}
                          className="btn-primary w-full py-5 text-xl shadow-2xl shadow-primary/30"
                        >
                          Save & Add to Cart
                        </button>
                        <p className="text-center text-slate-400 text-xs font-medium flex items-center justify-center gap-2">
                          <ShieldCheck size={14} /> Your customization details will be verified by our designers.
                        </p>
                      </motion.div>
                     )}
                  </motion.div>
                ) : (
                  <motion.div 
                    key="product-details"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: 20 }}
                    className="space-y-10"
                  >
                    {/* Basic Info */}
                    <div>
                      <div className="flex items-center gap-3 mb-6">
                        <span className="text-primary font-black uppercase tracking-[0.3em] text-xs">{product.category_name}</span>
                        <div className="flex gap-1 text-accent">
                          {[1,2,3,4,5].map(n => <Star key={n} size={14} fill="currentColor" />)}
                        </div>
                        <span className="text-slate-400 text-xs font-bold">(48 Reviews)</span>
                      </div>
                      <h1 className="text-4xl md:text-6xl font-bold text-slate-900 mb-6 leading-tight tracking-tight">{product.name}</h1>
                      
                      {/* Pricing */}
                      <div className="flex flex-col gap-2 mb-8">
                        <div className="flex items-end gap-4">
                          <span className="text-5xl font-bold text-slate-900 tracking-tighter">
                            <AnimatedPrice value={bulkPricing.unitPrice} />
                          </span>
                          {bulkPricing.discount > 0 && (
                            <div className="mb-2">
                               <span className="text-slate-400 line-through font-medium mr-2">₹{product.price}</span>
                               <span className="text-green-600 font-bold text-sm bg-green-50 px-2 py-1 rounded-lg">-{bulkPricing.discount}% Bulk Discount</span>
                            </div>
                          )}
                        </div>
                        {quantity > 1 && (
                          <div className="flex items-center gap-2">
                            <span className="text-slate-500 text-sm font-medium">
                              Subtotal: <span className="text-slate-900 font-bold"><AnimatedPrice value={bulkPricing.total} /></span>
                            </span>
                            {bulkPricing.savings > 0 && (
                              <span className="text-[10px] font-black text-green-600 uppercase tracking-widest bg-green-50 px-2 py-0.5 rounded-md border border-green-100 animate-pulse">
                                Saving <AnimatedPrice value={bulkPricing.savings} />
                              </span>
                            )}
                          </div>
                        )}
                      </div>

                      <p className="text-lg text-slate-500 leading-relaxed font-light">
                        {product.description}
                      </p>

                      {/* Quantity Selector & Bulk Info */}
                      <div className="pt-4 space-y-4">
                        <div className="flex flex-col gap-3">
                           <div className="flex items-center justify-between">
                              <label className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] flex items-center gap-2">
                                Select Quantity
                                <div className="relative">
                                   <button 
                                     onClick={() => setShowBulkDetails(!showBulkDetails)}
                                     className={`w-4 h-4 rounded-full flex items-center justify-center transition-all ${
                                       showBulkDetails ? 'bg-primary text-white shadow-lg' : 'bg-slate-100 text-slate-400 hover:bg-slate-200'
                                     }`}
                                   >
                                      <span className="text-[10px] font-black italic">i</span>
                                   </button>
                                   
                                   {/* Popover */}
                                   <AnimatePresence>
                                     {showBulkDetails && (
                                       <motion.div 
                                         initial={{ opacity: 0, y: -10, scale: 0.95 }}
                                         animate={{ opacity: 1, y: 0, scale: 1 }}
                                         exit={{ opacity: 0, y: -10, scale: 0.95 }}
                                         className="absolute top-full left-0 mt-3 w-64 p-5 bg-slate-900 text-white rounded-[2rem] shadow-3xl z-50 origin-top-left"
                                       >
                                          <div className="flex items-center justify-between mb-4 border-b border-white/10 pb-3">
                                            <h4 className="text-[10px] font-black uppercase tracking-widest">Bulk Pricing Tiers</h4>
                                            <button onClick={() => setShowBulkDetails(false)} className="text-white/40 hover:text-white">✕</button>
                                          </div>
                                          <div className="space-y-3">
                                             {[
                                               { range: '1-99 Units', disc: 'Base Price', active: quantity < 100 },
                                               { range: '100+ Units', disc: '5% Discount', active: quantity >= 100 && quantity < 250 },
                                               { range: '250+ Units', disc: '10% Discount', active: quantity >= 250 && quantity < 500 },
                                               { range: '500+ Units', disc: '15% Discount', active: quantity >= 500 },
                                             ].map((tier, i) => (
                                               <div key={i} className={`flex justify-between items-center p-2 rounded-xl transition-colors ${tier.active ? 'bg-primary/20 border border-primary/30' : 'bg-white/5'}`}>
                                                  <span className={`text-[10px] font-bold ${tier.active ? 'text-white' : 'text-slate-400'}`}>{tier.range}</span>
                                                  <span className={`text-[10px] font-black ${tier.active ? 'text-primary' : 'text-white'}`}>{tier.disc}</span>
                                               </div>
                                             ))}
                                          </div>
                                          <div className="absolute bottom-full left-2 border-8 border-transparent border-b-slate-900"></div>
                                       </motion.div>
                                     )}
                                   </AnimatePresence>
                                </div>
                              </label>
                              <button 
                                onClick={() => setShowBulkDetails(!showBulkDetails)}
                                className="text-[10px] font-black text-primary uppercase tracking-widest hover:underline"
                              >
                                {showBulkDetails ? 'Hide Details' : 'View Bulk Tiers'}
                              </button>
                           </div>
                           
                           <div className="flex items-center gap-6">
                              <div className="flex items-center p-1 bg-white border border-slate-200 rounded-2xl shadow-sm">
                                 <button 
                                   onClick={() => setQuantity(prev => Math.max(1, prev - 1))}
                                   className="w-12 h-12 flex items-center justify-center text-slate-400 hover:text-primary hover:bg-slate-50 rounded-xl transition-all"
                                 >
                                   <span className="text-2xl font-light">−</span>
                                 </button>
                                 <input 
                                   type="number" 
                                   value={quantity}
                                   onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value) || 1))}
                                   className="w-20 text-center font-bold text-xl text-slate-900 bg-transparent outline-none [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                                 />
                                 <button 
                                   onClick={() => setQuantity(prev => prev + 1)}
                                   className="w-12 h-12 flex items-center justify-center text-slate-400 hover:text-primary hover:bg-slate-50 rounded-xl transition-all"
                                 >
                                   <span className="text-2xl font-light">+</span>
                                 </button>
                              </div>
                              <div className="flex flex-col">
                                <div className="flex items-center gap-2">
                                  <span className="text-[10px] font-black text-slate-900 uppercase tracking-widest">Instant Ordering</span>
                                  {quantity >= 100 && (
                                    <span className="text-[8px] font-black bg-green-500 text-white px-1.5 py-0.5 rounded uppercase">Level {quantity >= 500 ? 3 : quantity >= 250 ? 2 : 1} Savings</span>
                                  )}
                                </div>
                                <span className="text-xs text-slate-400">Up to 1,000 units</span>
                              </div>
                           </div>
                        </div>
                      </div>
                    </div>

                    {/* Highlights Grid */}
                    <div className="grid grid-cols-2 gap-4">
                       <div className="bg-white p-6 rounded-3xl border border-slate-100 flex items-center gap-4">
                          <div className="w-12 h-12 rounded-2xl bg-slate-50 flex items-center justify-center text-primary shadow-sm">
                             <Truck size={24} />
                          </div>
                          <div>
                             <p className="text-[10px] text-slate-400 font-black uppercase tracking-widest">Delivery</p>
                             <p className="text-sm font-bold text-slate-900">7-10 Days</p>
                          </div>
                       </div>
                       <div className="bg-white p-6 rounded-3xl border border-slate-100 flex items-center gap-4">
                          <div className="w-12 h-12 rounded-2xl bg-slate-50 flex items-center justify-center text-primary shadow-sm">
                             <ShieldCheck size={24} />
                          </div>
                          <div>
                             <p className="text-[10px] text-slate-400 font-black uppercase tracking-widest">Warranty</p>
                             <p className="text-sm font-bold text-slate-900">12 Months</p>
                          </div>
                       </div>
                    </div>

                    {/* Pincode Checker */}
                    <div className="bg-slate-50 p-6 rounded-3xl border border-slate-100">
                      <div className="flex items-center gap-2 mb-4">
                        <MapPin size={16} className="text-primary" />
                        <span className="text-[10px] font-black text-slate-900 uppercase tracking-widest">Check Delivery Availability</span>
                      </div>
                      <div className="flex gap-3">
                        <div className="flex-grow relative">
                          <input 
                            type="text" 
                            maxLength={6}
                            placeholder="Enter 6-digit Pincode"
                            className="w-full px-5 py-3 rounded-xl bg-white border border-slate-200 focus:outline-none focus:border-primary text-sm font-bold placeholder:font-normal"
                            value={pincode}
                            onChange={(e) => setPincode(e.target.value.replace(/\D/g, ''))}
                          />
                        </div>
                        <button 
                          onClick={handlePincodeCheck}
                          disabled={pincodeStatus === 'checking'}
                          className="bg-slate-900 text-white px-6 py-3 rounded-xl text-xs font-bold hover:bg-primary transition-all disabled:bg-slate-400"
                        >
                          {pincodeStatus === 'checking' ? 'Checking...' : 'Check'}
                        </button>
                      </div>
                      
                      <AnimatePresence mode="wait">
                        {pincodeStatus === 'success' && (
                          <motion.div 
                            initial={{ opacity: 0, y: -10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="flex items-center gap-2 mt-4 text-green-600 font-bold text-xs"
                          >
                            <CheckCircle2 size={14} /> Delivery available in your area
                          </motion.div>
                        )}
                        {pincodeStatus === 'not_serviceable' && (
                          <motion.div 
                            initial={{ opacity: 0, y: -10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="flex items-center gap-2 mt-4 text-red-500 font-bold text-xs"
                          >
                            <AlertCircle size={14} /> Sorry, we do not deliver to this area currently.
                          </motion.div>
                        )}
                        {pincodeStatus === 'error' && (
                          <motion.div 
                            initial={{ opacity: 0, y: -10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="flex items-center gap-2 mt-4 text-orange-500 font-bold text-xs"
                          >
                            <AlertCircle size={14} /> Please enter a valid 6-digit pincode.
                          </motion.div>
                        )}
                      </AnimatePresence>
                    </div>

                    {/* Stock & Urgency */}
                    <div className="p-6 rounded-[2rem] bg-slate-900 text-white relative overflow-hidden">
                       <div className="relative z-10 flex items-center justify-between">
                          <div>
                             <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Availability</p>
                             <p className={`text-lg font-bold flex items-center gap-2 ${product.stock > 0 ? 'text-white' : 'text-red-400'}`}>
                                {product.stock > 0 ? (
                                  <> <CheckCircle2 size={18} className="text-green-400" /> In Stock & Ready to Ship</>
                                ) : 'Currently Out of Stock'}
                             </p>
                          </div>
                          <div className="text-right">
                             <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Ships From</p>
                             <p className="text-lg font-bold text-white">Mumbai, IN</p>
                          </div>
                       </div>
                       <div className="absolute top-0 right-0 w-32 h-32 bg-primary/20 rounded-full blur-3xl"></div>
                    </div>

                    {/* Actions */}
                    <div className="flex flex-col sm:flex-row gap-5 pt-6">
                      <button 
                        onClick={handleAddToCart}
                        disabled={product.stock <= 0}
                        className="btn-primary flex-grow py-6 text-xl shadow-2xl shadow-primary/30"
                      >
                        Add to Collection
                      </button>
                      <a 
                        href={`https://wa.me/918169975287?text=Hi, I am interested in ${product.name} (Quantity: ${quantity})`}
                        target="_blank"
                        rel="noreferrer"
                        className="btn-outline border-slate-200 text-slate-900 hover:bg-slate-900 hover:text-white flex items-center justify-center px-10 py-6"
                      >
                        <Phone size={24} />
                      </a>
                    </div>

                    {/* Features List */}
                    <div className="pt-10 border-t border-slate-200">
                       <h4 className="text-lg font-bold text-slate-900 mb-6">Why Choose This Gift?</h4>
                       <div className="grid sm:grid-cols-2 gap-x-8 gap-y-4">
                          {[
                            'Premium Quality Materials',
                            'Eco-friendly Packaging',
                            'Corporate Branding Ready',
                            'Individually Quality Checked',
                            'Doorstep Delivery Pan-India',
                            'Dedicated Account Support'
                          ].map((feat, idx) => (
                            <div key={idx} className="flex items-center gap-3 text-sm text-slate-600 font-medium">
                               <div className="w-5 h-5 rounded-full bg-green-500/10 flex items-center justify-center text-green-500">
                                  <CheckCircle2 size={12} />
                               </div>
                               {feat}
                            </div>
                          ))}
                       </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>

          {/* Related Products */}
          {relatedProducts.length > 0 && (
            <div className="mt-40">
               <div className="flex justify-between items-end mb-16">
                  <div>
                     <span className="text-primary font-black uppercase tracking-[0.3em] text-xs mb-4 inline-block">Curated Suggestions</span>
                     <h2 className="text-4xl font-bold text-slate-900 tracking-tight">You May Also <span className="text-primary italic">Like</span></h2>
                  </div>
                  <Link to="/products" className="btn-secondary py-3 px-6 text-sm">View Full Catalog</Link>
               </div>
               <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-10">
                  {relatedProducts.map((rel) => (
                    <Link 
                      key={rel.id} 
                      to={`/products/${rel.id}`}
                      className="group"
                    >
                      <div className="bg-white rounded-[2rem] overflow-hidden shadow-premium hover-lift transition-all duration-500 border border-slate-100">
                         <div className="aspect-square bg-slate-50 overflow-hidden">
                            <img src={getImageUrl(rel.image)} alt={rel.name} className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" />
                         </div>
                         <div className="p-8">
                            <h4 className="font-bold text-slate-900 mb-2 group-hover:text-primary transition-colors truncate">{rel.name}</h4>
                            <p className="text-xl font-bold text-slate-900">₹{rel.price}</p>
                         </div>
                      </div>
                    </Link>
                  ))}
               </div>
            </div>
          )}
        </div>
      </div>
      {/* Premium Success Toast */}
      <AnimatePresence>
        {showToast && (
          <motion.div
            initial={{ opacity: 0, y: -50, x: 50, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, x: 0, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9, transition: { duration: 0.2 } }}
            className="fixed top-24 right-8 z-[100] flex items-center gap-4 bg-white/90 backdrop-blur-xl border border-primary/20 p-5 rounded-[2rem] shadow-[0_20px_50px_-12px_rgba(217,22,86,0.2)]"
          >
            <div className="w-12 h-12 bg-primary text-white rounded-2xl flex items-center justify-center shadow-lg shadow-primary/20">
              <CheckCircle2 size={24} />
            </div>
            <div className="pr-4">
              <h3 className="text-sm font-black text-slate-900 uppercase tracking-widest">Added to Cart</h3>
              <p className="text-[10px] text-slate-500 font-medium">Your customized {product.name} is ready.</p>
            </div>
            <button 
              onClick={() => navigate('/cart')}
              className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-600 rounded-xl text-[9px] font-black uppercase tracking-widest transition-all"
            >
              View Cart
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

export default ProductDetail;
