import { useState, useEffect, useRef } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api';
import { useCart } from '../context/CartContext';
import { MapPin, CreditCard, ShieldCheck, ArrowRight, CheckCircle2, ChevronLeft, Plus, Globe, Lock } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const Checkout = () => {
  const { cart, fetchCart } = useCart();
  const [addresses, setAddresses] = useState([]);
  const [selectedAddress, setSelectedAddress] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [orderComplete, setOrderComplete] = useState(false);
  const navigate = useNavigate();
  const initialized = useRef(false);

  const [newAddress, setNewAddress] = useState({
    street_address: '',
    city: '',
    state: '',
    pincode: ''
  });

  async function fetchAddresses() {
    try {
      const res = await api.get('/orders/addresses/');
      setAddresses(res.data);
      if (res.data.length > 0) setSelectedAddress(res.data[0].id);
    } catch {
      console.error("Error fetching addresses");
    }
  }

  useEffect(() => {
    if (!initialized.current) {
      initialized.current = true;
      fetchAddresses();
      window.scrollTo(0, 0);
    }
  }, []);

  const handleAddAddress = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post('/orders/addresses/', newAddress);
      setAddresses([...addresses, res.data]);
      setSelectedAddress(res.data.id);
      setNewAddress({ street_address: '', city: '', state: '', pincode: '' });
    } catch (err) {
      console.error("Error adding address", err);
    }
  };

  const loadRazorpay = () => {
    return new Promise((resolve) => {
      const script = document.createElement('script');
      script.src = 'https://checkout.razorpay.com/v1/checkout.js';
      script.onload = () => resolve(true);
      script.onerror = () => resolve(false);
      document.body.appendChild(script);
    });
  };

  const [paymentMethod, setPaymentMethod] = useState('ONLINE');

  const handleCheckout = async () => {
    if (!selectedAddress) {
      alert("Please select or add a shipping address");
      return;
    }

    setIsProcessing(true);
    try {
      if (paymentMethod === 'ONLINE') {
        const res = await loadRazorpay();
        if (!res) {
          alert("Razorpay SDK failed to load. Are you online?");
          setIsProcessing(false);
          return;
        }

        const orderRes = await api.post('/orders/create-order/', {
          address_id: selectedAddress,
          payment_method: 'ONLINE'
        });

        const { razorpay_order_id, amount, key, order_id } = orderRes.data;

        const options = {
          key: key,
          amount: amount * 100,
          currency: "INR",
          name: "Soham Gift",
          description: `Order #${order_id}`,
          image: "https://sohamgift.com/logo.png", 
          order_id: razorpay_order_id,
          handler: async function (response) {
            try {
              await api.post('/orders/verify-payment/', {
                razorpay_order_id: response.razorpay_order_id,
                razorpay_payment_id: response.razorpay_payment_id,
                razorpay_signature: response.razorpay_signature,
              });
              setOrderComplete(true);
              fetchCart(); 
            } catch {
              alert("Payment verification failed");
            }
          },
          prefill: {
            name: "Corporate Client", 
            email: "corporate@example.com",
          },
          theme: {
            color: "#D91656",
          },
        };

        const rzp1 = new window.Razorpay(options);
        rzp1.open();
      } else {
        // Cash on Delivery
        await api.post('/orders/create-order/', {
          address_id: selectedAddress,
          payment_method: 'COD'
        });
        setOrderComplete(true);
        fetchCart();
      }
    } catch (err) {
      console.error("Checkout initiation failed", err);
      alert("Error starting checkout process");
    } finally {
      setIsProcessing(false);
    }
  };

  if (orderComplete) {
    return (
      <div className="pt-40 pb-40 text-center bg-slate-50 min-h-screen flex flex-col items-center justify-center px-4">
        <motion.div 
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          className="w-32 h-32 bg-green-100 text-green-600 rounded-full flex items-center justify-center mb-8 shadow-lg shadow-green-100/50"
        >
          <CheckCircle2 size={64} />
        </motion.div>
        <h2 className="text-4xl md:text-5xl font-bold text-slate-900 mb-4 tracking-tight">Order Confirmed!</h2>
        <p className="text-slate-500 text-lg mb-12 max-w-md mx-auto font-light leading-relaxed">
          Your transaction was successful. We've started preparing your premium gifts for dispatch. You'll receive a confirmation email shortly.
        </p>
        <div className="flex flex-col sm:flex-row gap-4">
           <button 
               onClick={() => navigate('/products')}
               className="btn-primary px-10 py-5 text-lg shadow-2xl shadow-primary/30"
           >
             Continue Gifting
           </button>
           <button 
               onClick={() => navigate('/orders')}
               className="btn-secondary px-10 py-5 text-lg"
           >
             View My Orders
           </button>
        </div>
      </div>
    );
  }

  return (
    <div className="pt-32 pb-32 bg-slate-50 min-h-screen">
      <div className="container-custom">
        <div className="flex items-center justify-between mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-slate-900 tracking-tight">Secure <span className="text-primary">Checkout</span></h1>
          <Link to="/cart" className="text-slate-400 hover:text-primary font-bold text-sm flex items-center gap-2 transition-colors">
            <ChevronLeft size={18} /> Return to Cart
          </Link>
        </div>

        <div className="grid lg:grid-cols-12 gap-12 items-start">
          <div className="lg:col-span-8 space-y-10">
            {/* Address Selection */}
            <motion.section 
               initial={{ opacity: 0, y: 20 }}
               animate={{ opacity: 1, y: 0 }}
               className="bg-white rounded-[3rem] p-8 md:p-12 shadow-premium border border-slate-100"
            >
              <div className="flex items-center gap-4 mb-10">
                <div className="w-12 h-12 rounded-2xl bg-primary/10 text-primary flex items-center justify-center">
                   <MapPin size={24} />
                </div>
                <div>
                   <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Delivery Logistics</h2>
                   <p className="text-xs text-slate-400 font-medium">Where should we dispatch your premium gifts?</p>
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-6 mb-12">
                <AnimatePresence>
                  {addresses.map((addr) => (
                    <motion.div 
                      key={addr.id}
                      layout
                      onClick={() => setSelectedAddress(addr.id)}
                      className={`p-8 rounded-[2rem] border-2 cursor-pointer transition-all duration-300 relative group overflow-hidden ${
                          selectedAddress === addr.id ? 'border-primary bg-primary/5' : 'border-slate-50 bg-slate-50 hover:border-slate-200'
                      }`}
                    >
                      {selectedAddress === addr.id && (
                        <div className="absolute top-4 right-4 text-primary">
                           <CheckCircle2 size={20} />
                        </div>
                      )}
                      <p className="font-bold text-slate-900 mb-2 leading-tight">{addr.street_address}</p>
                      <p className="text-xs text-slate-500 font-medium">{addr.city}, {addr.state} - {addr.pincode}</p>
                    </motion.div>
                  ))}
                </AnimatePresence>
                
                <button 
                  onClick={() => document.getElementById('new-address-form').scrollIntoView({ behavior: 'smooth' })}
                  className="p-8 rounded-[2rem] border-2 border-dashed border-slate-200 flex flex-col items-center justify-center gap-3 text-slate-400 hover:text-primary hover:border-primary transition-all group"
                >
                   <div className="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center group-hover:bg-primary group-hover:text-white transition-all">
                      <Plus size={20} />
                   </div>
                   <span className="text-sm font-bold uppercase tracking-widest">New Address</span>
                </button>
              </div>

              <form id="new-address-form" onSubmit={handleAddAddress} className="space-y-6 pt-10 border-t border-slate-100">
                <h3 className="text-lg font-bold text-slate-900 mb-6 flex items-center gap-2">
                   Add a New Delivery Point
                </h3>
                <div className="space-y-4">
                  <input 
                    type="text" 
                    placeholder="Full Street Address / Office Building / Unit No." 
                    className="w-full px-6 py-5 bg-slate-50 border border-slate-100 rounded-2xl focus:bg-white focus:ring-4 focus:ring-primary/5 focus:border-primary focus:outline-none transition-all text-slate-700 font-medium"
                    value={newAddress.street_address}
                    onChange={(e) => setNewAddress({...newAddress, street_address: e.target.value})}
                    required
                  />
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      <input 
                          type="text" 
                          placeholder="City" 
                          className="px-6 py-5 bg-slate-50 border border-slate-100 rounded-2xl focus:bg-white focus:ring-4 focus:ring-primary/5 focus:border-primary focus:outline-none transition-all text-slate-700 font-medium"
                          value={newAddress.city}
                          onChange={(e) => setNewAddress({...newAddress, city: e.target.value})}
                          required
                      />
                      <input 
                          type="text" 
                          placeholder="State" 
                          className="px-6 py-5 bg-slate-50 border border-slate-100 rounded-2xl focus:bg-white focus:ring-4 focus:ring-primary/5 focus:border-primary focus:outline-none transition-all text-slate-700 font-medium"
                          value={newAddress.state}
                          onChange={(e) => setNewAddress({...newAddress, state: e.target.value})}
                          required
                      />
                      <input 
                          type="text" 
                          placeholder="Pincode" 
                          className="px-6 py-5 bg-slate-50 border border-slate-100 rounded-2xl focus:bg-white focus:ring-4 focus:ring-primary/5 focus:border-primary focus:outline-none transition-all text-slate-700 font-medium"
                          value={newAddress.pincode}
                          onChange={(e) => setNewAddress({...newAddress, pincode: e.target.value})}
                          required
                      />
                  </div>
                </div>
                <button type="submit" className="btn-secondary px-8 py-4 text-sm">Save & Select Address</button>
              </form>
            </motion.section>

            {/* Payment Method Selection */}
            <motion.section 
               initial={{ opacity: 0, y: 20 }}
               animate={{ opacity: 1, y: 0 }}
               transition={{ delay: 0.1 }}
               className="bg-white rounded-[3rem] p-8 md:p-12 shadow-premium border border-slate-100"
            >
               <div className="flex items-center gap-4 mb-10">
                 <div className="w-12 h-12 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center">
                    <CreditCard size={24} />
                 </div>
                 <div>
                    <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Payment Method</h2>
                    <p className="text-xs text-slate-400 font-medium">Choose how you'd like to pay for your order.</p>
                 </div>
               </div>

               <div className="grid md:grid-cols-2 gap-6">
                  <div 
                    onClick={() => setPaymentMethod('ONLINE')}
                    className={`p-6 rounded-[2rem] border-2 cursor-pointer transition-all duration-300 flex items-center gap-4 ${
                      paymentMethod === 'ONLINE' ? 'border-primary bg-primary/5' : 'border-slate-50 bg-slate-50 hover:border-slate-200'
                    }`}
                  >
                    <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${paymentMethod === 'ONLINE' ? 'border-primary' : 'border-slate-300'}`}>
                       {paymentMethod === 'ONLINE' && <div className="w-3 h-3 bg-primary rounded-full"></div>}
                    </div>
                    <div>
                       <p className="font-bold text-slate-900">Online Payment</p>
                       <p className="text-xs text-slate-500">Cards, UPI, Netbanking</p>
                    </div>
                  </div>

                  <div 
                    onClick={() => setPaymentMethod('COD')}
                    className={`p-6 rounded-[2rem] border-2 cursor-pointer transition-all duration-300 flex items-center gap-4 ${
                      paymentMethod === 'COD' ? 'border-primary bg-primary/5' : 'border-slate-50 bg-slate-50 hover:border-slate-200'
                    }`}
                  >
                    <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${paymentMethod === 'COD' ? 'border-primary' : 'border-slate-300'}`}>
                       {paymentMethod === 'COD' && <div className="w-3 h-3 bg-primary rounded-full"></div>}
                    </div>
                    <div>
                       <p className="font-bold text-slate-900">Cash on Delivery</p>
                       <p className="text-xs text-slate-500">Pay when you receive</p>
                    </div>
                  </div>
               </div>

               {paymentMethod === 'ONLINE' && (
                 <div className="mt-8 flex flex-col md:flex-row items-center gap-8 p-8 rounded-[2rem] bg-slate-50 border border-slate-100">
                    <div className="w-20 h-20 bg-white rounded-3xl flex items-center justify-center shadow-sm">
                       <img src="https://razorpay.com/assets/razorpay-glyph.svg" className="w-10 h-10" alt="Razorpay" />
                    </div>
                    <div className="text-center md:text-left flex-grow">
                      <p className="text-xl font-bold text-slate-900 mb-1">Razorpay Secure Integration</p>
                      <p className="text-sm text-slate-500 font-medium">Global encrypted gateway for secure transactions.</p>
                    </div>
                 </div>
               )}
            </motion.section>
          </div>

          {/* Right Sidebar: Summary */}
          <div className="lg:col-span-4 sticky top-32">
            <motion.div 
               initial={{ opacity: 0, x: 20 }}
               animate={{ opacity: 1, x: 0 }}
               className="bg-slate-900 rounded-[3rem] p-10 text-white shadow-3xl relative overflow-hidden"
            >
              <div className="absolute top-0 right-0 w-32 h-32 bg-primary/20 rounded-full blur-3xl"></div>
              
              <h2 className="text-2xl font-bold mb-10 tracking-tight">Final Summary</h2>
              
              <div className="space-y-6 mb-10">
                <div className="flex justify-between items-center text-slate-400">
                  <span className="text-sm font-medium">Products Value</span>
                  <span className="text-white font-bold">₹{cart?.total_price}</span>
                </div>
                <div className="flex justify-between items-center text-slate-400">
                  <span className="text-sm font-medium">Priority Dispatch</span>
                  <span className="text-green-400 font-bold tracking-widest text-[10px] uppercase">Complimentary</span>
                </div>
                <div className="flex justify-between items-center text-slate-400">
                  <span className="text-sm font-medium">Taxation (GST)</span>
                  <span className="text-white font-bold text-xs uppercase tracking-widest italic">Inclusive</span>
                </div>
                
                <div className="pt-6 border-t border-white/10 flex justify-between items-end">
                  <div>
                     <p className="text-[10px] font-black text-primary uppercase tracking-[0.3em] mb-1">Final Amount</p>
                     <span className="text-lg font-bold">Total Payable</span>
                  </div>
                  <span className="text-5xl font-black text-white tracking-tighter">₹{cart?.total_price}</span>
                </div>
              </div>

              <div className="space-y-6">
                 <button 
                   onClick={handleCheckout}
                   disabled={isProcessing || !cart?.items?.length}
                   className={`btn-primary w-full py-6 text-2xl shadow-2xl shadow-primary/30 group flex items-center justify-center gap-3 ${isProcessing ? 'opacity-50 grayscale' : ''}`}
                 >
                   {isProcessing ? (
                     <>
                       <div className="w-6 h-6 border-3 border-white/30 border-t-white rounded-full animate-spin"></div>
                       Processing...
                     </>
                   ) : (
                     <>
                        {paymentMethod === 'COD' ? 'Confirm Order' : 'Pay Securely'} <ArrowRight size={24} className="group-hover:translate-x-2 transition-transform" />
                     </>
                   )}
                 </button>
                 
                 <div className="flex items-center justify-center gap-4 py-4 border-t border-white/5 mt-6">
                    <div className="flex flex-col items-center">
                       <ShieldCheck size={20} className="text-primary mb-1" />
                       <span className="text-[9px] font-black text-slate-500 uppercase">Verified</span>
                    </div>
                    <div className="w-px h-8 bg-white/5"></div>
                    <div className="flex flex-col items-center">
                       <Globe size={20} className="text-primary mb-1" />
                       <span className="text-[9px] font-black text-slate-500 uppercase">Secure</span>
                    </div>
                    <div className="w-px h-8 bg-white/5"></div>
                    <div className="flex flex-col items-center">
                       <Lock size={20} className="text-primary mb-1" />
                       <span className="text-[9px] font-black text-slate-500 uppercase">SSL 256-bit</span>
                    </div>
                 </div>
              </div>
            </motion.div>
            
            {/* Help Widget */}
            <div className="mt-8 p-8 bg-white rounded-[2.5rem] border border-slate-100 shadow-sm flex items-center gap-6">
               <div className="w-12 h-12 rounded-full bg-slate-50 flex items-center justify-center text-slate-400">
                  <ShieldCheck size={24} />
               </div>
               <div>
                  <p className="text-xs font-bold text-slate-900 mb-1">Need help with checkout?</p>
                  <p className="text-[10px] text-slate-400 font-medium">Contact our priority billing team at <span className="text-slate-900 font-bold">+91 81699 75287</span></p>
               </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Checkout;

