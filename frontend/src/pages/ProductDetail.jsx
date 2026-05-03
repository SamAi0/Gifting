import { useState, useEffect, useMemo } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { ShieldCheck, Truck, ArrowLeft, MessageSquare, Wand2, Star, ChevronRight, CheckCircle2, Share2, Heart, Package } from 'lucide-react';
import { fetchProductById, getImageUrl } from '../api';
import api from '../api';
import CanvasCustomizer from '../components/CanvasCustomizer';
import CustomizerControls from '../components/CustomizerControls';
import { useCart } from '../context/CartContext';
import { motion, AnimatePresence } from 'framer-motion';

const ProductDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { addToCart } = useCart();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  
  // Customization State
  const [customText, setCustomText] = useState('');
  const [textColor, setTextColor] = useState('#000000'); // Default to black
  const [logoImage, setLogoImage] = useState(null);
  const [logoFile, setLogoFile] = useState(null);
  const [mockupImage, setMockupImage] = useState(null);
  const [isCustomizing, setIsCustomizing] = useState(false);
  const [relatedProducts, setRelatedProducts] = useState([]);
  const [warningMessage, setWarningMessage] = useState('');

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
           setIsCustomizing(true);
           console.log('✅ Customization enabled for this product');
        } else {
           console.warn('⚠️ No customization zones found for this product');
           console.log('💡 Run: cd backend && python sync_customization.py to load zones from JSON');
        }

        const relatedRes = await api.get('/products/', { 
          params: { category: productData.category } 
        });
        setRelatedProducts(relatedRes.data.filter(p => p.id !== parseInt(id)).slice(0, 4));
        
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
      text: customText,
      color: textColor,
      timestamp: new Date().toISOString()
    };

    addToCart(product.id, 1, customText, imageFile, customizationData, logoFile);
    navigate('/cart');
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
                    customText={customText} 
                    textColor={textColor}
                    logoImage={logoImage}
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
                    <div className="flex justify-between items-center mb-4">
                      <span className="bg-primary/10 text-primary font-black uppercase tracking-[0.3em] text-[10px] px-3 py-1 rounded-full">Branding Lab</span>
                      <button 
                        onClick={() => setIsCustomizing(false)}
                        className="text-slate-400 hover:text-red-500 font-bold text-xs uppercase tracking-widest flex items-center gap-2"
                      >
                        <ArrowLeft size={14} /> Back to Details
                      </button>
                    </div>
                    <h2 className="text-4xl font-bold text-slate-900 tracking-tight">Personalize Your Gift</h2>
                    <p className="text-slate-500 mt-2 font-light">Add your corporate identity to create a lasting impression.</p>
                  </div>
                  
                  <div className="bg-white p-8 rounded-[2.5rem] border border-slate-200/50 shadow-premium">
                    <CustomizerControls 
                      customText={customText}
                      setCustomText={(val) => { setCustomText(val); setWarningMessage(''); }}
                      zoneConfigs={customizationConfig.zones}
                      textColor={textColor}
                      setTextColor={setTextColor}
                      logoImage={logoImage}
                      setLogoImage={setLogoImage}
                      onLogoUpload={setLogoFile}
                      onReset={() => { setCustomText(''); setTextColor('#000000'); setLogoImage(null); setLogoFile(null); setWarningMessage(''); }}
                      warningMessage={warningMessage}
                    />
                  </div>

                  <div className="space-y-4">
                    <button 
                      onClick={handleAddToCart}
                      className="btn-primary w-full py-5 text-xl shadow-2xl shadow-primary/30"
                    >
                      Save & Add to Cart
                    </button>
                    <p className="text-center text-slate-400 text-xs font-medium flex items-center justify-center gap-2">
                      <ShieldCheck size={14} /> Your customization details will be verified by our designers.
                    </p>
                  </div>
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
                    <div className="flex items-end gap-4 mb-8">
                      <span className="text-5xl font-bold text-slate-900 tracking-tighter">₹{product.price}</span>
                      {product.discount_price && (
                        <div className="mb-2">
                           <span className="text-slate-400 line-through font-medium mr-2">₹{product.discount_price}</span>
                           <span className="text-green-600 font-bold text-sm bg-green-50 px-2 py-1 rounded-lg">Save ₹{product.price - product.discount_price}</span>
                        </div>
                      )}
                    </div>

                    <p className="text-lg text-slate-500 leading-relaxed font-light">
                      {product.description}
                    </p>
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
                      href={`https://wa.me/918169975287?text=Hi, I am interested in ${product.name}`}
                      target="_blank"
                      rel="noreferrer"
                      className="btn-outline border-slate-200 text-slate-900 hover:bg-slate-900 hover:text-white flex items-center justify-center px-10 py-6"
                    >
                      <MessageSquare size={24} />
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
  );
};

export default ProductDetail;

