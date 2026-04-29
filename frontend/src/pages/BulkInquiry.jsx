import { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import { Upload, CheckCircle, Phone, Mail, Building, Image as ImageIcon, ArrowRight, ShieldCheck, Zap, Target, Globe } from 'lucide-react';
import { submitBulkInquiry } from '../api';
import { motion, AnimatePresence } from 'framer-motion';

const BulkInquiry = () => {
  const location = useLocation();
  const [formData, setFormData] = useState({
    company_name: '',
    contact_person: '',
    email: '',
    phone: '',
    message: '',
    logo_file: null,
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isCustomMockup, setIsCustomMockup] = useState(false);
  const initialized = useRef(false);

  // Helper to convert DataURL to File
  const dataURLtoFile = (dataurl, filename) => {
    let arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
    bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
    while(n--){
      u8arr[n] = bstr.charCodeAt(n);
    }
    return new File([u8arr], filename, {type:mime});
  };

  // Initialize form with custom mockup data from navigation state
  useEffect(() => {
    if (location.state?.customMockup && !initialized.current) {
      initialized.current = true;
      const file = dataURLtoFile(location.state.customMockup, `branding-${location.state.productName || 'product'}.png`);
      setFormData(prev => ({ 
        ...prev, 
        logo_file: file,
        message: location.state.productName ? `Inquiry for customized ${location.state.productName}. Text applied: "${location.state.customText}"` : prev.message
      }));
      setPreviewUrl(location.state.customMockup);
      setIsCustomMockup(true);
    }
    window.scrollTo(0, 0);
  }, [location.state]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFormData({ ...formData, logo_file: file });
      setPreviewUrl(URL.createObjectURL(file));
      setIsCustomMockup(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    const data = new FormData();
    Object.keys(formData).forEach(key => {
      if (formData[key]) data.append(key, formData[key]);
    });

    try {
      await submitBulkInquiry(data);
      setIsSuccess(true);
      setFormData({
        company_name: '',
        contact_person: '',
        email: '',
        phone: '',
        message: '',
        logo_file: null,
      });
      setPreviewUrl(null);
    } catch (error) {
      console.error("Error submitting inquiry:", error);
      alert("Submission failed. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="pt-32 pb-32 bg-slate-50 min-h-screen">
      <div className="container-custom">
        <div className="max-w-7xl mx-auto">
           {/* Header Section */}
           <div className="text-center mb-24">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <span className="inline-block py-1.5 px-4 rounded-full bg-primary/10 text-primary text-[10px] font-black uppercase tracking-[0.3em] mb-6">Corporate Solutions</span>
                <h1 className="text-5xl md:text-7xl font-bold text-slate-900 mb-8 tracking-tight">Scale Your <span className="text-primary italic">Appreciation</span></h1>
                <p className="text-xl text-slate-500 max-w-3xl mx-auto font-light leading-relaxed">
                  Tailored gifting programs for employee recognition, client appreciation, and large-scale events. Get preferred pricing and dedicated support.
                </p>
              </motion.div>
           </div>

           <div className="grid lg:grid-cols-12 gap-16 items-start">
              {/* Main Form Area */}
              <motion.div 
                initial={{ opacity: 0, x: -30 }}
                animate={{ opacity: 1, x: 0 }}
                className="lg:col-span-8"
              >
                 <div className="bg-white p-8 md:p-16 rounded-[3rem] shadow-premium border border-slate-100 relative overflow-hidden">
                    <div className="absolute top-0 right-0 w-64 h-64 bg-primary/5 rounded-full blur-3xl -z-10"></div>
                    
                    <AnimatePresence mode="wait">
                      {isSuccess ? (
                        <motion.div 
                          key="success"
                          initial={{ opacity: 0, scale: 0.9 }}
                          animate={{ opacity: 1, scale: 1 }}
                          className="text-center py-20"
                        >
                           <div className="w-24 h-24 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto mb-10 shadow-lg shadow-green-100/50">
                              <CheckCircle size={48} />
                           </div>
                           <h2 className="text-4xl font-bold text-slate-900 mb-6 tracking-tight">Inquiry Submitted Successfully</h2>
                           <p className="text-slate-500 text-lg mb-12 max-w-md mx-auto font-light">Your requirements have been logged. A dedicated account manager will reach out with a custom proposal within 2 business hours.</p>
                           <button 
                             onClick={() => setIsSuccess(false)}
                             className="btn-primary px-10 py-5 text-lg shadow-2xl shadow-primary/30"
                           >
                             Submit Another Requirement
                           </button>
                        </motion.div>
                      ) : (
                        <form onSubmit={handleSubmit} className="space-y-12">
                           <div className="grid md:grid-cols-2 gap-10">
                              <div className="space-y-2 group">
                                 <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-4 group-focus-within:text-primary transition-colors flex items-center gap-2">
                                    <Building size={14} /> Company Identity
                                 </label>
                                 <input 
                                   required
                                   type="text" 
                                   name="company_name"
                                   placeholder="e.g. Acme Corporation India"
                                   className="w-full px-6 py-5 rounded-2xl bg-slate-50 border border-slate-100 focus:bg-white focus:ring-4 focus:ring-primary/5 focus:border-primary focus:outline-none transition-all text-slate-700 font-medium"
                                   value={formData.company_name}
                                   onChange={handleInputChange}
                                 />
                              </div>
                              <div className="space-y-2 group">
                                 <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-4 group-focus-within:text-primary transition-colors">
                                    Primary Contact Name
                                 </label>
                                 <input 
                                   required
                                   type="text" 
                                   name="contact_person"
                                   placeholder="Full Name"
                                   className="w-full px-6 py-5 rounded-2xl bg-slate-50 border border-slate-100 focus:bg-white focus:ring-4 focus:ring-primary/5 focus:border-primary focus:outline-none transition-all text-slate-700 font-medium"
                                   value={formData.contact_person}
                                   onChange={handleInputChange}
                                 />
                              </div>
                           </div>

                           <div className="grid md:grid-cols-2 gap-10">
                              <div className="space-y-2 group">
                                 <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-4 group-focus-within:text-primary transition-colors flex items-center gap-2">
                                    <Mail size={14} /> Work Email
                                 </label>
                                 <input 
                                   required
                                   type="email" 
                                   name="email"
                                   placeholder="name@company.com"
                                   className="w-full px-6 py-5 rounded-2xl bg-slate-50 border border-slate-100 focus:bg-white focus:ring-4 focus:ring-primary/5 focus:border-primary focus:outline-none transition-all text-slate-700 font-medium"
                                   value={formData.email}
                                   onChange={handleInputChange}
                                 />
                              </div>
                              <div className="space-y-2 group">
                                 <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-4 group-focus-within:text-primary transition-colors flex items-center gap-2">
                                    <Phone size={14} /> Direct Phone
                                 </label>
                                 <input 
                                   required
                                   type="tel" 
                                   name="phone"
                                   placeholder="+91 00000 00000"
                                   className="w-full px-6 py-5 rounded-2xl bg-slate-50 border border-slate-100 focus:bg-white focus:ring-4 focus:ring-primary/5 focus:border-primary focus:outline-none transition-all text-slate-700 font-medium"
                                   value={formData.phone}
                                   onChange={handleInputChange}
                                 />
                              </div>
                           </div>

                           <div className="space-y-2 group">
                              <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-4 group-focus-within:text-primary transition-colors">Order Brief & Special Requirements</label>
                              <textarea 
                                required
                                name="message"
                                rows="5"
                                placeholder="Describe the occasion, expected quantity, and any specific products or branding needs..."
                                className="w-full px-6 py-5 rounded-2xl bg-slate-50 border border-slate-100 focus:bg-white focus:ring-4 focus:ring-primary/5 focus:border-primary focus:outline-none transition-all text-slate-700 font-medium resize-none"
                                value={formData.message}
                                onChange={handleInputChange}
                              ></textarea>
                           </div>

                           <div className="space-y-4">
                              <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-4">
                                {isCustomMockup ? "Visual Branding Attached" : "Company Logo (SVG/PNG preferred)"}
                              </label>
                              <div className="relative">
                                 <label className={`flex flex-col items-center justify-center w-full h-72 border-2 border-dashed rounded-[2rem] cursor-pointer transition-all duration-500 overflow-hidden ${isCustomMockup ? 'border-primary bg-primary/5' : 'border-slate-200 bg-slate-50/50 hover:bg-slate-50 hover:border-primary/50 group'}`}>
                                    <div className="flex flex-col items-center justify-center p-8 text-center">
                                       {previewUrl ? (
                                          <div className="relative animate-in fade-in zoom-in duration-500">
                                             <img src={previewUrl} className="h-48 object-contain mb-4 rounded-xl shadow-premium" alt="Preview" />
                                             {isCustomMockup && (
                                               <div className="absolute -top-4 -right-4 bg-primary text-white p-3 rounded-2xl shadow-xl border-4 border-white">
                                                 <ImageIcon size={20} />
                                               </div>
                                             )}
                                             <p className="text-xs text-primary font-black uppercase tracking-widest mt-2">Click to replace</p>
                                          </div>
                                       ) : (
                                          <>
                                             <div className="w-20 h-20 rounded-3xl bg-white shadow-sm flex items-center justify-center text-slate-300 mb-6 group-hover:text-primary transition-colors">
                                                <Upload className="w-10 h-10" />
                                             </div>
                                             <p className="text-lg text-slate-900 font-bold mb-2">Drop your logo here</p>
                                             <p className="text-sm text-slate-400 font-medium max-w-xs">We'll use this to prepare a personalized catalog for your review.</p>
                                          </>
                                       )}
                                    </div>
                                    <input type="file" className="hidden" accept="image/*" onChange={handleFileChange} />
                                 </label>
                              </div>
                           </div>

                           <button 
                             type="submit" 
                             disabled={isSubmitting}
                             className="btn-primary w-full py-6 text-2xl shadow-2xl shadow-primary/30"
                           >
                             {isSubmitting ? (
                               <span className="flex items-center gap-3 justify-center">
                                  <div className="w-6 h-6 border-3 border-white/30 border-t-white rounded-full animate-spin"></div>
                                  Processing Request...
                               </span>
                             ) : (
                               <span className="flex items-center gap-3 justify-center">
                                  Initiate Bulk Inquiry <ArrowRight size={24} />
                               </span>
                             )}
                           </button>
                        </form>
                      )}
                    </AnimatePresence>
                 </div>
              </motion.div>

              {/* Sidebar Support Info */}
              <div className="lg:col-span-4 space-y-10">
                 {/* Process Steps */}
                 <motion.div 
                   initial={{ opacity: 0, x: 30 }}
                   animate={{ opacity: 1, x: 0 }}
                   transition={{ delay: 0.2 }}
                   className="bg-slate-900 p-10 rounded-[2.5rem] text-white shadow-3xl relative overflow-hidden"
                 >
                    <div className="absolute top-0 right-0 w-32 h-32 bg-primary/10 rounded-full blur-3xl"></div>
                    <h3 className="text-2xl font-bold mb-10 tracking-tight">Our Workflow</h3>
                    <div className="space-y-10">
                       {[
                         { step: '01', title: 'Concept', desc: 'Detailed requirement analysis and budgeting.', icon: Target },
                         { step: '02', title: 'Curation', desc: 'Personalized product selection and mockups.', icon: Zap },
                         { step: '03', title: 'Branding', desc: 'Precision logo application and gift wrapping.', icon: ShieldCheck },
                         { step: '04', title: 'Global Logistics', desc: 'Secure doorstep delivery to all locations.', icon: Globe },
                       ].map((item, idx) => (
                         <div key={idx} className="flex gap-6 items-start group">
                            <div className="w-12 h-12 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center font-bold text-primary flex-shrink-0 group-hover:bg-primary group-hover:text-white transition-all duration-500">
                               <item.icon size={20} />
                            </div>
                            <div>
                               <h4 className="font-bold text-lg leading-none mb-2">{item.title}</h4>
                               <p className="text-slate-400 text-sm leading-relaxed font-light">{item.desc}</p>
                            </div>
                         </div>
                       ))}
                    </div>
                 </motion.div>

                 {/* Trust Badge */}
                 <div className="bg-white p-10 rounded-[2.5rem] shadow-premium border border-slate-100">
                    <h3 className="text-xl font-bold text-slate-900 mb-8">Direct Assistance</h3>
                    <div className="space-y-8">
                       <a href="tel:+918169975287" className="flex items-center gap-5 group">
                          <div className="w-14 h-14 rounded-2xl bg-slate-50 flex items-center justify-center text-primary shadow-sm group-hover:bg-primary group-hover:text-white transition-all duration-500">
                             <Phone size={24} />
                          </div>
                          <div>
                             <p className="text-[10px] text-slate-400 font-black uppercase tracking-widest mb-1">Priority Hotline</p>
                             <p className="font-bold text-slate-900 text-lg">+91 81699 75287</p>
                          </div>
                       </a>
                       <a href="mailto:corporate@sohamgift.com" className="flex items-center gap-5 group">
                          <div className="w-14 h-14 rounded-2xl bg-slate-50 flex items-center justify-center text-primary shadow-sm group-hover:bg-primary group-hover:text-white transition-all duration-500">
                             <Mail size={24} />
                          </div>
                          <div>
                             <p className="text-[10px] text-slate-400 font-black uppercase tracking-widest mb-1">Corporate Relations</p>
                             <p className="font-bold text-slate-900 text-sm">corporate@sohamgift.com</p>
                          </div>
                       </a>
                    </div>
                 </div>

                 {/* Social Proof */}
                 <div className="text-center p-6 bg-primary/5 rounded-3xl border border-primary/10">
                    <p className="text-primary font-bold text-sm mb-2">Join 200+ Enterprises</p>
                    <p className="text-slate-500 text-xs font-medium leading-relaxed">Trusted by Fortune 500 companies and startups across India for excellence in gifting.</p>
                 </div>
              </div>
           </div>
        </div>
      </div>
    </div>
  );
};

export default BulkInquiry;

