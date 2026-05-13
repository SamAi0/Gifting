import { useState, useEffect, useMemo, useRef, useCallback } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { ShieldCheck, Truck, ArrowLeft, Wand2, Star, ChevronRight, CheckCircle2, Share2, Heart, Package, Phone, MapPin, AlertCircle } from 'lucide-react';
import { fetchProductById, getImageUrl, fetchReviews, submitReview, updateReview, addToWishlist, removeFromWishlist, fetchWishlist } from '../api';
import api from '../api';
import CanvasCustomizer from '../components/CanvasCustomizer';
import CustomizerControls from '../components/CustomizerControls';
import StarRating from '../components/StarRating';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
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
  const { user } = useAuth();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  
  // Review States
  const [reviews, setReviews] = useState([]);
  const [reviewsLoading, setReviewsLoading] = useState(true);
  const [showReviewForm, setShowReviewForm] = useState(false);
  const [newReview, setNewReview] = useState({ rating: 5, comment: '', image: null });
  const [submittingReview, setSubmittingReview] = useState(false);
  const [userReview, setUserReview] = useState(null);
  const [isEditingReview, setIsEditingReview] = useState(false);
  const [hasAlreadyReviewed, setHasAlreadyReviewed] = useState(false);
  
  // Wishlist States
  const [isInWishlist, setIsInWishlist] = useState(false);
  const [wishlistItemId, setWishlistItemId] = useState(null);
  
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
  const [selectedVariant, setSelectedVariant] = useState(null);
  
  const handlePincodeCheck = async () => {
    if (pincode.length !== 6) {
      setPincodeStatus('error');
      return;
    }
    setPincodeStatus('checking');
    try {
      const res = await api.get(`orders/check-pincode/?pincode=${pincode}`);
      const serviceable = res.data.is_serviceable;
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

  const loadReviews = useCallback(async () => {
    setReviewsLoading(true);
    setUserReview(null);
    setIsEditingReview(false);
    try {
      const res = await fetchReviews({ product: id });
      const reviewsData = res.data.results || res.data;
      setReviews(reviewsData);
      
      if (user) {
        const existingReview = reviewsData.find(r => r.user_name === user.username);
        if (existingReview) {
          setHasAlreadyReviewed(true);
          // Check if within 4 minute editing window
          const createdAt = new Date(existingReview.created_at);
          const now = new Date();
          const diffInMinutes = (now - createdAt) / (1000 * 60);
          
          if (diffInMinutes <= 4) {
            setUserReview(existingReview);
            setNewReview({ rating: existingReview.rating, comment: existingReview.comment, image: null });
          } else {
            // Review exists but window expired
            setUserReview(null); 
          }
        } else {
          setHasAlreadyReviewed(false);
        }
      }
    } catch (err) {
      console.error("Error fetching reviews", err);
    } finally {
      setReviewsLoading(false);
    }
  }, [id, user]);

  const checkWishlist = useCallback(async () => {
    try {
      const res = await fetchWishlist();
      const item = res.data.find(w => w.product === parseInt(id));
      if (item) {
        setIsInWishlist(true);
        setWishlistItemId(item.id);
      } else {
        setIsInWishlist(false);
      }
    } catch (err) {
      console.error("Wishlist check error", err);
    }
  }, [id]);

  const loadProduct = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetchProductById(id);
      const productData = res.data;
      setProduct(productData);
      
      if (productData.variants && productData.variants.length > 0) {
        setSelectedVariant(productData.variants[0]);
      }

      // Fetch Related Products (with fallback to trending if category is empty)
      let relatedRes = await api.get('/products/', { 
        params: { category: productData.category } 
      });
      let relatedData = relatedRes.data.results || relatedRes.data;
      
      // If no related products in same category, fetch trending products
      if (relatedData.length <= 1) {
        relatedRes = await api.get('/products/', { params: { is_trending: 'true' } });
        relatedData = relatedRes.data.results || relatedRes.data;
      }
      
      setRelatedProducts(relatedData.filter(p => p.id !== parseInt(id)).slice(0, 4));
      
      // Fetch Reviews
      loadReviews();
      
      // Check Wishlist
      if (user) {
        checkWishlist();
      }
      
    } catch (error) {
      console.error("Error loading product:", error);
    } finally {
      setLoading(false);
    }
  }, [id, user, loadReviews, checkWishlist]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    loadProduct();
    window.scrollTo(0, 0);

    // Check for setup mode in URL
    const params = new URLSearchParams(window.location.search);
    if (params.get('setup') === 'true') {
      setIsCustomizing(true);
      // Populate textEntries to match max possible zones (usually 7) to show all placeholders
      setTextEntries(Array.from({ length: 7 }, (_, i) => ({ id: Date.now() + i, text: '' })));
    }
  }, [loadProduct]);

  const handleToggleWishlist = async () => {
    if (!user) {
      navigate('/login?redirect=' + window.location.pathname);
      return;
    }
    
    try {
      if (isInWishlist) {
        await removeFromWishlist(wishlistItemId);
        setIsInWishlist(false);
        setWishlistItemId(null);
      } else {
        const res = await addToWishlist(product.id);
        setIsInWishlist(true);
        setWishlistItemId(res.data.id);
      }
    } catch (err) {
      console.error("Wishlist toggle error", err);
    }
  };

  const handleReviewSubmit = async (e) => {
    e.preventDefault();
    if (!user) {
      navigate('/login?redirect=' + window.location.pathname);
      return;
    }
    
    if (!newReview.comment.trim()) {
      alert("Please enter a comment for your review.");
      setSubmittingReview(false);
      return;
    }

    const formData = new FormData();
    formData.append('product', id);
    formData.append('rating', newReview.rating);
    formData.append('comment', newReview.comment);
    if (newReview.image) formData.append('image', newReview.image);
    
    try {
      if (isEditingReview && userReview) {
        await updateReview(userReview.id, formData);
        setToastMessage("Review updated successfully!");
      } else {
        await submitReview(formData);
        setToastMessage("Review posted successfully!");
      }
      
      setNewReview({ rating: 5, comment: '', image: null });
      setShowReviewForm(false);
      setIsEditingReview(false);
      setShowToast(true);
      setTimeout(() => setShowToast(false), 3000);
      
      // Reload reviews and product
      loadReviews();
      const prodRes = await fetchProductById(id);
      setProduct(prodRes.data);
    } catch (err) {
      console.error("Review submit error", err);
      // Handle Django Rest Framework validation errors (400)
      const errorData = err.response?.data;
      let errorMessage = "Failed to submit review.";
      
      if (errorData) {
        if (typeof errorData === 'string') errorMessage = errorData;
        else if (errorData.detail) errorMessage = errorData.detail;
        else if (errorData.non_field_errors) errorMessage = errorData.non_field_errors[0];
        else {
          // Join all field errors
          errorMessage = Object.entries(errorData)
            .map(([field, msgs]) => `${field}: ${Array.isArray(msgs) ? msgs.join(', ') : msgs}`)
            .join('\n');
        }
      }
      alert(errorMessage);
    } finally {
      setSubmittingReview(false);
    }
  };

  const customizationConfig = useMemo(() => {
    if (!product?.customization_zones?.length) return null;
    return {
      baseImage: getImageUrl(selectedVariant ? selectedVariant.image : product.image, true),
      zones: product.customization_zones
    };
  }, [product, selectedVariant]);


  const bulkPricing = useMemo(() => {
    if (!product) return { unitPrice: 0, total: 0, savings: 0, discount: 0 };
    const basePrice = product.discount_price || product.price;
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
    setToastMessage(`Added ${product.name} to collection`);
    setShowToast(true);
    setTimeout(() => setShowToast(false), 3000);
  };

  const [toastMessage, setToastMessage] = useState("");

  const handleShare = async () => {
    const shareData = {
      title: product.name,
      text: `Check out this amazing gift: ${product.name}`,
      url: window.location.href,
    };

    try {
      if (navigator.share) {
        await navigator.share(shareData);
      } else {
        await navigator.clipboard.writeText(window.location.href);
        setToastMessage("Link copied to clipboard!");
        setShowToast(true);
        setTimeout(() => setShowToast(false), 3000);
      }
    } catch (err) {
      console.error("Share failed", err);
    }
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
      <div className="pt-32 md:pt-40 pb-20 bg-slate-50 min-h-screen">
        <div className="container-wide px-4 sm:px-8 lg:px-12">
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

          <div className="grid lg:grid-cols-2 gap-10 items-start">
            {/* Visual Area */}
            <div className="lg:sticky lg:top-32">
               <motion.div 
                 layout
                 className="glass-card overflow-hidden relative border-slate-200/50 bg-white min-h-[300px] md:min-h-[500px] lg:min-h-[600px] flex items-center justify-center"
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
                      src={getImageUrl(selectedVariant ? selectedVariant.image : product.image) || "https://images.unsplash.com/photo-1549465220-1a8b9238cd48?auto=format&fit=crop&q=80&w=1000"} 
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
                     <button 
                        onClick={handleToggleWishlist}
                        className={`w-12 h-12 rounded-2xl border flex items-center justify-center transition-all shadow-sm ${
                          isInWishlist 
                            ? 'bg-primary text-white border-primary shadow-lg shadow-primary/20' 
                            : 'bg-white border-slate-100 text-slate-400 hover:text-primary hover:border-primary/20'
                        }`}
                      >
                        <Heart size={20} fill={isInWishlist ? "currentColor" : "none"} />
                     </button>
                     <button 
                       onClick={handleShare}
                       className="w-12 h-12 rounded-2xl bg-white border border-slate-100 flex items-center justify-center text-slate-400 hover:text-primary hover:border-primary/20 transition-all shadow-sm"
                     >
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
                        <StarRating rating={parseFloat(product.average_rating)} />
                        <span className="text-slate-400 text-xs font-bold">({product.review_count} Reviews)</span>
                      </div>
                      <h1 className="text-4xl md:text-6xl font-bold text-slate-900 mb-6 leading-tight tracking-tight">{product.name}</h1>
                      
                      {/* Pricing */}
                      <div className="flex flex-col gap-2 mb-8">
                        <div className="flex items-center gap-4 mb-8">
                           {product.discount_price && (
                             <span className="text-slate-400 line-through font-medium mr-2">₹{product.price}</span>
                           )}
                           <span className="text-5xl font-bold text-slate-900 tracking-tighter">
                             <AnimatedPrice value={bulkPricing.unitPrice} />
                           </span>
                           {bulkPricing.discount > 0 && (
                             <span className="text-green-600 font-bold text-sm bg-green-50 px-2 py-1 rounded-lg">-{bulkPricing.discount}% Bulk Discount</span>
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

                      {/* Color Variant Selection */}
                      {product.variants && product.variants.length > 0 && (
                        <div className="mb-8">
                          <label className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] block mb-4">
                            Available Colors
                          </label>
                          <div className="flex flex-wrap gap-4">
                            {product.variants.map((variant) => (
                              <button
                                key={variant.id}
                                onClick={() => setSelectedVariant(variant)}
                                className={`group relative flex flex-col items-center gap-2 transition-all ${
                                  selectedVariant?.id === variant.id ? 'scale-110' : 'opacity-60 hover:opacity-100'
                                }`}
                              >
                                <div 
                                  className={`w-10 h-10 rounded-full border-2 p-0.5 transition-all ${
                                    selectedVariant?.id === variant.id ? 'border-primary shadow-lg shadow-primary/20' : 'border-transparent'
                                  }`}
                                >
                                  <div 
                                    className="w-full h-full rounded-full border border-slate-200"
                                    style={{ 
                                      backgroundColor: {
                                        'golden': '#FFD700',
                                        'metallic golden': '#FFD700',
                                        'silver': '#C0C0C0',
                                        'tan': '#D2B48C',
                                        'crock': '#C2B280',
                                        'wooden': '#8B4513'
                                      }[variant.color_name.toLowerCase()] || variant.color_name.toLowerCase(),
                                      backgroundImage: (variant.color_name.toLowerCase() === 'wooden' || variant.color_name.toLowerCase() === 'crock') 
                                        ? 'url(https://www.transparenttextures.com/patterns/wood-pattern.png)' 
                                        : 'none'
                                    }}
                                  ></div>
                                </div>
                                <span className={`text-[9px] font-bold uppercase tracking-widest ${
                                  selectedVariant?.id === variant.id ? 'text-primary' : 'text-slate-400'
                                }`}>
                                  {variant.color_name}
                                </span>
                              </button>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Description Moved Below for better Mobile Hierarchy */}
                      <div className="hidden lg:block">
                        <p className="text-lg text-slate-500 leading-relaxed font-light">
                          {product.description}
                        </p>
                      </div>

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

                    <div className="lg:hidden">
                      <p className="text-lg text-slate-500 leading-relaxed font-light">
                        {product.description}
                      </p>
                    </div>

                    {/* Highlights Grid */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
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
                            'Doorstep Delivery in Maharashtra',
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

          {/* Reviews Section */}
          <div className="mt-40">
             <div className="flex flex-col md:flex-row justify-between items-start md:items-end mb-16 gap-8">
                 <div>
                    <span className="text-primary font-black uppercase tracking-[0.3em] text-xs mb-4 inline-block">Customer Voice</span>
                    <h2 className="text-4xl font-bold text-slate-900 tracking-tight">Product <span className="text-primary italic">Reviews</span></h2>
                    <div className="flex items-center gap-4 mt-6">
                       <div className="text-5xl font-black text-slate-900">{parseFloat(product.average_rating).toFixed(1)}</div>
                       <div>
                          <StarRating rating={parseFloat(product.average_rating)} size={20} />
                          <p className="text-xs text-slate-400 font-bold mt-1">Based on {product.review_count} verified reviews</p>
                       </div>
                    </div>
                 </div>
                 <div className="flex flex-col items-start md:items-end gap-3">
                   {hasAlreadyReviewed && !userReview && !showReviewForm && (
                     <div className="flex items-center gap-2 text-green-600 bg-green-50 px-4 py-2 rounded-xl text-xs font-bold border border-green-100">
                       <CheckCircle2 size={14} /> You have already reviewed this product
                     </div>
                   )}
                   {( !hasAlreadyReviewed || userReview ) && (
                    <button 
                      onClick={() => {
                        if (!showReviewForm && userReview) {
                          setIsEditingReview(true);
                          setNewReview({ rating: userReview.rating, comment: userReview.comment, image: null });
                        } else if (!showReviewForm) {
                          setIsEditingReview(false);
                          setNewReview({ rating: 5, comment: '', image: null });
                        }
                        setShowReviewForm(!showReviewForm);
                      }}
                      className="btn-primary py-4 px-10 text-sm shadow-xl"
                    >
                      {showReviewForm ? 'Cancel' : (userReview ? 'Edit Your Review' : 'Write a Review')}
                    </button>
                   )}
                 </div>
              </div>

             <AnimatePresence>
                {showReviewForm && (
                  <motion.div 
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    className="overflow-hidden mb-20"
                  >
                     <form onSubmit={handleReviewSubmit} className="bg-white p-10 rounded-[3rem] border border-slate-200 shadow-premium max-w-2xl mx-auto">
                        <h3 className="text-xl font-bold text-slate-900 mb-8">
                          {isEditingReview ? 'Update your experience' : 'How was your experience?'}
                        </h3>
                        
                        <div className="space-y-8">
                           <div>
                              <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest block mb-4">Your Rating</label>
                              <div className="flex gap-4">
                                 {[1, 2, 3, 4, 5].map((star) => (
                                   <button
                                     key={star}
                                     type="button"
                                     onClick={() => setNewReview({...newReview, rating: star})}
                                     className={`w-12 h-12 rounded-2xl border flex items-center justify-center transition-all ${
                                       newReview.rating >= star 
                                         ? 'bg-accent/10 border-accent text-accent shadow-sm' 
                                         : 'bg-slate-50 border-slate-100 text-slate-300 hover:border-slate-200'
                                     }`}
                                   >
                                      <Star size={24} fill={newReview.rating >= star ? "currentColor" : "none"} />
                                   </button>
                                 ))}
                              </div>
                           </div>

                           <div>
                              <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest block mb-4">Your Feedback</label>
                              <textarea 
                                required
                                rows={4}
                                placeholder="Tell us what you liked or didn't like..."
                                className="w-full px-6 py-4 rounded-2xl bg-slate-50 border border-slate-100 focus:outline-none focus:border-primary text-sm font-medium"
                                value={newReview.comment}
                                onChange={(e) => setNewReview({...newReview, comment: e.target.value})}
                              />
                           </div>

                           <div className="flex justify-end">
                              <button 
                                type="submit" 
                                disabled={submittingReview}
                                className="btn-primary py-4 px-12 text-sm shadow-2xl"
                              >
                                {submittingReview ? 'Submitting...' : (isEditingReview ? 'Update Review' : 'Post Review')}
                              </button>
                           </div>
                        </div>
                     </form>
                  </motion.div>
                )}
             </AnimatePresence>

             <div className="grid md:grid-cols-2 gap-8">
                {reviewsLoading ? (
                  [1, 2].map(n => <div key={n} className="h-48 bg-slate-200 animate-pulse rounded-[2rem]"></div>)
                ) : reviews.length > 0 ? (
                  reviews.map((review) => (
                    <motion.div 
                      key={review.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="bg-white p-8 rounded-[2.5rem] border border-slate-100 shadow-sm hover:shadow-md transition-all"
                    >
                       <div className="flex justify-between items-start mb-6">
                          <div className="flex items-center gap-4">
                             <div className="w-12 h-12 rounded-2xl bg-primary/5 flex items-center justify-center text-primary font-black text-lg">
                                {review.user_name[0].toUpperCase()}
                             </div>
                             <div>
                                <h4 className="font-bold text-slate-900">{review.user_name}</h4>
                                <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest">Verified Purchase</p>
                             </div>
                          </div>
                          <StarRating rating={review.rating} size={14} />
                       </div>
                       <p className="text-slate-600 text-sm leading-relaxed mb-6">"{review.comment}"</p>
                       <div className="flex justify-between items-center pt-6 border-t border-slate-50">
                          <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{new Date(review.created_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' })}</span>
                          <button className="text-[10px] font-black text-slate-400 hover:text-primary transition-colors flex items-center gap-2">
                             Helpful? ({review.helpful_votes})
                          </button>
                       </div>
                    </motion.div>
                  ))
                ) : (
                  <div className="md:col-span-2 text-center py-20 bg-white rounded-[3rem] border border-dashed border-slate-200">
                     <p className="text-slate-400 font-medium">No reviews yet. Be the first to share your experience!</p>
                  </div>
                )}
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
                            <div className="flex items-center justify-between">
                               <p className="text-xl font-bold text-slate-900">₹{rel.price}</p>
                               <StarRating rating={parseFloat(rel.average_rating)} size={10} />
                            </div>
                         </div>
                      </div>
                    </Link>
                  ))}
               </div>
            </div>
          )}
        </div>
      </div>
      {/* Premium Toast Notification */}
      <AnimatePresence>
        {showToast && (
          <motion.div
            initial={{ opacity: 0, y: -50, x: 50, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, x: 0, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9, transition: { duration: 0.2 } }}
            className="fixed top-24 right-8 z-[100] flex items-center gap-4 bg-white/90 backdrop-blur-xl border border-primary/20 p-5 rounded-[2rem] shadow-[0_20px_50px_-12px_rgba(217,22,86,0.2)]"
          >
            <div className={`w-12 h-12 ${toastMessage.includes('Link') ? 'bg-blue-500' : toastMessage.includes('Review') ? 'bg-emerald-500' : 'bg-primary'} text-white rounded-2xl flex items-center justify-center shadow-lg shadow-primary/20`}>
              {toastMessage.includes('Link') ? <Share2 size={24} /> : <CheckCircle2 size={24} />}
            </div>
            <div className="pr-4">
              <h3 className="text-sm font-black text-slate-900 uppercase tracking-widest">
                {toastMessage.includes('Link') ? 'Shared' : toastMessage.includes('Review') ? 'Success' : 'Added to Cart'}
              </h3>
              <p className="text-[10px] text-slate-500 font-medium">{toastMessage}</p>
            </div>
            {!toastMessage.includes('Link') && !toastMessage.includes('Review') && (
              <button 
                onClick={() => navigate('/cart')}
                className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-600 rounded-xl text-[9px] font-black uppercase tracking-widest transition-all"
              >
                View Cart
              </button>
            )}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Floating Bottom Bar for Mobile */}
      {!isCustomizing && (
        <motion.div 
          initial={{ y: 100 }}
          animate={{ y: 0 }}
          className="lg:hidden fixed bottom-0 left-0 right-0 bg-white/90 backdrop-blur-xl border-t border-slate-200/50 p-4 z-[60] flex items-center justify-between shadow-[0_-10px_30px_rgba(0,0,0,0.08)]"
        >
          <div className="flex flex-col">
            <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest leading-none mb-1">Price for {quantity} units</span>
            <span className="text-xl font-bold text-slate-900 tracking-tight">
              <AnimatedPrice value={bulkPricing.total} />
            </span>
          </div>
          <button 
            onClick={() => {
              if (customizationConfig) {
                const el = document.getElementById('add-to-cart-btn');
                if (el) {
                  el.scrollIntoView({ behavior: 'smooth' });
                } else {
                  setIsCustomizing(true);
                  window.scrollTo({ top: 0, behavior: 'smooth' });
                }
              } else {
                handleAddToCart();
              }
            }}
            className="btn-primary py-3.5 px-8 text-sm shadow-xl shadow-primary/20"
          >
            {customizationConfig && !isCustomizing ? 'Personalize' : 'Add to Cart'}
          </button>
        </motion.div>
      )}

      {/* Spacing for Floating Bar */}
      <div className="h-24 lg:hidden"></div>
    </>
  );
};

export default ProductDetail;
